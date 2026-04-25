#!/usr/bin/env python3
"""
Creates the /host/ page and 6 new blog posts for The Prospecting Show.
"""
import os, json

SITE_URL = "https://the-prospecting-show.vercel.app"
BASE_DIR = "/tmp/the-prospecting-show"

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
    "address": {"@type": "PostalAddress", "addressLocality": "Pittsburgh", "addressRegion": "PA", "addressCountry": "US"},
    "worksFor": [
        {"@type": "Organization", "name": "The Prospecting Show", "url": SITE_URL},
        {"@type": "Organization", "name": "Elixir Consulting Group", "url": "https://elixirconsultinggroup.com"}
    ]
}

NAV = '''<nav class="nav">
    <div class="nav-inner">
        <a href="/" class="nav-brand"><span>The Prospecting Show</span></a>
        <ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/episodes/">Episodes</a></li><li><a href="/about/">About</a></li><li><a href="/host/">Host</a></li><li><a href="/guests/">Guests</a></li><li><a href="/blog/">Blog</a></li><li><a href="/contact/">Contact</a></li></ul>
        <a href="/subscribe/" class="nav-cta">Subscribe</a>
        <button class="mobile-toggle" aria-label="Menu">&#9776;</button>
    </div>
</nav>'''

FOOTER = '''<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="/" class="nav-brand"><span>The Prospecting Show</span></a>
                <p>Every week, Dr. Connor Robertson interviews entrepreneurs and business owners about how they built, scaled, and grew their businesses.</p>
            </div>
            <div class="footer-col">
                <h4>Show</h4>
                <ul><li><a href="/episodes/">All Episodes</a></li><li><a href="/guests/">Guests</a></li><li><a href="/about/">About</a></li><li><a href="/host/">Meet the Host</a></li><li><a href="/blog/">Blog</a></li></ul>
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
<script src="/js/main.js"></script>'''

def make_page(title, meta_desc, canonical, og_type, breadcrumbs, extra_schemas, body_content):
    bc_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(breadcrumbs)]
    }
    schemas = [PERSON_SCHEMA, bc_schema] + extra_schemas
    schema_tags = "\n".join([f'<script type="application/ld+json">\n{json.dumps(s, indent=2)}\n</script>' for s in schemas])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="author" content="Dr. Connor Robertson">
    <link rel="canonical" href="{canonical}">
    <meta property="og:locale" content="en_US">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="The Prospecting Show">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{meta_desc}">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    {schema_tags}
</head>
<body>
{NAV}
{body_content}
{FOOTER}
</body>
</html>'''

# ─────────────────────────────────────────────
# HOST PAGE
# ─────────────────────────────────────────────
def create_host_page():
    os.makedirs(os.path.join(BASE_DIR, "host"), exist_ok=True)
    
    profile_page_schema = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "name": "Dr. Connor Robertson - Host of The Prospecting Show",
        "url": f"{SITE_URL}/host/",
        "mainEntity": {"@id": "https://drconnorrobertson.com/#person"},
        "description": "Dr. Connor Robertson is the host of The Prospecting Show podcast. Entrepreneur, business strategist, and thought leader based in Pittsburgh, PA."
    }
    
    body = '''
<section class="section" style="padding-top:120px;">
    <div class="container">
        <div class="about-hero">
            <div class="about-content">
                <h1 class="section-title">Dr. Connor Robertson</h1>
                <p style="font-size:1.2rem; color:var(--accent-light); margin-bottom:20px; font-weight:600;">Host of The Prospecting Show | Entrepreneur | Business Strategist</p>
                <p>Dr. Connor Robertson is the creator and host of The Prospecting Show, one of the leading podcasts for entrepreneurs, sales professionals, and business owners looking to scale. Based in Pittsburgh, PA, Connor has spent years building businesses, interviewing the sharpest minds in sales and entrepreneurship, and helping others do the same.</p>
                <p>With over 178 episodes and counting, The Prospecting Show has become a go-to resource for anyone looking to master the art of prospecting, close more deals, and build a sustainable business.</p>
            </div>
            <div style="text-align:center;">
                <div style="width:300px; height:300px; border-radius:20px; background:var(--gradient-1); display:flex; align-items:center; justify-content:center; margin:0 auto;">
                    <span style="font-size:4rem; color:#fff; font-weight:800;">CR</span>
                </div>
            </div>
        </div>

        <div class="content-section" style="margin:60px 0;">
            <h2>About Dr. Connor Robertson</h2>
            <p>Dr. Connor Robertson is a Pittsburgh-based entrepreneur, podcast host, and business strategist who has spent his career at the intersection of sales, business development, and entrepreneurship. As the founder and host of The Prospecting Show, Connor brings a unique combination of academic rigor and real-world business experience to every conversation.</p>
            <p>Connor launched The Prospecting Show to create a platform where entrepreneurs could share the unfiltered truth about building businesses. The show covers everything from cold outreach and lead generation to scaling operations, hiring teams, and navigating the challenges of entrepreneurship. Each episode features a different guest who has built something remarkable, and Connor draws out the specific strategies and frameworks that listeners can immediately apply.</p>
            <p>Beyond podcasting, Dr. Connor Robertson is the founder of <a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener">Elixir Consulting Group</a>, where he helps businesses develop growth strategies rooted in data-driven prospecting and sales optimization. He is also a contributor to <a href="https://thepittsburghwire.com" target="_blank" rel="noopener">The Pittsburgh Wire</a>, covering business news and development in the Pittsburgh region.</p>
        </div>

        <div class="content-section" style="margin:60px 0;">
            <h2>What Dr. Connor Robertson Covers on The Prospecting Show</h2>
            <div class="values-grid">
                <div class="value-card">
                    <div class="icon">&#128200;</div>
                    <h3>Sales and Prospecting</h3>
                    <p>Dr. Connor Robertson interviews top sales professionals about cold outreach, pipeline building, closing strategies, and modern prospecting techniques that actually work in B2B and B2C environments.</p>
                </div>
                <div class="value-card">
                    <div class="icon">&#127793;</div>
                    <h3>Entrepreneurship and Startups</h3>
                    <p>Connor digs into the stories behind successful startups and small businesses, covering everything from finding product-market fit to raising capital and building teams.</p>
                </div>
                <div class="value-card">
                    <div class="icon">&#9881;</div>
                    <h3>Business Systems and Automation</h3>
                    <p>Guests share how they have built repeatable systems, SOPs, and automations that allow businesses to scale without burning out the founder.</p>
                </div>
                <div class="value-card">
                    <div class="icon">&#128640;</div>
                    <h3>Digital Marketing and SEO</h3>
                    <p>Dr. Connor Robertson explores content marketing, search engine optimization, social media strategy, and paid advertising with marketing experts.</p>
                </div>
                <div class="value-card">
                    <div class="icon">&#127968;</div>
                    <h3>Real Estate and Investing</h3>
                    <p>The show features real estate investors and financial strategists who share how they build wealth through property investment and alternative assets.</p>
                </div>
                <div class="value-card">
                    <div class="icon">&#128101;</div>
                    <h3>Leadership and Mindset</h3>
                    <p>Connor covers the mental frameworks, leadership principles, and personal development strategies that separate good entrepreneurs from great ones.</p>
                </div>
            </div>
        </div>

        <div class="content-section" style="margin:60px 0;">
            <h2>Connect with Dr. Connor Robertson</h2>
            <div style="display:flex; flex-wrap:wrap; gap:16px; margin-top:20px;">
                <a href="https://drconnorrobertson.com" target="_blank" rel="noopener" class="btn-primary">drconnorrobertson.com</a>
                <a href="https://elixirconsultinggroup.com" target="_blank" rel="noopener" class="btn-secondary">Elixir Consulting Group</a>
                <a href="https://thepittsburghwire.com" target="_blank" rel="noopener" class="btn-secondary">The Pittsburgh Wire</a>
                <a href="https://www.linkedin.com/in/drconnorrobertson/" target="_blank" rel="noopener" class="btn-secondary">LinkedIn</a>
            </div>
        </div>

        <div style="margin-top:40px; padding:32px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border); text-align:center;">
            <h3 style="margin-bottom:8px;">Listen to The Prospecting Show</h3>
            <p style="color:var(--text-secondary); margin-bottom:16px;">New episodes every week. Available on all major podcast platforms.</p>
            <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">&#9654; Listen on Spotify</a>
        </div>
    </div>
</section>'''
    
    html = make_page(
        title="Dr. Connor Robertson - Host of The Prospecting Show | Entrepreneur & Business Strategist",
        meta_desc="Dr. Connor Robertson is the host of The Prospecting Show podcast. Pittsburgh-based entrepreneur, business strategist, and founder of Elixir Consulting Group. 178+ episodes interviewing top entrepreneurs about sales, prospecting, and business growth.",
        canonical=f"{SITE_URL}/host/",
        og_type="profile",
        breadcrumbs=[("Home", f"{SITE_URL}/"), ("Host", f"{SITE_URL}/host/")],
        extra_schemas=[profile_page_schema],
        body_content=body
    )
    
    with open(os.path.join(BASE_DIR, "host", "index.html"), "w") as f:
        f.write(html)
    print("Created /host/ page")

# ─────────────────────────────────────────────
# NEW BLOG POSTS
# ─────────────────────────────────────────────
BLOG_POSTS = [
    {
        "slug": "cold-outreach-strategies-that-actually-work",
        "title": "Cold Outreach Strategies That Actually Work in 2026",
        "meta_title": "Cold Outreach Strategies That Actually Work in 2026 | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson breaks down the cold outreach strategies that are generating real results in 2026. From email to LinkedIn to phone, learn what top performers do differently.",
        "date": "2026-04-20",
        "read_time": "9 min read",
        "content": """
<h2>Why Most Cold Outreach Fails</h2>
<p>After interviewing over 178 entrepreneurs on The Prospecting Show, one pattern stands out clearly: the businesses that grow fastest are the ones that master outbound prospecting. But here is the uncomfortable truth that Dr. Connor Robertson has observed across hundreds of conversations -- most cold outreach is terrible, and the people sending it know it.</p>
<p>The problem is not cold outreach itself. The problem is that most salespeople treat it as a numbers game without doing the work to make each touchpoint relevant. In a world where every decision-maker gets dozens of cold messages daily, generic outreach does not just fail -- it actively damages your brand.</p>

<h2>The Framework Dr. Connor Robertson Uses</h2>
<p>Through years of interviewing top sales performers on The Prospecting Show, a clear framework has emerged. The best outreach follows what Connor calls the RTP method: Research, Trigger, Personalize.</p>
<p><strong>Research</strong> means going beyond the prospect's LinkedIn headline. Read their recent posts. Look at their company's latest press releases. Understand what problems they are likely facing right now. Stefan Smulders of Expandi, who appeared on Episode 163 of The Prospecting Show, emphasized that the best LinkedIn outreach starts with 30 minutes of research before a single message is sent.</p>
<p><strong>Trigger</strong> means finding a specific event or signal that makes your outreach timely. A new hire, a funding round, a product launch, a job posting -- these are all triggers that give you a reason to reach out right now rather than some arbitrary Tuesday.</p>
<p><strong>Personalize</strong> means going beyond "Hey [First Name]." It means referencing something specific about their situation that shows you did the work. Zach Thomas of Compound Marketing, who joined The Prospecting Show on Episode 158, shared that his team generates 5+ appointments per week on LinkedIn by writing messages that could only be sent to that specific person.</p>

<h2>Email Outreach in 2026</h2>
<p>Email remains the most scalable outreach channel, but deliverability has become the real battleground. If your emails are landing in spam, nothing else matters. Joel Stevenson from Yesware discussed this extensively on Episode 170 of The Prospecting Show -- tools that track opens, clicks, and replies give you the data to optimize your sequences over time.</p>
<p>The winning formula for cold email in 2026 is short, specific, and value-first. Your first email should be under 100 words. It should reference something specific about the prospect. And it should offer genuine value, not just a pitch for your product.</p>

<h2>LinkedIn Outreach That Generates Meetings</h2>
<p>LinkedIn has become the dominant channel for B2B prospecting, and Dr. Connor Robertson has covered it extensively on The Prospecting Show. The key insight from guests like Stefan Smulders and Zach Thomas is that connection requests alone are not enough -- you need a full engagement strategy.</p>
<p>This means engaging with your prospects' content before reaching out. Comment on their posts. Share their articles. Build familiarity before sending that first message. When you do reach out, reference a specific piece of content they shared and tie it to how you can help.</p>

<h2>Phone Outreach Is Not Dead</h2>
<p>Despite what you may have heard, cold calling still works. It works best when combined with email and LinkedIn in a multi-channel sequence. The key is to use the phone as a follow-up to digital touches, not as the first point of contact.</p>
<p>As Dr. Connor Robertson often tells guests on The Prospecting Show, the phone is the fastest path to a real conversation -- and real conversations are where deals happen.</p>

<h2>Building Your Outreach System</h2>
<p>The best outreach is systematic, not sporadic. Set a daily target for new prospects added, messages sent, and follow-ups completed. Track your conversion rates at each stage. Double down on what works and cut what does not.</p>
<p>For more strategies on building a scalable outreach system, listen to The Prospecting Show on <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener">Spotify</a> or <a href="https://podcasts.apple.com/us/podcast/id1488353384" target="_blank" rel="noopener">Apple Podcasts</a>.</p>
""",
        "related": [
            ("/episodes/the-perfect-linkedin-machine-with-zach-thomas/", "Episode 158: The Perfect LinkedIn Machine with Zach Thomas"),
            ("/episodes/linkedin-2022-with-stefan-smulders-of-expandi/", "Episode 163: LinkedIn 2022 with Stefan Smulders of Expandi"),
            ("/episodes/sales-enablement-with-yesware-joel-stevenson/", "Episode 170: Sales Enablement with YESWARE - Joel Stevenson"),
        ]
    },
    {
        "slug": "building-a-predictable-sales-pipeline",
        "title": "How to Build a Predictable Sales Pipeline from Scratch",
        "meta_title": "How to Build a Predictable Sales Pipeline from Scratch | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson shares the step-by-step framework for building a sales pipeline that generates consistent, predictable revenue. Based on insights from 178+ Prospecting Show episodes.",
        "date": "2026-04-12",
        "read_time": "10 min read",
        "content": """
<h2>The Pipeline Problem Most Businesses Face</h2>
<p>Dr. Connor Robertson has talked to hundreds of entrepreneurs on The Prospecting Show, and the number one challenge they cite is inconsistent revenue. Months where deals close are followed by months of drought. The root cause is almost always the same: no system for generating pipeline.</p>
<p>A predictable sales pipeline is not about luck or timing. It is about building a machine that produces qualified conversations on a reliable schedule. And that machine has specific components that anyone can build.</p>

<h2>Define Your Ideal Customer Profile</h2>
<p>Before you build any outreach system, you need absolute clarity on who you are targeting. Dr. Connor Robertson sees this mistake constantly -- businesses that try to sell to everyone end up selling to no one. Your Ideal Customer Profile (ICP) should be specific enough that you could describe your best customer to a stranger in 30 seconds.</p>
<p>Consider industry, company size, revenue range, geography, technology stack, and the specific pain points your solution addresses. The tighter your ICP, the higher your conversion rates will be at every stage of the pipeline.</p>

<h2>Build Your Prospecting List</h2>
<p>With your ICP defined, the next step is building a targeted list of companies and contacts. Tools like LinkedIn Sales Navigator, Apollo, and ZoomInfo make this easier than ever. But the list itself is only as good as the research behind it.</p>
<p>Ravi Abuvala, who appeared on Episode 156 of The Prospecting Show, shared how he scaled his agency by building hyper-targeted lists and running systematic outreach campaigns. The key was combining automated list building with manual verification to ensure quality.</p>

<h2>Design Your Outreach Sequence</h2>
<p>A single touchpoint is not a strategy. Dr. Connor Robertson recommends building multi-channel sequences that combine email, LinkedIn, and phone across a 3 to 4 week window. Each touchpoint should add value and build on the previous one.</p>
<p>A strong sequence typically includes 7 to 10 touches: an initial email, a LinkedIn connection, a follow-up email with a piece of content, a phone call, and additional follow-ups that reference different angles of your value proposition.</p>

<h2>Qualify Ruthlessly</h2>
<p>Not every response is a good lead. Dr. Connor Robertson emphasizes on The Prospecting Show that qualification is where most salespeople waste the most time. Use a simple framework like BANT (Budget, Authority, Need, Timeline) or MEDDIC to determine whether a prospect is worth your time.</p>
<p>The goal is to fill your calendar with conversations that have a reasonable chance of turning into revenue. One qualified meeting is worth more than ten unqualified ones.</p>

<h2>Track, Measure, Optimize</h2>
<p>A predictable pipeline requires predictable metrics. Track your connection rate, response rate, meeting rate, and close rate. Know how many prospects you need to contact to generate one new customer, and then reverse-engineer your daily activity targets from there.</p>
<p>Peter Velardi of ReferMeIQ discussed this on Episode 168 of The Prospecting Show -- the businesses that grow fastest are the ones that treat their pipeline like a science experiment, constantly testing and optimizing.</p>

<h2>Make It a Daily Habit</h2>
<p>The most important piece of advice Dr. Connor Robertson gives on The Prospecting Show is this: prospecting must be a daily habit, not an occasional activity. Block time on your calendar every day for outreach. Protect that time like you would a meeting with your biggest client.</p>
<p>Consistency is what separates businesses with predictable revenue from businesses that live deal to deal.</p>
""",
        "related": [
            ("/episodes/scaling-using-systems-with-ravi-abuvala/", "Episode 156: Scaling Using Systems with Ravi Abuvala"),
            ("/episodes/scaling-your-referrals-with-peter-velardi-and-refermeiq/", "Episode 168: Scaling Your Referrals with Peter Velardi and ReferMeIQ"),
            ("/episodes/high-ticket-sales-with-kelsey-oneal/", "Episode 93: High Ticket Sales with Kelsey Oneal"),
        ]
    },
    {
        "slug": "ai-tools-transforming-sales-prospecting",
        "title": "How AI Is Transforming Sales Prospecting in 2026",
        "meta_title": "How AI Is Transforming Sales Prospecting in 2026 | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson explores how artificial intelligence is reshaping sales prospecting, from AI-powered lead scoring to automated personalization and predictive analytics.",
        "date": "2026-04-05",
        "read_time": "8 min read",
        "content": """
<h2>The AI Revolution in Sales</h2>
<p>Artificial intelligence is fundamentally changing how sales teams prospect, qualify, and close deals. As Dr. Connor Robertson has discussed with dozens of guests on The Prospecting Show, the companies that adopt AI tools early are gaining a significant competitive advantage over those that do not.</p>
<p>But AI in sales is not about replacing human connection. It is about amplifying it. The best AI tools handle the repetitive, data-heavy tasks so that salespeople can focus on what they do best: building relationships and solving problems.</p>

<h2>AI-Powered Lead Scoring</h2>
<p>Traditional lead scoring relies on static criteria -- job title, company size, industry. AI-powered lead scoring goes further by analyzing behavioral signals, engagement patterns, and historical data to predict which prospects are most likely to convert.</p>
<p>Dr. Connor Robertson has seen guests on The Prospecting Show implement AI lead scoring and cut their sales cycle in half. Instead of working a list from top to bottom, sales reps can focus their energy on the prospects that are statistically most likely to buy.</p>

<h2>Automated Research and Personalization</h2>
<p>One of the biggest bottlenecks in prospecting is research. AI tools can now scan a prospect's LinkedIn activity, company news, job postings, and tech stack in seconds, then generate personalized talking points for each outreach message.</p>
<p>This is not about sending AI-generated spam. It is about using AI to do the research that used to take 30 minutes per prospect in under 30 seconds, so your team can send thoughtful, personalized outreach at scale.</p>

<h2>Predictive Analytics for Pipeline Management</h2>
<p>AI can analyze your historical deal data to predict which opportunities are likely to close, which are at risk, and where your pipeline has gaps. This gives sales leaders real-time visibility into their revenue forecast and allows them to make data-driven decisions about where to allocate resources.</p>
<p>As Dr. Connor Robertson has noted on The Prospecting Show, the companies that will win in the next decade are the ones that combine human intuition with machine intelligence. AI does not replace the salesperson -- it makes them smarter and faster.</p>

<h2>Conversational AI and Chatbots</h2>
<p>Conversational AI has evolved beyond basic chatbots. Modern AI assistants can qualify leads, schedule meetings, and answer product questions 24/7. For businesses that generate inbound leads, this means no prospect goes unattended even outside business hours.</p>

<h2>What This Means for Sales Professionals</h2>
<p>Dr. Connor Robertson's advice to listeners of The Prospecting Show is clear: learn to work with AI, not against it. The sales professionals who will thrive are the ones who use AI to handle the grind work while they focus on high-value activities like discovery calls, demos, and relationship building.</p>
<p>The future of sales is not AI or human. It is AI and human, working together to create better outcomes for everyone involved.</p>
""",
        "related": [
            ("/episodes/seo-content-built-fast-with-market-muse/", "Episode 167: SEO Content Built FAST with Market Muse"),
            ("/episodes/sales-enablement-with-yesware-joel-stevenson/", "Episode 170: Sales Enablement with YESWARE - Joel Stevenson"),
            ("/episodes/digital-marketing-with-rj-huebert/", "Episode: Digital Marketing with RJ Huebert"),
        ]
    },
    {
        "slug": "networking-strategies-for-entrepreneurs-in-pittsburgh",
        "title": "Networking Strategies for Entrepreneurs in Pittsburgh",
        "meta_title": "Networking Strategies for Entrepreneurs in Pittsburgh | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson shares proven networking strategies for entrepreneurs in Pittsburgh. From local events to digital communities, learn how Pittsburgh business owners build valuable connections.",
        "date": "2026-03-28",
        "read_time": "7 min read",
        "content": """
<h2>Pittsburgh Is a City Built on Connections</h2>
<p>As a Pittsburgh-based entrepreneur and host of The Prospecting Show, Dr. Connor Robertson has seen firsthand how this city's tight-knit business community creates unique opportunities for networking. Pittsburgh has a culture of collaboration that you do not find in larger cities -- people here genuinely want to help each other succeed.</p>
<p>But networking effectively requires more than just showing up at events. It requires a strategy, consistent follow-up, and a genuine willingness to give before you ask.</p>

<h2>The Pittsburgh Networking Advantage</h2>
<p>Pittsburgh's business community is large enough to offer real opportunities but small enough that relationships matter. Dr. Connor Robertson has found that in Pittsburgh, you are typically only one or two introductions away from anyone you want to meet. That is a powerful advantage for entrepreneurs who are willing to invest in relationships.</p>
<p>The city's strong base of universities, healthcare systems, tech startups, and established companies creates a diverse ecosystem where entrepreneurs can find partners, customers, and mentors across multiple industries.</p>

<h2>Where to Network in Pittsburgh</h2>
<p>Pittsburgh offers a strong calendar of business events, meetups, and professional organizations. Organizations like the Pittsburgh Technology Council, Ascender, and the various chambers of commerce host regular events that attract serious business people.</p>
<p>But some of the best networking in Pittsburgh happens informally -- at coffee shops in Lawrenceville, co-working spaces in the Strip District, and industry events at venues across the city. Dr. Connor Robertson recommends attending at least two to three events per month to maintain visibility and build momentum.</p>

<h2>Digital Networking for Pittsburgh Entrepreneurs</h2>
<p>LinkedIn is essential for Pittsburgh entrepreneurs. The city has an active LinkedIn community, and Dr. Connor Robertson has found that connecting with other Pittsburgh professionals on the platform leads to real in-person meetings more often than in most markets.</p>
<p>Podcasting is another powerful networking tool -- as Connor has discovered through The Prospecting Show, inviting someone to be a guest on your podcast is one of the best ways to build a relationship with someone you admire.</p>

<h2>The Follow-Up Framework</h2>
<p>Networking without follow-up is a waste of time. Dr. Connor Robertson recommends following up within 24 hours of meeting someone new. Send a personalized LinkedIn connection request, reference something specific from your conversation, and suggest a specific next step.</p>
<p>The entrepreneurs who win at networking are not the ones who collect the most business cards. They are the ones who build the deepest relationships with a smaller number of the right people.</p>

<h2>Give First, Ask Later</h2>
<p>The most effective networkers in Pittsburgh are the ones who lead with generosity. Make introductions. Share resources. Offer help without expecting anything in return. This approach builds trust and creates a network that naturally generates opportunities over time.</p>
<p>Dr. Connor Robertson covers networking and relationship building extensively on The Prospecting Show. For more insights, subscribe on <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener">Spotify</a>.</p>
""",
        "related": [
            ("/episodes/scaling-your-referrals-with-peter-velardi-and-refermeiq/", "Episode 168: Scaling Your Referrals with Peter Velardi and ReferMeIQ"),
            ("/episodes/digital-business-cards-with-pieter-limburg/", "Episode 172: Digital Business Cards with Pieter Limburg"),
            ("/episodes/growing-your-consulting-business-with-mark-firth/", "Episode 156: Growing Your Consulting Business with Mark Firth"),
        ]
    },
    {
        "slug": "the-prospecting-mindset-how-top-sellers-think",
        "title": "The Prospecting Mindset: How Top Sellers Think Differently",
        "meta_title": "The Prospecting Mindset: How Top Sellers Think Differently | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson reveals the mental frameworks that separate top sales performers from the rest. Based on patterns from 178+ interviews on The Prospecting Show.",
        "date": "2026-03-20",
        "read_time": "8 min read",
        "content": """
<h2>Mindset Is the Multiplier</h2>
<p>After 178+ episodes of The Prospecting Show, Dr. Connor Robertson has identified a pattern that shows up in virtually every top performer: it starts with mindset. The tools, tactics, and techniques matter, but the mental framework behind them is what makes the difference between average and exceptional.</p>
<p>The best salespeople do not see prospecting as a necessary evil. They see it as the most important activity in their business. That shift in perspective changes everything -- how they prepare, how they show up, and how they handle rejection.</p>

<h2>Embrace Rejection as Data</h2>
<p>Every guest on The Prospecting Show who has built a significant sales career has one thing in common: they have been rejected thousands of times. The difference is how they process rejection. Top performers treat a "no" as data, not as a personal verdict.</p>
<p>Dr. Connor Robertson encourages listeners to track their rejection rate the same way they track their close rate. If you are not getting enough rejections, you are not prospecting enough. Rejection is simply the cost of doing business in sales.</p>

<h2>Activity Over Outcome</h2>
<p>The best prospectors focus on activity metrics, not outcome metrics. You cannot control whether a prospect says yes. You can control how many prospects you contact, how many follow-ups you send, and how many conversations you have.</p>
<p>Dr. Terri Levine shared this exact philosophy on Episode 155 of The Prospecting Show -- the key to her success was setting daily activity targets and hitting them regardless of the results. Over time, the results take care of themselves.</p>

<h2>Curiosity Over Persuasion</h2>
<p>Top sellers approach prospecting with genuine curiosity about their prospects' problems. They are not trying to convince anyone of anything. They are trying to understand whether they can help. This subtle shift makes every conversation more natural and productive.</p>
<p>Eli Wilde, who joined The Prospecting Show on Episode 171, talked about how selling for Tony Robbins taught him that the best sales conversations feel like coaching sessions, not pitches. When you are genuinely curious about someone's situation, they naturally want to keep talking.</p>

<h2>Long-Term Thinking</h2>
<p>Average salespeople think in terms of this month's quota. Top performers think in terms of this year's relationship portfolio. Dr. Connor Robertson has seen this pattern repeatedly on The Prospecting Show -- the guests who build the biggest businesses are the ones who play long games with long people.</p>
<p>Not every prospect is ready to buy today. But the one who gets your thoughtful follow-up in six months, when they are ready, will remember you. The prospecting mindset is about planting seeds, not just harvesting crops.</p>

<h2>Continuous Learning</h2>
<p>The best salespeople are obsessive learners. They read, listen to podcasts like The Prospecting Show, attend workshops, and constantly refine their approach. Dr. Connor Robertson believes that the moment you stop learning is the moment your competition starts passing you.</p>
<p>Commit to learning one new prospecting technique per month. Test it for 30 days. Keep what works. Discard what does not. Over time, you will build a prospecting system that is uniquely suited to your strengths and your market.</p>
""",
        "related": [
            ("/episodes/why-you-need-a-mentor-with-dr-terri-levine/", "Episode 155: Why You Need a Mentor with Dr. Terri Levine"),
            ("/episodes/sales-communication-and-scaling-with-eli-wilde/", "Episode 171: Sales, Communication and Scaling with Eli Wilde"),
            ("/episodes/finding-your-purpose-with-steph-shinabery/", "Episode 157: Finding Your Purpose with Steph Shinabery"),
        ]
    },
    {
        "slug": "lessons-from-178-entrepreneur-interviews",
        "title": "10 Lessons from Interviewing 178 Entrepreneurs on The Prospecting Show",
        "meta_title": "10 Lessons from 178 Entrepreneur Interviews | Dr. Connor Robertson",
        "description": "Dr. Connor Robertson distills the most important lessons from 178+ interviews with entrepreneurs on The Prospecting Show. The patterns, principles, and strategies that separate successful businesses from the rest.",
        "date": "2026-03-10",
        "read_time": "11 min read",
        "content": """
<h2>Patterns from 178 Conversations</h2>
<p>Over the course of 178+ episodes of The Prospecting Show, Dr. Connor Robertson has had a front-row seat to the strategies, failures, and breakthroughs of entrepreneurs across every industry. While every business is different, certain patterns keep showing up. These are the 10 most important lessons from those conversations.</p>

<h2>1. Revenue Solves Most Problems</h2>
<p>Every guest on The Prospecting Show who has built a successful business started by solving the revenue problem first. Before you optimize your website, build your brand, or hire a team, figure out how to generate consistent income. Everything else follows.</p>

<h2>2. Systems Beat Hustle</h2>
<p>Hustle gets you started. Systems get you to scale. Dr. Connor Robertson has seen this lesson play out hundreds of times. Ron Medlin discussed this on Episode 164 -- Go High Level and similar tools let small businesses build marketing systems that work while they sleep. Franbeau Beduya covered it on Episode 116 with SOPs that allowed her agency to scale without her being in every meeting.</p>

<h2>3. Your Network Is Your Net Worth</h2>
<p>Networking came up in nearly every episode of The Prospecting Show. Peter Velardi built ReferMeIQ specifically to systematize referral networking because he saw how powerful it was. The entrepreneurs who build the strongest networks build the strongest businesses.</p>

<h2>4. Specialize or Die</h2>
<p>The guests who struggled most were the ones who tried to be everything to everyone. The ones who thrived picked a niche and owned it. Dr. Connor Robertson recommends going narrow before going wide -- it is easier to dominate a small market than to compete in a large one.</p>

<h2>5. Sell Before You Build</h2>
<p>Multiple guests on The Prospecting Show validated their business ideas by selling the product before it existed. This is counterintuitive but incredibly effective. If you can get someone to pay for something you have not built yet, you know you have a real business.</p>

<h2>6. Hire Slowly, Fire Quickly</h2>
<p>Hiring mistakes are the most expensive mistakes a small business can make. Dr. Connor Robertson has heard this lesson echoed by guests who scaled to seven and eight figures -- take your time finding the right people, but do not hesitate to make changes when someone is not working out.</p>

<h2>7. Content Is the Long Game</h2>
<p>Podcasting, blogging, LinkedIn posting -- the guests on The Prospecting Show who invest in content consistently build the most durable businesses. Content builds trust, generates inbound leads, and establishes authority in your market. But it takes time. Salik Muhammed covered this on Episode 100, and Market Muse reinforced it on Episode 167.</p>

<h2>8. Cash Flow Is King</h2>
<p>Revenue is vanity, profit is sanity, cash flow is reality. Dr. Connor Robertson has interviewed business owners who did millions in revenue but could not make payroll. The lesson is clear: understand your cash conversion cycle and manage it ruthlessly.</p>

<h2>9. Invest in Yourself</h2>
<p>Every successful entrepreneur Dr. Connor Robertson has interviewed invests heavily in their own education, coaching, and personal development. Dr. Terri Levine, Ben Nader, and dozens of other guests emphasized this -- the return on investing in yourself is the highest return available.</p>

<h2>10. Start Before You Are Ready</h2>
<p>The final lesson from 178 episodes of The Prospecting Show is the simplest: just start. Every guest was once exactly where you are now -- uncertain, under-resourced, and a little scared. They started anyway. And that made all the difference.</p>

<p style="margin-top:32px;">For more stories and strategies from top entrepreneurs, subscribe to The Prospecting Show on <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener">Spotify</a> or <a href="https://podcasts.apple.com/us/podcast/id1488353384" target="_blank" rel="noopener">Apple Podcasts</a>.</p>
""",
        "related": [
            ("/episodes/creating-building-scaling-and-selling-a-company-with-andrew-kroeze/", "Episode 160: Creating, Building, Scaling and Selling a Company with Andrew Kroeze"),
            ("/episodes/scaling-using-systems-with-ravi-abuvala/", "Episode: Scaling Using Systems with Ravi Abuvala"),
            ("/episodes/why-you-need-a-mentor-with-dr-terri-levine/", "Episode 155: Why You Need a Mentor with Dr. Terri Levine"),
        ]
    },
]

def create_blog_posts():
    for post in BLOG_POSTS:
        slug = post["slug"]
        os.makedirs(os.path.join(BASE_DIR, "blog", slug), exist_ok=True)
        
        blog_schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post["title"],
            "description": post["description"],
            "datePublished": post["date"],
            "dateModified": post["date"],
            "author": {"@id": "https://drconnorrobertson.com/#person"},
            "publisher": {
                "@type": "Organization",
                "name": "The Prospecting Show",
                "url": SITE_URL,
                "founder": {"@id": "https://drconnorrobertson.com/#person"}
            },
            "mainEntityOfPage": f"{SITE_URL}/blog/{slug}/",
            "keywords": "prospecting, sales, Dr. Connor Robertson, The Prospecting Show, business development, entrepreneurship"
        }
        
        related_html = ""
        if post.get("related"):
            related_items = "".join([f'<li><a href="{url}">{name}</a></li>' for url, name in post["related"]])
            related_html = f"<div class='content-section' style='margin-top:40px;'><h2>Related Episodes</h2><ul>{related_items}</ul></div>"
        
        body = f'''
<section class="blog-detail">
    <div class="container">
        <a href="/blog/" class="back-link">&larr; Back to Blog</a>
        <article>
            <header style="margin-bottom:32px;">
                <h1>{post["title"]}</h1>
                <div class="meta-bar">
                    <span>By <a href="/host/"><strong>Dr. Connor Robertson</strong></a></span>
                    <span>{post["date"]}</span>
                    <span>{post["read_time"]}</span>
                </div>
            </header>
            <div class="blog-body">
                {post["content"]}
            </div>
            {related_html}
            <div style="margin-top:40px; padding:32px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border); text-align:center;">
                <h3 style="margin-bottom:8px;">Want More Insights from Dr. Connor Robertson?</h3>
                <p style="color:var(--text-secondary); margin-bottom:16px;">Subscribe to The Prospecting Show for weekly interviews with top entrepreneurs.</p>
                <a href="https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">&#9654; Listen on Spotify</a>
            </div>
        </article>
    </div>
</section>'''
        
        html = make_page(
            title=post["meta_title"],
            meta_desc=post["description"],
            canonical=f"{SITE_URL}/blog/{slug}/",
            og_type="article",
            breadcrumbs=[("Home", f"{SITE_URL}/"), ("Blog", f"{SITE_URL}/blog/"), (post["title"][:50], f"{SITE_URL}/blog/{slug}/")],
            extra_schemas=[blog_schema],
            body_content=body
        )
        
        with open(os.path.join(BASE_DIR, "blog", slug, "index.html"), "w") as f:
            f.write(html)
        print(f"  Created blog: {slug}")

if __name__ == "__main__":
    print("Creating host page...")
    create_host_page()
    print("\nCreating new blog posts...")
    create_blog_posts()
    print("\nDone!")
