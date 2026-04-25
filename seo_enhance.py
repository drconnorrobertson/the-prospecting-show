#!/usr/bin/env python3
"""
Comprehensive SEO enhancement script for The Prospecting Show.
Adds Person schema, BreadcrumbList, enhances OG/Twitter tags, 
strengthens Dr. Connor Robertson entity signals across all pages.
"""

import os
import re
import json
from datetime import datetime

SITE_URL = "https://the-prospecting-show.vercel.app"
BASE_DIR = "/tmp/the-prospecting-show"

# ─────────────────────────────────────────────
# PERSON SCHEMA (goes on EVERY page)
# ─────────────────────────────────────────────
PERSON_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": "https://drconnorrobertson.com/#person",
    "name": "Dr. Connor Robertson",
    "givenName": "Connor",
    "familyName": "Robertson",
    "honorificPrefix": "Dr.",
    "url": "https://drconnorrobertson.com",
    "jobTitle": "Entrepreneur, Podcast Host, Business Strategist",
    "description": "Dr. Connor Robertson is a Pittsburgh-based entrepreneur, podcast host of The Prospecting Show, and business strategist helping entrepreneurs scale through sales, prospecting, and business development.",
    "knowsAbout": ["Sales", "Prospecting", "B2B Sales", "Business Development", "Entrepreneurship", "Lead Generation", "Cold Outreach", "Podcasting", "Digital Marketing", "Pittsburgh Business"],
    "sameAs": [
        "https://drconnorrobertson.com",
        "https://thepittsburghwire.com",
        "https://elixirconsultinggroup.com",
        "https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX",
        "https://www.linkedin.com/in/drconnorrobertson/"
    ],
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Pittsburgh",
        "addressRegion": "PA",
        "addressCountry": "US"
    },
    "worksFor": [
        {
            "@type": "Organization",
            "name": "The Prospecting Show",
            "url": SITE_URL
        },
        {
            "@type": "Organization",
            "name": "Elixir Consulting Group",
            "url": "https://elixirconsultinggroup.com"
        }
    ]
}

# ─────────────────────────────────────────────
# ENHANCED PODCAST SERIES SCHEMA (homepage)
# ─────────────────────────────────────────────
PODCAST_SERIES_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "PodcastSeries",
    "@id": f"{SITE_URL}/#podcast",
    "name": "The Prospecting Show with Dr. Connor Robertson",
    "description": "Every week, Dr. Connor Robertson interviews entrepreneurs and small business owners about how they built, scaled, and grew their businesses. Real stories. Real strategies. Real results. Covering sales, prospecting, lead generation, business systems, digital marketing, and entrepreneurship.",
    "url": SITE_URL,
    "webFeed": "https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX",
    "genre": ["Business", "Entrepreneurship", "Sales", "Marketing", "Investing"],
    "inLanguage": "en",
    "author": {"@id": "https://drconnorrobertson.com/#person"},
    "creator": {"@id": "https://drconnorrobertson.com/#person"},
    "publisher": {
        "@type": "Organization",
        "name": "The Prospecting Show",
        "url": SITE_URL,
        "founder": {"@id": "https://drconnorrobertson.com/#person"}
    },
    "numberOfEpisodes": 178,
    "startDate": "2019",
    "keywords": "prospecting, sales, B2B, lead generation, cold outreach, business development, entrepreneurship, Dr. Connor Robertson, Pittsburgh"
}

WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": f"{SITE_URL}/#website",
    "name": "The Prospecting Show with Dr. Connor Robertson",
    "url": SITE_URL,
    "description": "The Prospecting Show podcast hosted by Dr. Connor Robertson -- interviews with entrepreneurs about sales, prospecting, and business growth.",
    "publisher": {"@id": "https://drconnorrobertson.com/#person"},
    "inLanguage": "en"
}

def make_breadcrumb(items):
    """Generate BreadcrumbList schema from list of (name, url) tuples."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url
            }
            for i, (name, url) in enumerate(items)
        ]
    }

def get_breadcrumb_for_path(path):
    """Determine breadcrumb based on file path relative to site root."""
    rel = path.replace(BASE_DIR, "").strip("/")
    crumbs = [("Home", SITE_URL + "/")]
    
    if rel == "index.html":
        return None  # No breadcrumb on homepage
    elif rel.startswith("episodes/") and rel != "episodes/index.html":
        slug = rel.replace("episodes/", "").replace("/index.html", "")
        crumbs.append(("Episodes", SITE_URL + "/episodes/"))
        # Get episode title from the file
        crumbs.append((slug.replace("-", " ").title()[:60], SITE_URL + "/" + rel.replace("/index.html", "/")))
    elif rel == "episodes/index.html":
        crumbs.append(("Episodes", SITE_URL + "/episodes/"))
    elif rel.startswith("blog/") and rel != "blog/index.html":
        slug = rel.replace("blog/", "").replace("/index.html", "")
        crumbs.append(("Blog", SITE_URL + "/blog/"))
        crumbs.append((slug.replace("-", " ").title()[:60], SITE_URL + "/" + rel.replace("/index.html", "/")))
    elif rel == "blog/index.html":
        crumbs.append(("Blog", SITE_URL + "/blog/"))
    elif rel == "about/index.html":
        crumbs.append(("About", SITE_URL + "/about/"))
    elif rel == "host/index.html":
        crumbs.append(("Host", SITE_URL + "/host/"))
    elif rel == "guests/index.html":
        crumbs.append(("Guests", SITE_URL + "/guests/"))
    elif rel == "contact/index.html":
        crumbs.append(("Contact", SITE_URL + "/contact/"))
    elif rel == "subscribe/index.html":
        crumbs.append(("Subscribe", SITE_URL + "/subscribe/"))
    else:
        return None
    
    return make_breadcrumb(crumbs)

def inject_schemas(html, path):
    """Inject Person schema and BreadcrumbList into every page."""
    rel = path.replace(BASE_DIR, "").strip("/")
    
    schemas_to_add = []
    
    # Always add Person schema (if not already a rich version)
    schemas_to_add.append(PERSON_SCHEMA)
    
    # Add breadcrumb
    bc = get_breadcrumb_for_path(path)
    if bc:
        schemas_to_add.append(bc)
    
    # On homepage, add enhanced PodcastSeries + WebSite
    if rel == "index.html":
        schemas_to_add.append(PODCAST_SERIES_SCHEMA)
        schemas_to_add.append(WEBSITE_SCHEMA)
    
    # Build script tags
    new_scripts = ""
    for schema in schemas_to_add:
        new_scripts += f'\n<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'
    
    # Insert before </head>
    if "</head>" in html:
        html = html.replace("</head>", new_scripts + "\n</head>")
    
    return html

def fix_canonical_urls(html, path):
    """Update canonical URLs to use the Vercel domain."""
    html = html.replace("https://drconnorrobertson.github.io", SITE_URL)
    return html

def enhance_og_tags(html, path):
    """Add missing OG and Twitter tags."""
    rel = path.replace(BASE_DIR, "").strip("/")
    
    # Add og:locale if missing
    if 'og:locale' not in html:
        html = html.replace('<meta property="og:type"', '<meta property="og:locale" content="en_US">\n    <meta property="og:type"')
    
    # Add article:author for blog posts
    if rel.startswith("blog/") and rel != "blog/index.html":
        if 'article:author' not in html:
            html = html.replace('</head>', '    <meta property="article:author" content="Dr. Connor Robertson">\n    <meta property="article:publisher" content="The Prospecting Show">\n</head>')
    
    return html

def strengthen_entity(html, path):
    """Ensure strong Dr. Connor Robertson presence."""
    rel = path.replace(BASE_DIR, "").strip("/")
    
    # For episode pages, ensure title includes Dr. Connor Robertson
    if rel.startswith("episodes/") and rel != "episodes/index.html":
        # Check if title already mentions Dr. Connor Robertson
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match and "Dr. Connor Robertson" not in title_match.group(1):
            old_title = title_match.group(1)
            # Add "with Dr. Connor Robertson" to title if not there
            new_title = old_title.replace(" | The Prospecting Show", " | The Prospecting Show with Dr. Connor Robertson")
            html = html.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
    
    return html

def process_all_html():
    """Find and process every HTML file."""
    count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip .git
        if '.git' in root:
            continue
        for f in files:
            if f.endswith('.html'):
                fpath = os.path.join(root, f)
                with open(fpath, 'r', encoding='utf-8') as fh:
                    html = fh.read()
                
                html = fix_canonical_urls(html, fpath)
                html = enhance_og_tags(html, fpath)
                html = strengthen_entity(html, fpath)
                html = inject_schemas(html, fpath)
                
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(html)
                count += 1
                print(f"  Processed: {fpath.replace(BASE_DIR, '')}")
    
    print(f"\nTotal HTML files processed: {count}")

# ─────────────────────────────────────────────
# ENHANCED ABOUT PAGE (add Person schema)
# ─────────────────────────────────────────────
def enhance_about_page():
    """Add comprehensive Person schema to about page."""
    about_path = os.path.join(BASE_DIR, "about", "index.html")
    with open(about_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add enhanced Person schema specific to about page
    about_person = {
        "@context": "https://schema.org",
        "@type": "AboutPage",
        "name": "About The Prospecting Show and Dr. Connor Robertson",
        "url": f"{SITE_URL}/about/",
        "mainEntity": {"@id": "https://drconnorrobertson.com/#person"},
        "description": "Learn about The Prospecting Show podcast and its host, Dr. Connor Robertson -- entrepreneur, business strategist, and podcast host based in Pittsburgh, PA."
    }
    
    script_tag = f'\n<script type="application/ld+json">\n{json.dumps(about_person, indent=2)}\n</script>'
    html = html.replace("</head>", script_tag + "\n</head>")
    
    with open(about_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Enhanced about page")

# ─────────────────────────────────────────────
# ENHANCE EXISTING EPISODE SCHEMAS
# ─────────────────────────────────────────────
def enhance_episode_schemas():
    """Upgrade existing PodcastEpisode schemas with @id references."""
    episodes_dir = os.path.join(BASE_DIR, "episodes")
    for slug in os.listdir(episodes_dir):
        ep_path = os.path.join(episodes_dir, slug, "index.html")
        if not os.path.isfile(ep_path):
            continue
        
        with open(ep_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Replace simple author objects with @id references
        html = html.replace(
            '"author": {\n        "@type": "Person",\n        "name": "Dr. Connor Robertson",\n        "url": "https://drconnorrobertson.com"\n    }',
            '"author": {"@id": "https://drconnorrobertson.com/#person"}'
        )
        
        # Enhance partOfSeries with @id
        html = html.replace(
            '"partOfSeries": {\n        "@type": "PodcastSeries",\n        "name": "The Prospecting Show with Dr. Connor Robertson",\n        "url": "https://drconnorrobertson.github.io/"\n    }',
            f'"partOfSeries": {{"@id": "{SITE_URL}/#podcast"}}'
        )
        html = html.replace(
            '"partOfSeries": {\n        "@type": "PodcastSeries",\n        "name": "The Prospecting Show with Dr. Connor Robertson",\n        "url": "' + SITE_URL + '/"\n    }',
            f'"partOfSeries": {{"@id": "{SITE_URL}/#podcast"}}'
        )
        
        with open(ep_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    print("Enhanced episode schemas")

# ─────────────────────────────────────────────
# ENHANCE EXISTING BLOG SCHEMAS
# ─────────────────────────────────────────────
def enhance_blog_schemas():
    """Upgrade existing BlogPosting schemas."""
    blog_dir = os.path.join(BASE_DIR, "blog")
    for slug in os.listdir(blog_dir):
        bp_path = os.path.join(blog_dir, slug, "index.html")
        if not os.path.isfile(bp_path):
            continue
        
        with open(bp_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Replace simple author with @id
        html = html.replace(
            '"author": {\n        "@type": "Person",\n        "name": "Dr. Connor Robertson",\n        "url": "https://drconnorrobertson.com"\n    }',
            '"author": {"@id": "https://drconnorrobertson.com/#person"}'
        )
        html = html.replace(
            '"publisher": {\n        "@type": "Organization",\n        "name": "The Prospecting Show"\n    }',
            f'"publisher": {{"@type": "Organization", "name": "The Prospecting Show", "url": "{SITE_URL}", "founder": {{"@id": "https://drconnorrobertson.com/#person"}}}}'
        )
        
        with open(bp_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    print("Enhanced blog schemas")

# ─────────────────────────────────────────────
# REPLACE HOMEPAGE PODCAST SCHEMA
# ─────────────────────────────────────────────
def replace_homepage_schema():
    """Remove old PodcastSeries schema from homepage (we inject the enhanced one)."""
    hp = os.path.join(BASE_DIR, "index.html")
    with open(hp, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove the old inline PodcastSeries schema block
    pattern = r'<script type="application/ld\+json">\s*\{[^}]*"@type":\s*"PodcastSeries"[^<]*\}</script>'
    # More careful removal
    old_block = '''<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "PodcastSeries",'''
    
    if old_block in html:
        # Find the full script block
        start = html.index(old_block)
        end = html.index('</script>', start) + len('</script>')
        html = html[:start] + html[end:]
    
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Replaced homepage schema")

if __name__ == "__main__":
    print("=== SEO Enhancement Script ===\n")
    print("1. Replacing homepage schema...")
    replace_homepage_schema()
    print("2. Enhancing episode schemas...")
    enhance_episode_schemas()
    print("3. Enhancing blog schemas...")
    enhance_blog_schemas()
    print("4. Enhancing about page...")
    enhance_about_page()
    print("5. Processing all HTML files (Person schema, breadcrumbs, OG, entity)...")
    process_all_html()
    print("\n=== Done ===")
