import os, base64, json, urllib.request, subprocess, sys

REPO = "cs960903/cyberblog"
WORK_DIR = r"D:\project\autoclaw-workspace\cyberblog"
TOKEN = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()
API = f"https://api.github.com/repos/{REPO}"

GITIGNORE = {"node_modules", ".git", "dist", ".astro", "__pycache__"}
BINARY_EXTS = {".ico", ".png", ".jpg", ".jpeg", ".gif", ".woff", ".woff2", ".eot", ".ttf"}

def gh_api(method, path, data=None):
    url = f"{API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "cyberblog-push")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
        return None

# Step 0: Create repo via gh
print("Creating repo...")
subprocess.run(["gh", "repo", "create", REPO, "--public", "--description", "CyberBlog"], check=True)

# Step 1: Collect and sort files
print("\nCollecting files...")
files = []
for root, dirs, names in os.walk(WORK_DIR):
    dirs[:] = [d for d in dirs if d not in GITIGNORE]
    for name in names:
        fp = os.path.join(root, name)
        rel = os.path.relpath(fp, WORK_DIR).replace("\\", "/")
        if name in {".DS_Store"}:
            continue
        files.append((rel, fp))

files.sort(key=lambda x: x[0])
print(f"  {len(files)} files")

# Step 2: Initialize repo via Contents API (creates first file and initializes the Git repo)
print("\nInitializing repo with first file...")
first_rel, first_fp = files[0]
with open(first_fp, "rb") as f:
    content = base64.b64encode(f.read()).decode()
result = gh_api("PUT", f"/contents/{first_rel}", {
    "message": f"init: {first_rel}",
    "content": content
})
if result and "content" in result:
    print(f"  Created: {first_rel}")
else:
    print(f"  Failed to init repo")
    sys.exit(1)

files = files[1:]  # Remove the first file from the list

# Step 3: Create blobs for remaining files (Git Data API now works since repo is initialized)
print("\nCreating blobs...")
blobs = {}
for relpath, filepath in files:
    with open(filepath, "rb") as f:
        raw = f.read()
    ext = os.path.splitext(relpath)[1].lower()
    is_binary = ext in BINARY_EXTS
    if is_binary:
        blob_data = {"content": base64.b64encode(raw).decode(), "encoding": "base64"}
    else:
        try:
            blob_data = {"content": raw.decode("utf-8"), "encoding": "utf-8"}
        except:
            blob_data = {"content": base64.b64encode(raw).decode(), "encoding": "base64"}
    blob = gh_api("POST", "/git/blobs", blob_data)
    if blob and "sha" in blob:
        blobs[relpath] = blob["sha"]

print(f"  {len(blobs)}/{len(files)} blobs created")

# Step 4: Get the current commit/tree to build upon
print("\nGetting current state...")
ref = gh_api("GET", "/git/ref/heads/main")
if not ref or "object" not in ref:
    print("  Failed to get current ref")
    sys.exit(1)

current_commit = gh_api("GET", f"/git/commits/{ref['object']['sha']}")
if not current_commit or "tree" not in current_commit:
    print("  Failed to get current commit")
    sys.exit(1)
base_tree_sha = current_commit["tree"]["sha"]

# Step 5: Create a new tree with all new files
print("Creating tree...")
# First get existing tree so we can include existing files
existing_tree = gh_api("GET", f"/git/trees/{base_tree_sha}")
existing_items = existing_tree.get("tree", []) if existing_tree else []

# Combine existing items with new blobs (new items override existing)
existing_paths = {item["path"]: item for item in existing_items}
new_tree_items = list(existing_items)

for path, sha in blobs.items():
    # Remove old entry if exists
    new_tree_items = [i for i in new_tree_items if i["path"] != path]
    new_tree_items.append({
        "path": path,
        "mode": "100644",
        "type": "blob",
        "sha": sha
    })

tree = gh_api("POST", "/git/trees", {"tree": new_tree_items})
if not tree or "sha" not in tree:
    print("  Failed to create tree")
    sys.exit(1)
print(f"  Tree: {tree['sha']}")

# Step 6: Create commit
print("Creating commit...")
commit = gh_api("POST", "/git/commits", {
    "message": "fix: 配置 base=/cyberblog 修复子路径 CSS/链接问题\n\n- 添加 base 配置使 CSS/JS 路径正确前缀 /cyberblog/\n- 所有内部链接改用 import.meta.env.BASE_URL\n- 添加 .gitattributes 处理行尾\n- 清理 .astro 缓存文件",
    "tree": tree["sha"],
    "parents": [ref["object"]["sha"]]
})
if not commit or "sha" not in commit:
    print("  Failed to create commit")
    sys.exit(1)
print(f"  Commit: {commit['sha']}")

# Step 7: Update ref
print("Updating ref...")
result = gh_api("PATCH", "/git/refs/heads/main", {
    "sha": commit["sha"],
    "force": True
})
if result:
    print(f"\n✅ 成功推送到 GitHub!")
    print(f"   https://github.com/{REPO}")
else:
    print("❌ 推送失败")
