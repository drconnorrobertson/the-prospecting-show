#!/usr/bin/env python3
"""
Final pass: update nav links, blog index, sitemap, robots.txt
"""
import os, json, re
from datetime import datetime

SITE_URL = "https://the-prospecting-show.vercel.app"
BASE_DIR = "/tmp/the-prospecting-show"

# 1. Add "Host" link to nav on ALL existing pages
def update_navs():
    old_nav = '<li><a href="/guests/">'
    new_nav = '<li><a href="/host/">Host</a></li><li><a href="/guests/">'
    
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r') as fh:
                    html = fh.read()
                if old_nav in html and '<li><a href="/host/">' not in html:
                    html = html.replace(old_nav, new_nav)
                    with open(fpath, 'w') as fh:
                        fh.write(html)
                    count += 1
    print(f"Updated nav on {count} pages")

# 2. Add article:author to new blog posts
def add_article_author():
    blog_dir = os.path.join(BASE_DIR, "blog")
    new_slugs = [
        "cold-outreach-strategies-that-actually-work",
        "building-a-predictable-sales-pipeline",
        "ai-tools-transforming-sales-prospecting",
        "networking-strategies-for-entrepreneurs-in-pittsburgh",
        "the-prospecting-mindset-how-top-sellers-think",
        "lessons-from-178-entrepreneur-interviews",
    ]
    for slug in new_slugs:
        fpath = os.path.join(blog_dir, slug, "index.html")
        with open(fpath, 'r') as f:
            html = f.read()
        if 'article:author' not in html:
            html = html.replace('</head>', '    <meta property="article:author" content="Dr. Connor Robertson">\n    <meta property="article:publisher" content="The Prospecting Show">\n</head>')
            with open(fpath, 'w') as f:
                f.write(html)
    print("Added article:author to new blog posts")

# 3. Update blog index to include new posts
def update_blog_index():
    blog_index = os.path.join(BASE_DIR, "blog", "index.html")
    with open(blog_index, 'r') as f:
        html = f.read()
    
    new_posts = [
        {"slug": "cold-outreach-strategies-that-actually-work", "title": "Cold Outreach Strategies That Actually Work in 2026", "date": "Apr 20, 2026", "desc": "Dr. Connor Robertson breaks down the cold outreach strategies generating real results. From email to LinkedIn to phone, learn what top performers do differently.", "read": "9 min read", "tags": ["Cold Outreach", "Sales", "Prospecting"]},
        {"slug": "building-a-predictable-sales-pipeline", "title": "How to Build a Predictable Sales Pipeline from Scratch", "date": "Apr 12, 2026", "desc": "The step-by-step framework for building a sales pipeline that generates consistent, predictable revenue. Based on insights from 178+ Prospecting Show episodes.", "read": "10 min read", "tags": ["Sales Pipeline", "B2B", "Revenue"]},
        {"slug": "ai-tools-transforming-sales-prospecting", "title": "How AI Is Transforming Sales Prospecting in 2026", "date": "Apr 5, 2026", "desc": "How artificial intelligence is reshaping sales prospecting, from AI-powered lead scoring to automated personalization and predictive analytics.", "read": "8 min read", "tags": ["AI", "Sales Tech", "Automation"]},
        {"slug": "networking-strategies-for-entrepreneurs-in-pittsburgh", "title": "Networking Strategies for Entrepreneurs in Pittsburgh", "date": "Mar 28, 2026", "desc": "Proven networking strategies for entrepreneurs in Pittsburgh. From local events to digital communities, learn how Pittsburgh business owners build valuable connections.", "read": "7 min read", "tags": ["Networking", "Pittsburgh", "Business"]},
        {"slug": "the-prospecting-mindset-how-top-sellers-think", "title": "The Prospecting Mindset: How Top Sellers Think Differently", "date": "Mar 20, 2026", "desc": "The mental frameworks that separate top sales performers from the rest. Based on patterns from 178+ interviews on The Prospecting Show.", "read": "8 min read", "tags": ["Mindset", "Sales", "Performance"]},
        {"slug": "lessons-from-178-entrepreneur-interviews", "title": "10 Lessons from Interviewing 178 Entrepreneurs", "date": "Mar 10, 2026", "desc": "Dr. Connor Robertson distills the most important lessons from 178+ interviews with entrepreneurs. The patterns and principles that separate successful businesses.", "read": "11 min read", "tags": ["Entrepreneurship", "Lessons", "Strategy"]},
    ]
    
    cards_html = ""
    for p in new_posts:
        tags = "".join([f'<span class="topic-tag">{t}</span>' for t in p["tags"]])
        cards_html += f'''
        <div class="episode-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="color:var(--text-muted); font-size:0.85rem;">{p["date"]}</span>
                <span style="color:var(--text-muted); font-size:0.85rem;">{p["read"]}</span>
            </div>
            <h3><a href="/blog/{p["slug"]}/">{p["title"]}</a></h3>
            <p class="episode-desc">{p["desc"]}</p>
            <div class="episode-topics">{tags}</div>
            <div style="margin-top:12px;">
                <span style="color:var(--text-muted); font-size:0.85rem;">By <a href="/host/">Dr. Connor Robertson</a></span>
            </div>
        </div>'''
    
    # Insert before existing blog grid content
    marker = '<div class="episodes-grid">'
    if marker in html:
        # Find the grid and insert new cards at the beginning
        idx = html.index(marker) + len(marker)
        html = html[:idx] + cards_html + html[idx:]
    
    with open(blog_index, 'w') as f:
        f.write(html)
    print("Updated blog index with new posts")

# 4. Generate comprehensive sitemap
def generate_sitemap():
    urls = []
    
    # Static pages
    static = [
        ("/", "1.0", "weekly"),
        ("/episodes/", "0.9", "weekly"),
        ("/about/", "0.8", "monthly"),
        ("/host/", "0.9", "monthly"),
        ("/guests/", "0.8", "weekly"),
        ("/blog/", "0.8", "weekly"),
        ("/subscribe/", "0.7", "monthly"),
        ("/contact/", "0.6", "monthly"),
    ]
    for path, pri, freq in static:
        urls.append(f'''  <url>
    <loc>{SITE_URL}{path}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{pri}</priority>
    <lastmod>2026-04-24</lastmod>
  </url>''')
    
    # Episodes
    episodes_dir = os.path.join(BASE_DIR, "episodes")
    for slug in sorted(os.listdir(episodes_dir)):
        if slug == "index.html":
            continue
        ep_path = os.path.join(episodes_dir, slug, "index.html")
        if os.path.isfile(ep_path):
            urls.append(f'''  <url>
    <loc>{SITE_URL}/episodes/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>''')
    
    # Blog posts
    blog_dir = os.path.join(BASE_DIR, "blog")
    for slug in sorted(os.listdir(blog_dir)):
        if slug == "index.html":
            continue
        bp_path = os.path.join(blog_dir, slug, "index.html")
        if os.path.isfile(bp_path):
            urls.append(f'''  <url>
    <loc>{SITE_URL}/blog/{slug}/</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <lastmod>2026-04-24</lastmod>
  </url>''')
    
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>'''
    
    with open(os.path.join(BASE_DIR, "sitemap.xml"), 'w') as f:
        f.write(sitemap)
    print(f"Generated sitemap.xml with {len(urls)} URLs")

# 5. Fix robots.txt
def fix_robots():
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    with open(os.path.join(BASE_DIR, "robots.txt"), 'w') as f:
        f.write(robots)
    print("Fixed robots.txt")

if __name__ == "__main__":
    print("=== Finalization Script ===\n")
    update_navs()
    add_article_author()
    update_blog_index()
    generate_sitemap()
    fix_robots()
    print("\n=== Done ===")
