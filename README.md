# jaisellers.blog

Joshua Jai Sellers' personal blog. Hosted free on GitHub Pages.

## Publish a new post (no coding)

1. Open `content/posts/` on GitHub.
2. **Add file → Create new file**, name it like `my-post-title.md`.
3. Start it with this header, then write the post below it:

```
---
title: My Post Title
date: 2026-11-01
summary: One or two sentences for the homepage.
tag: Faith
---
```

For a Grace & Mercy entry, add `series: Grace & Mercy` and `part: 3`.
Add `draft: true` to keep a post off the site until it's ready.

### Schedule a Mosaic of Humanity release

Use `series: Mosaic of Humanity`, `part: 1`, and `publish_at:` in the
front matter. For example:

```
---
title: Radical Love Was Never Meant to Be Comfortable
date: 2026-11-10
summary: The first portrait in Mosaic of Humanity, reflecting on Jesus and radical love.
tag: Faith & Justice
series: Mosaic of Humanity
part: 1
publish_at: 2026-11-10T09:00:00-05:00
---
```

The builder leaves future posts out of the site, feed, and series listings.
GitHub Actions rebuilds at 9 a.m. Eastern every Tuesday during this season.
Scheduled workflows sometimes start a little late. Check the live blog before
posting the matching portrait and caption to your personal Facebook profile.
Facebook personal-profile publishing is a separate manual step.

4. Click **Commit changes**. The site rebuilds and goes live in about a minute.

Formatting: blank line between paragraphs, `**bold**`, `*italic*`,
`> pull quote`, and `---` for an ornamental divider.
