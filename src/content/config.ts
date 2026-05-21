import { defineCollection, z } from "astro:content";

const docs = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    description: z.string(),
    category: z.string(),
    level: z.string().optional(),
    order: z.number().default(999),
    tags: z.array(z.string()).default([]),
    updated: z.string().optional(),
  }),
});

export const collections = { docs };
