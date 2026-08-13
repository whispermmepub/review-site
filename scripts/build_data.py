#!/usr/bin/env python3
"""Extract posts from whispermmepub/Review and rebuild the review site data.

Usage:
    python3 scripts/build_data.py /path/to/Review /path/to/review-site

Writes:
    review-site/data/posts.json      -> full post content (body HTML)
    review-site/script.js            -> embedded summary list (const POSTS)
"""
import json
import os
import re
import sys
from bs4 import BeautifulSoup

MARKER = "/*__POSTS_SUMMARY__*/"


def clean_text(s):
    return re.sub(r"\s+", " ", s or "").strip()


def minify_html(s):
    s = re.sub(r">\s+<", "><", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def extract_posts(review_dir):
    posts = []
    for folder in os.listdir(review_dir):
        if not folder.isdigit():
            continue
        path = os.path.join(review_dir, folder, "index.html")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1")
        title = clean_text(title.get_text()) if title else ""

        date = author = ""
        meta = soup.find("div", class_="post-meta")
        if meta:
            mtxt = clean_text(meta.get_text())
            m = re.search(r"(\d{4}-\d{2}-\d{2})", mtxt)
            if m:
                date = m.group(1)
            m = re.search(r"✍️\s*(.+)", mtxt)
            if m:
                author = clean_text(m.group(1))

        img = soup.find("img", class_="post-image")
        image = img.get("src") if img else ""

        body_el = soup.find("div", class_="post-content")
        if body_el is None:
            body_el = soup.find("div", class_="post-body")
        body_html = ""
        body_text = ""
        if body_el:
            for tag in body_el(["script", "style"]):
                tag.decompose()
            body_html = minify_html(str(body_el.decode_contents()).strip())
            body_text = clean_text(body_el.get_text())

        excerpt = body_text[:220]
        if len(body_text) > 220:
            excerpt += "…"
        tags = re.findall(r"#([\w\u1000-\u109f_]+)", body_text)
        tags = list(dict.fromkeys(tags))[:6]

        blog_link = ""
        credit = soup.find("div", class_="reviewer-credit")
        if credit:
            a = credit.find("a", href=True)
            if a:
                blog_link = a["href"]

        posts.append({
            "id": folder,
            "title": title,
            "date": date,
            "author": author or "Whisper Of Words",
            "image": image,
            "excerpt": excerpt,
            "body": body_html,
            "tags": tags,
            "blog": blog_link,
        })

    # drop placeholder posts without a title
    posts = [p for p in posts if p["title"].strip()]
    posts.sort(key=lambda p: (p["date"] or "0000-00-00", -int(p["id"])), reverse=True)
    return posts


def rebuild_site(posts, site_dir):
    full_json = json.dumps(posts, ensure_ascii=False, separators=(",", ":"))
    data_path = os.path.join(site_dir, "data", "posts.json")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    with open(data_path, "w", encoding="utf-8") as f:
        f.write(full_json)

    summary = [{k: v for k, v in p.items() if k != "body"} for p in posts]
    summary_json = json.dumps(summary, ensure_ascii=False, separators=(",", ":"))

    script_path = os.path.join(site_dir, "script.js")
    with open(script_path, encoding="utf-8") as f:
        src = f.read()
    if MARKER not in src:
        raise SystemExit(f"marker {MARKER} not found in script.js")
    start = src.index(MARKER)
    arr = src.index("[", start)
    decoder = json.JSONDecoder()
    _, end = decoder.raw_decode(src[arr:])
    src = src[:arr] + summary_json + src[arr + end:]
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"posts: {len(posts)} | full json: {len(full_json.encode()) // 1024} KB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    rebuild_site(extract_posts(sys.argv[1]), sys.argv[2])
