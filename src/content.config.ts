import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    category: z.array(z.string()).default([]),
    description: z.string().optional(),
    image: z.string().optional(),
    slug: z.string(),
    aliases: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
