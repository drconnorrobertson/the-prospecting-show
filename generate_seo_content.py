#!/usr/bin/env python3
import os
import re
from datetime import datetime
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing beautifulsoup4...")
    os.system("pip install beautifulsoup4 -q")
    from bs4 import BeautifulSoup

TOPIC_CLUSTERS = {
    'cold-outreach': {
        'title': 'Cold Outreach & Prospecting',
        'intro': "Cold outreach is the foundation of modern sales. It's not about being pushy or aggressive—it's about reaching the right person at the right time with a message that resonates. On The Prospecting Show, we explore proven strategies for effective cold outreach, from email sequencing and LinkedIn messaging to phone prospecting and multi-channel campaigns. Learn how top salespeople break through the noise, build genuine connections, and turn cold prospects into warm leads. Whether you're building a sales team or scaling your personal outreach efforts, these episodes will give you the frameworks and tactics to succeed.",
        'keywords': ['cold', 'outreach', 'prospecting', 'email', 'linkedin', 'lead', 'cold outreach', 'cold calling', 'cold email']
    },
    'sales-pipeline': {
        'title': 'Sales Pipeline & Lead Management',
        'intro': "A predictable sales pipeline is the lifeblood of any growing business. In this topic cluster, we dive deep into pipeline management, lead qualification, lead nurturing, and sales process optimization. You'll learn how successful entrepreneurs and sales leaders structure their funnels, qualify prospects efficiently, and maintain healthy deal flow. From understanding the psychology of the sales cycle to implementing systems that keep deals moving, these conversations explore real-world strategies for building a repeatable, scalable sales process. Discover how to reduce churn, improve conversion rates, and create predictability in your business.",
        'keywords': ['pipeline', 'sales', 'lead', 'funnel', 'conversion', 'qualification', 'nurture', 'deal flow', 'sales process']
    },
    'ai-in-sales': {
        'title': 'AI & Technology in Sales',
        'intro': "Artificial intelligence and modern technology are revolutionizing how sales teams work. From AI-powered prospecting tools to automation platforms that handle repetitive tasks, technology is enabling salespeople to focus on high-value activities. In this cluster, we explore how AI is transforming cold outreach, lead scoring, and customer engagement. Hear from industry experts about the best tools for sales automation, how AI can improve personalization at scale, and the future of technology-enabled selling. Learn how to leverage AI without losing the human touch that builds relationships and closes deals.",
        'keywords': ['ai', 'artificial intelligence', 'automation', 'tools', 'technology', 'sales', 'automation platform', 'ai sales']
    },
    'networking': {
        'title': 'Networking & Relationship Building',
        'intro': "Your network is your net worth. Throughout The Prospecting Show, we've emphasized the power of relationships in business. This topic cluster focuses on relationship building, networking strategies, and how to develop genuine connections that lead to opportunities. Learn how to network authentically, build strategic partnerships, leverage events and conferences, and create a personal brand that attracts opportunities. Hear from entrepreneurs and leaders who've built incredible networks and discover how relationships fuel business growth, create referrals, and open doors you didn't know existed.",
        'keywords': ['network', 'relationship', 'partner', 'referral', 'connection', 'community', 'mentor', 'partnership']
    },
    'real-estate-investing': {
        'title': 'Real Estate Investing & Property',
        'intro': "Real estate is one of the most powerful wealth-building vehicles available to entrepreneurs. Whether you're interested in rental properties, commercial real estate, real estate wholesaling, or property development, this cluster covers the strategies and tactics that successful real estate investors use. Learn about deal sourcing, property analysis, financing options, and the business of real estate. Hear from investors who've built substantial portfolios and discover how real estate can diversify your income and create long-term wealth. These episodes blend sales and prospecting skills with real estate investing wisdom.",
        'keywords': ['real estate', 'property', 'investing', 'rental', 'real estate investing', 'property investment', 'real estate agent', 'wholesaling']
    },
    'entrepreneurship': {
        'title': 'Entrepreneurship & Business Building',
        'intro': "Entrepreneurship is a journey of constant learning and growth. In this comprehensive cluster, we explore what it takes to build, scale, and grow a successful business from the ground up. Topics include idea validation, business models, growth strategies, scaling operations, building teams, and the mindset required for entrepreneurial success. Listen to interviews with entrepreneurs who've built multiple companies, sold businesses, and created wealth through their ventures. Whether you're just starting out or looking to scale your existing business, these conversations will inspire and educate you.",
        'keywords': ['entrepreneur', 'entrepreneurship', 'business', 'startup', 'founder', 'business owner', 'startup founder', 'build']
    },
    'mindset': {
        'title': 'Mindset & Personal Development',
        'intro': "Success starts between your ears. Your mindset, beliefs, and mental frameworks directly impact your ability to achieve your goals. This topic cluster explores the psychology of success, overcoming limiting beliefs, building confidence, and developing the resilience required to navigate entrepreneurship. Learn from high-performing individuals about their mental strategies, how they handle failure and rejection, and what mindset shifts led to their breakthroughs. These episodes go beyond tactics and systems to address the internal game—because sustainable success requires getting your mind right first.",
        'keywords': ['mindset', 'success', 'beliefs', 'psychology', 'confidence', 'resilience', 'mental', 'personal development', 'growth']
    },
    'business-acquisitions': {
        'title': 'Business Acquisitions & Scaling Through M&A',
        'intro': "Acquiring businesses is one of the fastest ways to scale. Rather than building everything from scratch, successful entrepreneurs acquire existing companies and integrate them into their operations. This cluster explores mergers and acquisitions, business valuations, deal structures, due diligence, and integration strategies. Learn how to identify acquisition targets, negotiate deals, understand valuations, and successfully integrate acquired companies into your business. Hear from founders and operators who've grown through strategic acquisitions and discover how M&A can accelerate your business growth.",
        'keywords': ['acquisition', 'acquisitions', 'merge', 'merger', 'scale', 'business acquisition', 'deal', 'buying business']
    }
}

def extract_episode_metadata(html_content, episode_slug):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    title_text = title_tag.string if title_tag else ''
    episode_match = re.search(r'Episode (\d+):', title_text)
    episode_num = int(episode_match.group(1)) if episode_match else 0
    h1 = soup.find('h1')
    episode_title = h1.get_text(strip=True) if h1 else ''
    guest_name = ''
    if ' with ' in episode_title:
        guest_name = episode_title.split(' with ')[-1].strip()
    description = ''
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        description = meta_desc.get('content', '')
    topics = []
    topic_tags = soup.find_all('span', {'class': 'topic-tag'})
    for tag in topic_tags:
        topics.append(tag.get_text(strip=True))
    meta_bar = soup.find('div', {'class': 'meta-bar'})
    date_text = ''
    if meta_bar:
        spans = meta_bar.find_all('span')
        for span in spans:
            text = span.get_text(strip=True)
            if any(m in text for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','20']):
                date_text = text
                break
    return {'slug': episode_slug, 'number': episode_num, 'title': episode_title, 'guest': guest_name, 'description': description, 'topics': topics, 'date': date_text}

def generate_show_notes(episode_metadata):
    guest = episode_metadata['guest']
    description = episode_metadata['description']
    topics = episode_metadata['topics']
    guest_str = guest or 'our guest'
    guest_str2 = guest or 'entrepreneurs'
    guest_str3 = guest or 'Our guest'
    guest_str4 = guest or 'the guest'
    topics_str = topics[0] if topics else 'business growth'
    
    show_notes = '        <div class="content-section">\n            <h2>Full Transcript & Show Notes</h2>\n            <h3>Key Topics Discussed</h3>\n'
    show_notes += '            <p>In this episode, ' + guest_str + ' explores ' + (description.lower() if description else 'important topics for business growth and entrepreneurship') + '. Here are the key areas covered during our conversation:</p>\n'
    show_notes += '            <h3>Episode Highlights</h3>\n'
    show_notes += '            <p><strong>Building and Scaling Success:</strong> Learn how ' + guest_str2 + ' approach business challenges and opportunities. The conversation covers practical strategies that you can apply to your own business, whether you\'re just starting out or looking to scale an existing operation.</p>\n'
    show_notes += '            <p><strong>Industry Insights and Trends:</strong> ' + guest_str3 + ' shares valuable insights about the current market landscape. Understanding these trends helps you stay competitive and position your business for long-term success. From market dynamics to emerging opportunities, this episode provides a comprehensive overview of what\'s happening in the space.</p>\n'
    show_notes += '            <p><strong>Practical Tactics and Strategies:</strong> Beyond the big-picture insights, this episode digs into actionable tactics. You\'ll hear specific strategies and frameworks that have worked in real-world situations. These are the kinds of details that transform knowledge into results.</p>\n'
    show_notes += '            <p><strong>Overcoming Challenges:</strong> Every successful entrepreneur faces obstacles. In this conversation, ' + guest_str4 + ' discusses how to identify, address, and overcome common challenges in business. This part of the episode is particularly valuable because it acknowledges the reality that business building isn\'t always smooth.</p>\n'
    show_notes += '            <h3>Key Takeaways</h3>\n            <ul>\n'
    show_notes += '                <li>Practical frameworks for ' + topics_str + '</li>\n'
    show_notes += '                <li>Strategies for overcoming common business obstacles</li>\n'
    show_notes += '                <li>How to apply these lessons to your specific situation</li>\n'
    show_notes += '                <li>Resources and tools that support long-term success</li>\n'
    show_notes += '                <li>The importance of mindset and continuous learning</li>\n            </ul>\n'
    show_notes += '            <h3>About the Guest</h3>\n'
    show_notes += '            <p>' + (guest or 'This episode guest') + ' brings valuable experience and insights to The Prospecting Show. With a track record of success in their field, ' + (guest or 'they') + ' shares the kind of practical wisdom that can accelerate your business growth. The episode represents just one conversation among many on this show designed to help entrepreneurs and business owners achieve their goals.</p>\n'
    show_notes += '            <h3>How to Apply These Insights</h3>\n            <p>The real value of any podcast comes when you apply what you learn. After listening to this episode, consider:</p>\n            <ul>\n'
    show_notes += '                <li>Which specific tactic from this episode can you implement immediately?</li>\n'
    show_notes += '                <li>What\'s one challenge you\'re facing that this episode addressed?</li>\n'
    show_notes += '                <li>How can you adapt ' + (guest or 'the guest') + '\'s approach to your unique situation?</li>\n'
    show_notes += '                <li>Who on your team would benefit from hearing this conversation?</li>\n            </ul>\n'
    show_notes += '            <p>The Prospecting Show exists to help you achieve breakthrough results in your business. Every episode is designed to provide actionable insights from entrepreneurs and leaders who\'ve achieved remarkable success. Tune in weekly for new conversations that will challenge your thinking and inspire your growth.</p>\n            </div>'
    return show_notes

def generate_topic_page(topic_key, topic_data, all_episodes):
    topic_title = topic_data['title']
    intro_text = topic_data['intro']
    keywords = topic_data['keywords']
    related_episodes = []
    for ep in all_episodes:
        title = ep['title'].lower()
        description = ep['description'].lower()
        for keyword in keywords:
            if keyword.lower() in title or keyword.lower() in description:
                related_episodes.append(ep)
                break
    related_episodes.sort(key=lambda x: x['number'], reverse=True)
    related_html = ''
    if related_episodes:
        related_html = '<div class="related-episodes">'
        for ep in related_episodes[:12]:
            related_html += f'<div class="episode-card"><span class="episode-num">Episode {ep["number"]}</span><h3><a href="/episodes/{ep["slug"]}/">{ep["title"]}</a></h3><div class="episode-meta"><span>{ep["date"]}</span></div></div>'
        related_html += '</div>'
    
    schema_intro = intro_text[:160].replace('"', '').replace('\n', ' ')
    
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOPIC_TITLE | The Prospecting Show with Dr. Connor Robertson</title>
    <meta name="description" content="Explore episodes about TOPIC_TITLE_LOWER on The Prospecting Show. Learn strategies and insights from successful entrepreneurs.">
    <meta name="author" content="Dr. Connor Robertson">
    <link rel="canonical" href="https://prospectingshow.com/topics/TOPIC_KEY/">
    <meta property="og:title" content="TOPIC_TITLE | The Prospecting Show">
    <meta property="og:description" content="Explore episodes about TOPIC_TITLE_LOWER on The Prospecting Show. Learn strategies and insights from successful entrepreneurs.">
    <meta property="og:locale" content="en_US">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://prospectingshow.com/topics/TOPIC_KEY/">
    <meta property="og:site_name" content="The Prospecting Show">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="TOPIC_TITLE | The Prospecting Show">
    <meta name="twitter:description" content="Explore episodes about TOPIC_TITLE_LOWER on The Prospecting Show. Learn strategies and insights from successful entrepreneurs.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    <script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "TOPIC_TITLE",
    "description": "SCHEMA_INTRO...",
    "url": "https://prospectingshow.com/topics/TOPIC_KEY/",
    "isPartOf": {"@id": "https://prospectingshow.com/#podcast"}
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://prospectingshow.com/"},
    {"@type": "ListItem", "position": 2, "name": "Topics", "item": "https://prospectingshow.com/topics/"},
    {"@type": "ListItem", "position": 3, "name": "TOPIC_TITLE", "item": "https://prospectingshow.com/topics/TOPIC_KEY/"}
  ]
}
</script>
</head>
<body>
<nav class="nav">
    <div class="nav-inner">
        <a href="/" class="nav-brand"><span>The Prospecting Show</span></a>
        <ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/episodes/">Episodes</a></li><li><a href="/about/">About</a></li><li><a href="/host/">Host</a></li><li><a href="/guests/">Guests</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul>
        <a href="/subscribe/" class="nav-cta">Subscribe</a>
        <button class="mobile-toggle" aria-label="Menu">&#9776;</button>
    </div>
</nav>
<section class="episode-detail">
    <div class="container">
        <a href="/episodes/" class="back-link">&larr; Back to Episodes</a>
        <h1>TOPIC_TITLE</h1>
        <div class="content-section">
            <p style="color:var(--text-secondary); font-size:1.05rem; line-height:1.6;">INTRO_TEXT</p>
        </div>
        <div class="content-section" style="text-align:center; padding:40px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border);">
            <h2 style="color:var(--text-primary); margin-bottom:12px;">Explore Related Episodes</h2>
            <p style="color:var(--text-secondary); margin-bottom:20px;">Listen to episodes exploring TOPIC_TITLE_LOWER on your favorite platform.</p>
            <div class="hero-buttons" style="justify-content:center;">
                <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">Spotify</a>
                <a href="https://podcasts.apple.com/us/podcast/id1488353384" target="_blank" rel="noopener" class="btn-primary" style="background:#8B5CF6;">Apple Podcasts</a>
            </div>
        </div>
        <div class='content-section'><h2>Episodes on TOPIC_TITLE</h2>RELATED_HTML</div>
    </div>
</section>
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="/" class="nav-brand"><span>The Prospecting Show</span></a>
                <p>Every week, Dr. Connor Robertson interviews entrepreneurs and business owners about how they built, scaled, and grew their businesses.</p>
            </div>
            <div class="footer-col">
                <h4>Show</h4>
                <ul><li><a href="/episodes/">All Episodes</a></li><li><a href="/host/">Host</a></li><li><a href="/guests/">Guests</a></li><li><a href="/about/">About</a></li><li><a href="/blog/">Blog</a></li></ul>
            </div>
            <div class="footer-col">
                <h4>Listen</h4>
                <ul><li><a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener">Spotify</a></li><li><a href="https://podcasts.apple.com/us/podcast/id1488353384" target="_blank" rel="noopener">Apple Podcasts</a></li><li><a href="https://www.youtube.com/@theprospectingshow" target="_blank" rel="noopener">YouTube</a></li></ul>
            </div>
            <div class="footer-col">
                <h4>Connect</h4>
                <ul><li><a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a></li><li><a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener">Elixir Consulting Group</a></li><li><a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a></li><li><a href="/contact/">Contact Us</a></li></ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; 2026 The Prospecting Show with Dr. Connor Robertson. All rights reserved.</span>
            <span>Hosted by <a href="https://drconnorrobertson.com" target="_blank" rel="noopener">Dr. Connor Robertson</a></span>
        </div>
    </div>
</footer>
<script src="/js/main.js"></script>
</body>
</html>
'''
    
    html_content = html_template.replace('TOPIC_TITLE', topic_title)
    html_content = html_content.replace('TOPIC_TITLE_LOWER', topic_title.lower())
    html_content = html_content.replace('TOPIC_KEY', topic_key)
    html_content = html_content.replace('SCHEMA_INTRO', schema_intro)
    html_content = html_content.replace('INTRO_TEXT', intro_text)
    html_content = html_content.replace('RELATED_HTML', related_html)
    
    return html_content

def inject_show_notes_to_episode(episode_path, show_notes):
    with open(episode_path, 'r', encoding='utf-8') as f:
        content = f.read()
    footer_start = content.rfind('<footer class="footer">')
    if footer_start == -1:
        footer_start = content.rfind('</body>')
    if footer_start != -1:
        new_content = content[:footer_start] + show_notes + '\n' + content[footer_start:]
    else:
        new_content = content
    with open(episode_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def update_sitemap(repo_path):
    sitemap_path = os.path.join(repo_path, 'sitemap.xml')
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'xml')
    for topic_key in TOPIC_CLUSTERS.keys():
        topic_url = f'https://prospectingshow.com/topics/{topic_key}/'
        url_element = soup.find('loc', string=topic_url)
        if not url_element:
            new_url = soup.new_tag('url')
            loc = soup.new_tag('loc')
            loc.string = topic_url
            new_url.append(loc)
            changefreq = soup.new_tag('changefreq')
            changefreq.string = 'monthly'
            new_url.append(changefreq)
            priority = soup.new_tag('priority')
            priority.string = '0.8'
            new_url.append(priority)
            lastmod = soup.new_tag('lastmod')
            lastmod.string = datetime.now().strftime('%Y-%m-%d')
            new_url.append(lastmod)
            soup.find('urlset').append(new_url)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

def main():
    repo_path = '/tmp/prospecting-work'
    episodes_path = os.path.join(repo_path, 'episodes')
    topics_path = os.path.join(repo_path, 'topics')
    os.makedirs(topics_path, exist_ok=True)
    print("Scanning episodes...")
    all_episodes = []
    for episode_dir in sorted(os.listdir(episodes_path)):
        episode_full_path = os.path.join(episodes_path, episode_dir)
        if not os.path.isdir(episode_full_path) or episode_dir == '__pycache__' or episode_dir == 'index.html':
            continue
        index_path = os.path.join(episode_full_path, 'index.html')
        if not os.path.exists(index_path):
            continue
        print(f"  {episode_dir}")
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        metadata = extract_episode_metadata(html_content, episode_dir)
        all_episodes.append(metadata)
        if 'Full Transcript & Show Notes' not in html_content:
            show_notes = generate_show_notes(metadata)
            inject_show_notes_to_episode(index_path, show_notes)
        else:
            print(f"    (show notes exist)")
    print(f"\nProcessed {len(all_episodes)} episodes")
    print("\nCreating topic cluster pages...")
    for topic_key, topic_data in TOPIC_CLUSTERS.items():
        print(f"  {topic_key}")
        topic_dir = os.path.join(topics_path, topic_key)
        os.makedirs(topic_dir, exist_ok=True)
        topic_page = generate_topic_page(topic_key, topic_data, all_episodes)
        index_path = os.path.join(topic_dir, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(topic_page)
    print("\nUpdating sitemap...")
    update_sitemap(repo_path)
    print("\nCompleted!")
    print(f"  - Added show notes to episodes")
    print(f"  - Created {len(TOPIC_CLUSTERS)} topic cluster pages")
    print("  - Updated sitemap.xml with topic URLs")

if __name__ == '__main__':
    main()
