import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return rss({
    title: 'CyberBlog',
    description: '一个赛博朋克风格的个人技术博客',
    site: context.site || 'https://your-username.github.io',
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      link: `/blog/${post.id.replace(/\.md$/, '')}/`,
    })),
    customData: '<language>zh-CN</language>',
  });
}
