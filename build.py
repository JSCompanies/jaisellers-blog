#!/usr/bin/env python3
"""Builds jaisellers.blog into _site/.

To publish a new post: add a .md file to content/posts/ with this header,
commit it, and GitHub builds and deploys the site automatically.

---
title: Your Title
date: 2026-11-01
summary: One or two sentences for the homepage.
tag: Faith                 (optional label)
series: Grace & Mercy      (optional; only for series posts)
part: 3                    (optional; series number)
draft: true                (optional; keeps the post off the site)
---
"""
import datetime as dt
import os
import html
import pathlib
import re
import shutil

import markdown

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "_site"
SITE_URL = "https://jaisellers.blog"
# Subfolder the site is served from. Empty on the custom domain (jaisellers.blog);
# "/jaisellers-blog" while it lives at jscompanies.github.io/jaisellers-blog/.
BASE_PATH = os.environ.get("BASE_PATH", "").rstrip("/")


def rebase(text):
    """Prefix root-relative links (href="/...", src="/...") with BASE_PATH."""
    if not BASE_PATH:
        return text
    return re.sub(r'((?:href|src)=")/(?!/)', rf"\1{BASE_PATH}/", text)
SERIES_INTRO = {
    "Grace & Mercy": "A numbered sequence on the distance between what the church says about grace and what it practices. Personal story first, then the prophetic and policy turn.",
}
ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..900;1,6..96,400..900&family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Jost:wght@400;500&display=swap">')

CREST_DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7D5E1C"/><stop offset=".35" stop-color="#C9A84C"/><stop offset=".5" stop-color="#E8D5A8"/><stop offset=".68" stop-color="#C9A84C"/><stop offset="1" stop-color="#7D5E1C"/></linearGradient>
<symbol id="laurel" viewBox="0 0 120 120">
<circle class="ring" cx="60" cy="60" r="56" fill="none" stroke="url(#foil)" stroke-width="1.6"/>
<circle cx="60" cy="60" r="49" fill="none" stroke="url(#foil)" stroke-width=".7" opacity=".55"/>
<g fill="url(#foil)">
<ellipse cx="27" cy="78" rx="3.2" ry="7" transform="rotate(-35 27 78)"/><ellipse cx="23" cy="66" rx="3.2" ry="7" transform="rotate(-15 23 66)"/><ellipse cx="23" cy="53" rx="3.2" ry="7" transform="rotate(5 23 53)"/><ellipse cx="27" cy="41" rx="3.2" ry="7" transform="rotate(25 27 41)"/><ellipse cx="34" cy="31" rx="3" ry="6.4" transform="rotate(45 34 31)"/>
<ellipse cx="93" cy="78" rx="3.2" ry="7" transform="rotate(35 93 78)"/><ellipse cx="97" cy="66" rx="3.2" ry="7" transform="rotate(15 97 66)"/><ellipse cx="97" cy="53" rx="3.2" ry="7" transform="rotate(-5 97 53)"/><ellipse cx="93" cy="41" rx="3.2" ry="7" transform="rotate(-25 93 41)"/><ellipse cx="86" cy="31" rx="3" ry="6.4" transform="rotate(-45 86 31)"/>
</g>
<path d="M34 88 Q60 100 86 88" fill="none" stroke="url(#foil)" stroke-width="1.2"/>
<circle cx="60" cy="95" r="2.6" fill="#A3283A" stroke="url(#foil)" stroke-width=".8"/>
<text x="60" y="71" text-anchor="middle" font-family="Bodoni Moda, Didot, serif" font-style="italic" font-weight="700" font-size="34" fill="url(#foil)">JS</text>
</symbol></defs></svg>"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
           "%3Crect width='100' height='100' rx='50' fill='%230C0C0E'/%3E"
           "%3Ccircle cx='50' cy='50' r='44' fill='none' stroke='%23C9A84C' stroke-width='4'/%3E"
           "%3Ctext x='50' y='64' text-anchor='middle' font-family='Georgia,serif' font-style='italic' font-weight='700' font-size='40' fill='%23C9A84C'%3EJS%3C/text%3E%3C/svg%3E")

e = html.escape


def page(title, description, body, path="/"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:type" content="{'article' if path.startswith('/posts/') else 'website'}">
<meta name="theme-color" content="#0C0C0E">
<link rel="canonical" href="{SITE_URL}{path}">
<link rel="icon" href="{FAVICON}">
<link rel="alternate" type="application/rss+xml" title="Joshua Jai Sellers" href="/feed.xml">
{FONTS}
<link rel="stylesheet" href="/style.css">
</head>
<body>
{CREST_DEFS}
<nav class="site"><div class="wrap">
<a class="mark" href="/" aria-label="Joshua Jai Sellers, home"><svg viewBox="0 0 120 120" aria-hidden="true"><use href="#laurel"/></svg><span>Jai Sellers</span></a>
<ul><li><a href="/#essays">Essays</a></li><li><a href="/#series">Grace &amp; Mercy</a></li><li><a href="/#about">About</a></li><li><a href="https://jaisellers.com">JSCo</a></li></ul>
</div></nav>
{body}
<footer class="site"><div class="wrap">
<svg viewBox="0 0 120 120" aria-hidden="true"><use href="#laurel"/></svg>
<div class="line1 foil">Joshua Jai Sellers</div>
<div class="line2">JaiSellers Companies · Personal Correspondence Edition</div>
</div></footer>
</body>
</html>
"""


def load_posts():
    posts = []
    for f in sorted((ROOT / "content" / "posts").glob("*.md")):
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if not m:
            raise SystemExit(f"{f.name}: missing the --- header block")
        meta = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip('"').strip("'")
        if meta.get("draft", "").lower() == "true":
            continue
        for req in ("title", "date", "summary"):
            if not meta.get(req):
                raise SystemExit(f"{f.name}: header needs a '{req}:' line")
        meta["date_obj"] = dt.date.fromisoformat(meta["date"])
        meta["part"] = int(meta["part"]) if meta.get("part") else None
        meta["slug"] = f.stem
        meta["url"] = f"/posts/{f.stem}/"
        meta["html"] = markdown.markdown(m.group(2), extensions=["smarty"])
        posts.append(meta)
    posts.sort(key=lambda p: (p["date_obj"], p["part"] or 0), reverse=True)
    return posts


def nice_date(d):
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def label(p):
    if p.get("series"):
        return f'{e(p["series"])} · {ROMAN[p["part"]] if p["part"] and p["part"] < len(ROMAN) else p["part"] or ""}'
    return e(p.get("tag", "Essay"))


def series_list(name, posts, current=None):
    parts = sorted([p for p in posts if p.get("series") == name], key=lambda p: p["part"] or 0)
    rows = []
    for p in parts:
        cur = " current" if current and p["slug"] == current else ""
        num = ROMAN[p["part"]] if p["part"] and p["part"] < len(ROMAN) else (p["part"] or "")
        rows.append(f'<a class="series-item live{cur}" href="{p["url"]}"><div class="numeral foil">{num}</div>'
                    f'<div class="body"><h4>{e(p["title"])}</h4><small>{nice_date(p["date_obj"])}</small></div>'
                    f'<div class="status">{"Reading" if cur else "Published"}</div></a>')
    nxt = (parts[-1]["part"] or len(parts)) + 1 if parts else 1
    num = ROMAN[nxt] if nxt < len(ROMAN) else nxt
    rows.append(f'<div class="series-item pending"><div class="numeral foil">{num}</div>'
                f'<div class="body"><h4>To be announced</h4><small>In the writing room</small></div>'
                f'<div class="status">Forthcoming</div></div>')
    return '<div class="series-list">' + "".join(rows) + "</div>"


def build_home(posts):
    essays = "".join(
        f'<article class="essay"><div class="meta"><span class="tag">{label(p)}</span><span>{nice_date(p["date_obj"])}</span></div>'
        f'<div><h3><a href="{p["url"]}">{e(p["title"])}</a></h3><p>{e(p["summary"])}</p>'
        f'<a class="read" href="{p["url"]}">Read the essay</a></div></article>'
        for p in posts)
    series_names = sorted({p["series"] for p in posts if p.get("series")})
    series_html = "".join(
        f'<section class="series" id="series"><div class="wrap"><div class="section-label"><div>'
        f'<div class="eyebrow">Ongoing Series</div><h2><span class="foil">{e(n)}</span></h2></div></div>'
        f'<p class="intro">{e(SERIES_INTRO.get(n, ""))}</p>{series_list(n, posts)}</div></section>'
        for n in series_names)
    body = f"""<header class="hero" id="top"><div class="wrap">
<svg class="crest" viewBox="0 0 120 120" role="img" aria-label="JS laurel crest"><use href="#laurel"/></svg>
<div class="eyebrow">Personal Correspondence Edition</div>
<h1><span class="foil">Joshua</span><br><em class="foil">Jai Sellers</em></h1>
<p class="lede">Essays on faith, justice, and the long work of coming home.</p>
<div class="ornament" aria-hidden="true"><i></i></div>
</div></header>
<section id="essays"><div class="wrap">
<div class="section-label"><div><div class="eyebrow">The Ledger</div><h2>Recent Essays</h2></div></div>
{essays}
</div></section>
{series_html}
<section class="about" id="about"><div class="wrap">
<blockquote>Grace is not a feeling. It is a practice, and it shows up in policy.</blockquote>
<div>
<p>I'm Joshua Jai Sellers, founder of JaiSellers Companies and the Just Systems Initiative in Kings Mountain, North Carolina.</p>
<p>Before consulting and design, I was a classically trained vocalist. These days I build nonprofit systems, write grants, and work on justice reform and reentry in Cleveland County.</p>
<p>This blog is the personal side of that work: faith, justice, and the people the systems were supposed to serve.</p>
</div></div></section>"""
    return page("Joshua Jai Sellers", "Essays on faith, justice, and the long work of coming home.", body)


def build_post(p, posts):
    i = posts.index(p)
    newer = posts[i - 1] if i > 0 else None
    older = posts[i + 1] if i + 1 < len(posts) else None
    series_block = ""
    if p.get("series"):
        series_block = (f'<div class="wrap post-series"><div class="section-label"><div><div class="eyebrow">The Series</div>'
                        f'<h2><span class="foil">{e(p["series"])}</span></h2></div></div>{series_list(p["series"], posts, p["slug"])}</div>')
    pager = '<div class="wrap pager">'
    pager += (f'<a href="{older["url"]}"><span class="eyebrow">Previous essay</span><h5>{e(older["title"])}</h5></a>' if older else "<span></span>")
    pager += (f'<a href="{newer["url"]}"><span class="eyebrow">Next essay</span><h5>{e(newer["title"])}</h5></a>' if newer else "<span></span>")
    pager += "</div>"
    body = f"""<header class="article-head"><div class="wrap">
<svg class="crest" viewBox="0 0 120 120" aria-hidden="true"><use href="#laurel"/></svg>
<div class="eyebrow">{label(p)}</div>
<h1 class="foil">{e(p["title"])}</h1>
<p class="dek">{e(p["summary"])}</p>
<div class="byline"><span>Joshua Jai Sellers</span><span>{nice_date(p["date_obj"])}</span></div>
</div></header>
<article class="wrap"><div class="prose">{p["html"]}</div></article>
{series_block}
{pager}"""
    return page(f'{p["title"]} · Joshua Jai Sellers', p["summary"], body, p["url"])


def build_feed(posts):
    items = "".join(
        f"<item><title>{e(p['title'])}</title><link>{SITE_URL}{p['url']}</link><guid>{SITE_URL}{p['url']}</guid>"
        f"<pubDate>{dt.datetime.combine(p['date_obj'], dt.time(12)).strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>"
        f"<description>{e(p['summary'])}</description></item>"
        for p in posts)
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Joshua Jai Sellers</title>'
            f"<link>{SITE_URL}</link><description>Essays on faith, justice, and the long work of coming home.</description>{items}</channel></rss>")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    posts = load_posts()
    (OUT / "index.html").write_text(rebase(build_home(posts)), encoding="utf-8")
    for p in posts:
        d = OUT / "posts" / p["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(rebase(build_post(p, posts)), encoding="utf-8")
    (OUT / "feed.xml").write_text(build_feed(posts), encoding="utf-8")
    (OUT / "404.html").write_text(rebase(page("Page not found · Joshua Jai Sellers", "Page not found.",
        '<header class="hero"><div class="wrap"><svg class="crest" viewBox="0 0 120 120" aria-hidden="true"><use href="#laurel"/></svg>'
        '<div class="eyebrow">Error 404</div><h1><em class="foil">Not here.</em></h1>'
        '<p class="lede">That page doesn\'t exist. <a href="/">Return to the essays.</a></p></div></header>')), encoding="utf-8")
    shutil.copy(ROOT / "static" / "style.css", OUT / "style.css")
    if not BASE_PATH:
        (OUT / "CNAME").write_text("jaisellers.blog\n")
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(posts)} posts into {OUT}")


if __name__ == "__main__":
    main()
