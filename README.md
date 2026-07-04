# andersonberg.com.br

Personal blog, built with [Astro](https://astro.build). Migrated from Gatsby in 2026.

## Structure

```text
/
├── public/
│   ├── images/            # post images and avatar
│   └── _redirects         # legacy URL redirects (Cloudflare Pages)
├── src/
│   ├── content/blog/      # posts (Markdown/MDX)
│   ├── content.config.ts  # post frontmatter schema
│   ├── layouts/
│   ├── components/
│   └── pages/
└── astro.config.mjs
```

## Commands

| Command           | Action                                      |
| :----------------- | :------------------------------------------ |
| `npm install`       | Install dependencies                        |
| `npm run dev`       | Start local dev server at `localhost:4321`  |
| `npm run build`     | Build production site to `./dist/`          |
| `npm run preview`   | Preview the production build locally        |

## Deployment

Deployed via Cloudflare Pages, connected to this repo. Every push to `master` deploys to production; every other branch/PR gets its own preview URL.
