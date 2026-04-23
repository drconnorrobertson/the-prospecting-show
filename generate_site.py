#!/usr/bin/env python3
"""
Site generator for The Prospecting Show podcast website.
Generates all HTML pages, blog posts, sitemap, and robots.txt.
"""

import os
import json
import re
from datetime import datetime

# ─────────────────────────────────────────────
# EPISODE DATA
# ─────────────────────────────────────────────

EPISODES = [
    {"num": 178, "title": "How to Grow Your Business Using Podcast Advertising with Lisa Laporte", "guest": "Lisa Laporte", "date": "Oct 31, 2022", "duration": "18 min 41 sec", "description": "Lisa Laporte shares her wisdom around how to scale a brand using podcast direct host read, embedded ads. If you are a business owner looking for big brand exposure, this episode covers strategies for podcast advertising.", "guest_company": "TWiT.tv", "guest_url": "https://www.twit.tv", "topics": ["Podcast Advertising", "Brand Scaling", "Media Buying"]},
    {"num": 177, "title": "Orthodontics Meets SAAS with Ingrid Murra", "guest": "Ingrid Murra", "date": "Jun 10, 2022", "duration": "15 min 5 sec", "description": "Ingrid shares how mytwofront.com is helping orthodontists and dentists collaborate through their software platform. As an orthodontist herself, Ingrid identified the gap in referral networks between providers.", "guest_company": "Two Front", "guest_url": "https://www.mytwofront.com", "topics": ["SaaS", "Healthcare Tech", "Dental Industry"]},
    {"num": 176, "title": "Optimizing Your Small Business Tax with Jeremy Herskovic", "guest": "Jeremy Herskovic", "date": "May 10, 2022", "duration": "22 min 57 sec", "description": "Jeremy specializes in helping small business owners save on tax. This episode covers small business entity election, pass-through vs corporately held entities and ways that online entrepreneurs can maximize their earnings.", "guest_company": "CalCPA Group", "guest_url": "https://calcpagroup.com", "topics": ["Tax Optimization", "Small Business", "Entity Structure"]},
    {"num": 175, "title": "Souqh.ca - Real Estate Marketplace with Sharjil Salim", "guest": "Sharjil Salim", "date": "Apr 1, 2022", "duration": "11 min 54 sec", "description": "Sharjil and the team at souqh.ca are focused on helping home owners get the services they need for their properties. Their marketplace connects home owners with professional service providers.", "guest_company": "Souqh", "guest_url": "https://souqh.ca", "topics": ["Real Estate", "Marketplace", "Property Services"]},
    {"num": 174, "title": "Insurance Pay Per Lead with Kelly Gordon", "guest": "Kelly Gordon", "date": "Mar 22, 2022", "duration": "17 min 34 sec", "description": "Kelly shows how insurance agents can rapidly grow their business by partnering with a pay per lead vendor to get socially qualified leads into their pipeline.", "guest_company": "", "guest_url": "https://www.linkedin.com/in/kellybryn/", "topics": ["Insurance", "Lead Generation", "Pay Per Lead"]},
    {"num": 173, "title": "Getting the Most for Your Car with Quinn Osha", "guest": "Quinn Osha", "date": "Mar 2, 2022", "duration": "15 min 3 sec", "description": "Quinn Osha, founder of Topmarq.com, walks us through a platform for evaluating the value of vehicles. Useful for both dealerships looking for inventory and consumers wanting top dollar for their cars.", "guest_company": "Topmarq", "guest_url": "https://topmarq.com", "topics": ["Automotive", "Vehicle Valuation", "Marketplace"]},
    {"num": 172, "title": "Digital Business Cards with Pieter Limburg", "guest": "Pieter Limburg", "date": "Feb 15, 2022", "duration": "16 min 58 sec", "description": "Pieter shows how he created a digital business card that you can give your vendors and prospects to scan during the sales process, sharing contact details and social handles without conventional paper cards.", "guest_company": "Mobilo Card", "guest_url": "https://www.mobilocard.com", "topics": ["Networking", "Digital Tools", "Sales Tech"]},
    {"num": 171, "title": "Sales, Communication and Scaling with Eli Wilde", "guest": "Eli Wilde", "date": "Feb 7, 2022", "duration": "21 min 13 sec", "description": "Eli Wilde shares his background of selling for Tony Robbins, building offers, scaling companies and selling from stage for some of the biggest brands in history. He helps sales teams communicate more clearly and dial in their sales process.", "guest_company": "Wilde Influence", "guest_url": "https://www.wildeinfluence.com", "topics": ["Sales", "Communication", "Stage Selling"]},
    {"num": 170, "title": "Sales Enablement with YESWARE - Joel Stevenson", "guest": "Joel Stevenson", "date": "Feb 4, 2022", "duration": "15 min 7 sec", "description": "Joel walks us through a deep Gmail integration software tool that allows you to have predictive follow-up, analytics and sales enablement in your sales process. Perfect for SDR and BDR teams.", "guest_company": "Yesware", "guest_url": "https://www.yesware.com", "topics": ["Sales Enablement", "Email Tracking", "CRM"]},
    {"num": 169, "title": "Finding Your Perfect Franchise with Rich LeBrun", "guest": "Rich LeBrun", "date": "Feb 3, 2022", "duration": "14 min 41 sec", "description": "Rich shows us the hottest businesses in the market to own today. Instead of starting your own business with limited product-market fit, buy a pre-existing franchise that already produces.", "guest_company": "", "guest_url": "https://www.linkedin.com/in/richlebrun/", "topics": ["Franchising", "Business Ownership", "Entrepreneurship"]},
    {"num": 168, "title": "Scaling Your Referrals with Peter Velardi and ReferMeIQ", "guest": "Peter Velardi", "date": "Jan 31, 2022", "duration": "17 min 30 sec", "description": "Peter shows how to scale any business through outbound referral marketing. ReferMeIQ is a platform for business owners and financial professionals to build referral networks.", "guest_company": "ReferMeIQ", "guest_url": "https://www.refermeiq.com", "topics": ["Referrals", "Business Growth", "Networking"]},
    {"num": 167, "title": "SEO Content Built FAST with Market Muse", "guest": "Market Muse Team", "date": "Jan 19, 2022", "duration": "15 min", "description": "Discussion about ways to scale your organic website content. Market Muse has specialized software in content writing through SEO to help you rank higher.", "guest_company": "Market Muse", "guest_url": "https://www.marketmuse.com", "topics": ["SEO", "Content Marketing", "AI Writing"]},
    {"num": 166, "title": "Get Your Tax Right with Sandoval Tax", "guest": "Sandoval Tax Team", "date": "Jan 13, 2022", "duration": "16 min 27 sec", "description": "Covering specialty tax work for small businesses doing under 5 million per year. Learn about tax strategies and compliance for growing businesses.", "guest_company": "Sandoval Tax", "guest_url": "https://www.sandovaltax.com", "topics": ["Tax", "Small Business", "Compliance"]},
    {"num": 165, "title": "Upgrade Your Career with Tim Madden", "guest": "Tim Madden", "date": "Dec 27, 2021", "duration": "16 min 1 sec", "description": "Tim Madden, CEO of Executive Upgrades, shares how to increase your salary as an employee by up to 50% by switching to a new role, optimizing your LinkedIn profile and scaling outreach.", "guest_company": "Executive Upgrades", "guest_url": "https://www.execupgrades.com", "topics": ["Career Growth", "LinkedIn", "Salary Negotiation"]},
    {"num": 164, "title": "Getting Your Systems Straight with Ron Medlin", "guest": "Ron Medlin", "date": "Dec 24, 2021", "duration": "19 min 39 sec", "description": "Ron shows how to use Go High Level to scale your business, from funnels to automations. He helps coaches, consultants and service providers scale through automated and integrated marketing.", "guest_company": "", "guest_url": "", "topics": ["Marketing Automation", "Go High Level", "Systems"]},
    {"num": 163, "title": "LinkedIn 2022 with Stefan Smulders of Expandi", "guest": "Stefan Smulders", "date": "Nov 24, 2021", "duration": "19 min 10 sec", "description": "Stefan shows how to use LinkedIn to grow your business with new features of Expandi, including event campaigns, webinars and alternative ways to connect with people.", "guest_company": "Expandi", "guest_url": "https://www.expandi.io", "topics": ["LinkedIn", "Automation", "Lead Generation"]},
    {"num": 162, "title": "The Team that Grew The Prospecting Show with Ryan Estes of Kitcaster", "guest": "Ryan Estes", "date": "Nov 12, 2021", "duration": "16 min 47 sec", "description": "Ryan Estes, cofounder of Kitcaster, helps entrepreneurs, business owners and tech founders share their ideas through thought leadership on podcasts.", "guest_company": "Kitcaster", "guest_url": "https://www.kitcaster.com", "topics": ["Podcast Booking", "Thought Leadership", "PR"]},
    {"num": 161, "title": "From Recruiter to Coach with Ben Nader", "guest": "Ben Nader", "date": "Nov 9, 2021", "duration": "14 min 38 sec", "description": "Ben shows how he grew a 7-figure brand using a YouTube channel and a Facebook group with no paid ads. He helps recruiters start and scale their businesses.", "guest_company": "6 Figure Recruiter", "guest_url": "", "topics": ["Recruiting", "Coaching", "Organic Marketing"]},
    {"num": 160, "title": "Creating, Building, Scaling and Selling a Company with Andrew Kroeze", "guest": "Andrew Kroeze", "date": "Oct 31, 2021", "duration": "21 min 24 sec", "description": "Andrew shows how he created an offer from scratch, built a team and scaled a coaching business to multiple seven figures before doing an exit. His program has helped hundreds of digital agencies.", "guest_company": "", "guest_url": "", "topics": ["Exit Strategy", "Business Scaling", "Coaching"]},
    {"num": 159, "title": "Finding the Bottleneck with Tom Tonkin", "guest": "Tom Tonkin", "date": "Oct 29, 2021", "duration": "23 min 18 sec", "description": "Tom walks through his frameworks used at The Conservatory Group. He helps executives get unstuck in their role and reach their full potential through organizational management and coaching.", "guest_company": "The Conservatory Group", "guest_url": "https://www.theconservatory.group", "topics": ["Executive Coaching", "Organizational Management", "Leadership"]},
    {"num": 158, "title": "The Perfect LinkedIn Machine with Zach Thomas", "guest": "Zach Thomas", "date": "Oct 20, 2021", "duration": "17 min 11 sec", "description": "Zach Thomas of Compound Marketing shares his copywriting and prospecting techniques that generate 5+ appointments per week on LinkedIn for his clients.", "guest_company": "Compound Marketing", "guest_url": "", "topics": ["LinkedIn", "Copywriting", "Outbound Sales"]},
    {"num": 157, "title": "Finding Your Purpose with Steph Shinabery", "guest": "Steph Shinabery", "date": "Oct 15, 2021", "duration": "17 min 23 sec", "description": "Steph shows why people burn out and how to build a business that is on purpose. She coaches people on how to build their business into something they enjoy month after month.", "guest_company": "", "guest_url": "https://www.stephshinabery.com", "topics": ["Burnout", "Purpose", "Life Coaching"]},
    {"num": 156, "title": "Growing Your Consulting Business with Mark Firth", "guest": "Mark Firth", "date": "Oct 12, 2021", "duration": "16 min 7 sec", "description": "Mark walks through the process of growing an online business through unconventional paid marketing strategies. He helps people with good business ideas make them better through great marketing.", "guest_company": "Clients Impact", "guest_url": "https://www.clientsimpact.com", "topics": ["Consulting", "Paid Marketing", "Funnels"]},
    {"num": 155, "title": "Why You Need a Mentor with Dr. Terri Levine", "guest": "Dr. Terri Levine", "date": "Oct 1, 2021", "duration": "26 min 20 sec", "description": "Dr. Terri shows what it takes to grow a company from nothing to something. Her top advice: make sure you have appointments and hire people. She runs Heartrepreneur and Modern Coaching Method.", "guest_company": "Heartrepreneur", "guest_url": "https://www.heartrepreneur.com", "topics": ["Mentorship", "Coaching", "Business Growth"]},
    # Earlier episodes from search results
    {"num": 120, "title": "Converting Leads With Low Cost Labor with Justin Oglesby", "guest": "Justin Oglesby", "date": "Jun 2021", "duration": "18 min", "description": "Justin shows how businesses can convert leads using cost-effective labor solutions. Conversionly.io helps businesses optimize their lead conversion process.", "guest_company": "Conversionly", "guest_url": "https://conversionly.io", "topics": ["Lead Conversion", "Outsourcing", "Cost Optimization"]},
    {"num": 116, "title": "Scaling an Agency through SOPs with Franbeau Beduya", "guest": "Franbeau Beduya", "date": "May 2021", "duration": "17 min", "description": "Franbeau shares the power of Standard Operating Procedures in scaling a digital marketing agency. Learn how systemizing your processes can unlock growth.", "guest_company": "", "guest_url": "", "topics": ["SOPs", "Agency Growth", "Systems"]},
    {"num": 107, "title": "Building The Tech Behind Your Idea with James Sullivan", "guest": "James Sullivan", "date": "Mar 2021", "duration": "19 min", "description": "James walks through the process of turning a business idea into a technology product. From MVP to scaling, learn how to build the tech foundation for your startup.", "guest_company": "", "guest_url": "", "topics": ["Tech Startups", "MVP", "Product Development"]},
    {"num": 104, "title": "The Offshore Arbitrage with Brett Trembly", "guest": "Brett Trembly", "date": "Feb 2021", "duration": "18 min", "description": "Brett discusses the offshore staffing model and how businesses can leverage international talent to scale operations while maintaining quality.", "guest_company": "Get Staffed Up", "guest_url": "https://getstaffedup.com", "topics": ["Offshore Staffing", "Arbitrage", "Virtual Teams"]},
    {"num": 100, "title": "Scaling SEO with Salik Muhammed", "guest": "Salik Muhammed", "date": "Jan 2021", "duration": "20 min", "description": "Salik shares strategies for scaling SEO efforts to drive organic traffic and business growth. Episode 100 milestone covers the evolution of search engine optimization.", "guest_company": "", "guest_url": "", "topics": ["SEO", "Organic Traffic", "Digital Marketing"]},
    {"num": 98, "title": "Building an Insurance Marketing Company with Justin Connor", "guest": "Justin Connor", "date": "Jan 2021", "duration": "17 min", "description": "Justin shares his journey building an insurance marketing company from scratch. Learn about niche marketing, lead generation, and building a specialized business.", "guest_company": "", "guest_url": "", "topics": ["Insurance Marketing", "Niche Business", "Lead Generation"]},
    {"num": 93, "title": "High Ticket Sales with Kelsey Oneal", "guest": "Kelsey Oneal", "date": "Dec 2020", "duration": "19 min", "description": "Kelsey discusses the intersection of high ticket sales and high ticket solutions. Learn frameworks for selling premium services and closing large deals.", "guest_company": "", "guest_url": "", "topics": ["High Ticket Sales", "Premium Pricing", "Sales Strategy"]},
    {"num": 75, "title": "Entrepreneurial Insights with Dr. Mike Carberry", "guest": "Dr. Mike Carberry", "date": "Sep 2020", "duration": "22 min", "description": "Dr. Mike Carberry shares his journey from clinical practice to entrepreneurship. Discussing the mindset shifts required to build a business in healthcare.", "guest_company": "", "guest_url": "", "topics": ["Healthcare", "Entrepreneurship", "Mindset"]},
    {"num": 70, "title": "Entrepreneurial Highlight with Ian Reith", "guest": "Ian Reith", "date": "Aug 2020", "duration": "16 min", "description": "Ian Reith is featured in this entrepreneurial highlight episode, showcasing the talents of people around the world who excel at what they do.", "guest_company": "", "guest_url": "", "topics": ["Entrepreneurship", "Business Strategy", "Leadership"]},
    {"num": 62, "title": "Entrepreneurial Highlight with Victoria Mattingly", "guest": "Victoria Mattingly", "date": "Jul 2020", "duration": "15 min", "description": "Victoria Mattingly shares her entrepreneurial journey and the lessons learned building a business. Part of the show's entrepreneurial highlight series.", "guest_company": "", "guest_url": "", "topics": ["Entrepreneurship", "Business Building", "Growth"]},
    {"num": 56, "title": "Education, Entrepreneurship, and Why Learning Never Stops with Jordan Ellis and Shamauri Phillip", "guest": "Jordan Ellis & Shamauri Phillip", "date": "Jun 2020", "duration": "20 min", "description": "Jordan Ellis and Shamauri Phillip discuss the intersection of education and entrepreneurship, and why continuous learning is essential for business success.", "guest_company": "", "guest_url": "", "topics": ["Education", "Continuous Learning", "Entrepreneurship"]},
    {"num": 54, "title": "Real Estate Investing with Spencer Gatten", "guest": "Spencer Gatten", "date": "May 2020", "duration": "21 min", "description": "Spencer Gatten breaks down real estate investing strategies for entrepreneurs looking to diversify their portfolio and build wealth through property.", "guest_company": "", "guest_url": "", "topics": ["Real Estate", "Investing", "Wealth Building"]},
    {"num": 32, "title": "Scaling Using Systems with Ravi Abuvala", "guest": "Ravi Abuvala", "date": "Feb 2020", "duration": "23 min", "description": "Ravi Abuvala shares his framework for scaling businesses using systems and virtual teams. Learn how to remove yourself from day-to-day operations.", "guest_company": "Scaling With Systems", "guest_url": "https://scalingwithsystems.com", "topics": ["Systems", "Virtual Teams", "Business Scaling"]},
    {"num": 28, "title": "Digital Marketing with RJ Huebert", "guest": "RJ Huebert", "date": "Jan 2020", "duration": "18 min", "description": "RJ Huebert shares digital marketing strategies for small businesses looking to grow their online presence and generate more leads.", "guest_company": "", "guest_url": "", "topics": ["Digital Marketing", "Online Presence", "Lead Generation"]},
    {"num": 6, "title": "Transitioning from Clinical to Sales with Demetri Nikoloulis, DPT", "guest": "Demetri Nikoloulis", "date": "Nov 2019", "duration": "19 min", "description": "Demetri Nikoloulis shares his journey transitioning from a clinical role as a Doctor of Physical Therapy to a career in sales and business development.", "guest_company": "", "guest_url": "", "topics": ["Career Transition", "Healthcare to Sales", "Sales Skills"]},
]

# ─────────────────────────────────────────────
# SPOTIFY SHOW ID FOR EMBEDS
# ─────────────────────────────────────────────
BASE_PATH = "/the-prospecting-show"  # GitHub Pages subdirectory
SPOTIFY_SHOW_ID = "4VDPOlbe2RSSqukaSuYniX"
SPOTIFY_SHOW_URL = f"https://open.spotify.com/show/{SPOTIFY_SHOW_ID}"
APPLE_PODCASTS_URL = "https://podcasts.apple.com/us/podcast/the-prospecting-show/id1488353384"
YOUTUBE_URL = "https://www.youtube.com/@theprospectingshow"

# Cross-linking URLs
HOST_SITE = "https://drconnorrobertson.com"
PITTSBURGH_WIRE = "https://thepittsburghwire.com"
ELIXIR_CONSULTING = "https://elixirconsultinggroup.com"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────

CSS = """
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: #1a1a2e;
    --bg-card-hover: #222240;
    --accent: #6c5ce7;
    --accent-light: #a29bfe;
    --accent-glow: rgba(108, 92, 231, 0.3);
    --text-primary: #f0f0f5;
    --text-secondary: #a0a0b8;
    --text-muted: #6c6c85;
    --border: #2a2a3e;
    --success: #00cec9;
    --warning: #fdcb6e;
    --gradient-1: linear-gradient(135deg, #6c5ce7, #a29bfe);
    --gradient-2: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
    --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 40px rgba(108, 92, 231, 0.15);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
}

a { color: var(--accent-light); text-decoration: none; transition: color 0.3s; }
a:hover { color: var(--accent); }

.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

/* ── Navigation ── */
.nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 1000;
    background: rgba(10, 10, 15, 0.92);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    padding: 0 24px;
}
.nav-inner {
    max-width: 1200px; margin: 0 auto;
    display: flex; align-items: center; justify-content: space-between;
    height: 72px;
}
.nav-brand {
    display: flex; align-items: center; gap: 12px;
    font-weight: 700; font-size: 1.1rem; color: var(--text-primary);
}
.nav-brand img { width: 40px; height: 40px; border-radius: 8px; }
.nav-brand span { background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.nav-links { display: flex; gap: 32px; list-style: none; }
.nav-links a { color: var(--text-secondary); font-size: 0.9rem; font-weight: 500; letter-spacing: 0.02em; }
.nav-links a:hover, .nav-links a.active { color: var(--text-primary); }
.nav-cta {
    background: var(--gradient-1); color: #fff; padding: 10px 24px;
    border-radius: 8px; font-weight: 600; font-size: 0.85rem;
    border: none; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
}
.nav-cta:hover { transform: translateY(-1px); box-shadow: var(--shadow-glow); color: #fff; }
.mobile-toggle { display: none; background: none; border: none; color: var(--text-primary); font-size: 1.5rem; cursor: pointer; }

/* ── Hero ── */
.hero {
    padding: 140px 0 80px;
    background: var(--gradient-2);
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; right: -20%;
    width: 600px; height: 600px;
    background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 60px;
    align-items: center; position: relative; z-index: 1;
}
.hero-content h1 {
    font-size: 3.5rem; font-weight: 800; line-height: 1.1;
    margin-bottom: 20px;
}
.hero-content h1 span { background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-content p { font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 32px; max-width: 500px; }
.hero-buttons { display: flex; gap: 16px; flex-wrap: wrap; }
.btn-primary {
    background: var(--gradient-1); color: #fff; padding: 14px 32px;
    border-radius: 10px; font-weight: 600; font-size: 0.95rem;
    display: inline-flex; align-items: center; gap: 8px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-glow); color: #fff; }
.btn-secondary {
    background: var(--bg-card); color: var(--text-primary);
    border: 1px solid var(--border); padding: 14px 32px;
    border-radius: 10px; font-weight: 600; font-size: 0.95rem;
    display: inline-flex; align-items: center; gap: 8px;
    transition: all 0.2s;
}
.btn-secondary:hover { background: var(--bg-card-hover); border-color: var(--accent); color: #fff; }
.hero-artwork {
    display: flex; justify-content: center;
}
.hero-artwork img {
    width: 380px; height: 380px; border-radius: 20px;
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}
.hero-stats {
    display: flex; gap: 40px; margin-top: 40px;
}
.stat { text-align: left; }
.stat-num { font-size: 2rem; font-weight: 800; background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stat-label { font-size: 0.85rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

/* ── Sections ── */
.section { padding: 80px 0; }
.section-alt { background: var(--bg-secondary); }
.section-title {
    font-size: 2.2rem; font-weight: 700; margin-bottom: 12px;
}
.section-subtitle { color: var(--text-secondary); font-size: 1.05rem; margin-bottom: 48px; }

/* ── Episode Cards ── */
.episodes-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 24px; }
.episode-card {
    background: var(--bg-card); border-radius: 16px; padding: 28px;
    border: 1px solid var(--border); transition: all 0.3s;
    display: flex; flex-direction: column;
}
.episode-card:hover { border-color: var(--accent); transform: translateY(-4px); box-shadow: var(--shadow-glow); }
.episode-num { font-size: 0.75rem; color: var(--accent-light); font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 8px; }
.episode-card h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; line-height: 1.4; }
.episode-card h3 a { color: var(--text-primary); }
.episode-card h3 a:hover { color: var(--accent-light); }
.episode-meta { display: flex; gap: 16px; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 12px; }
.episode-desc { color: var(--text-secondary); font-size: 0.9rem; flex-grow: 1; margin-bottom: 16px; }
.episode-topics { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.topic-tag {
    background: rgba(108, 92, 231, 0.15); color: var(--accent-light);
    padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 500;
}
.episode-actions { display: flex; gap: 12px; margin-top: auto; }
.episode-actions a {
    padding: 8px 16px; border-radius: 8px; font-size: 0.8rem; font-weight: 600;
}
.listen-btn { background: #1DB954; color: #fff !important; }
.listen-btn:hover { background: #1ed760; color: #fff !important; }
.details-btn { background: var(--bg-card-hover); color: var(--text-primary) !important; border: 1px solid var(--border); }

/* ── Guest Grid ── */
.guests-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.guest-card {
    background: var(--bg-card); border-radius: 14px; padding: 24px;
    border: 1px solid var(--border); text-align: center;
    transition: all 0.3s;
}
.guest-card:hover { border-color: var(--accent); transform: translateY(-3px); }
.guest-avatar {
    width: 70px; height: 70px; border-radius: 50%;
    background: var(--gradient-1); display: flex; align-items: center;
    justify-content: center; font-size: 1.5rem; font-weight: 700; color: #fff;
    margin: 0 auto 16px;
}
.guest-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 4px; }
.guest-card .company { color: var(--text-muted); font-size: 0.85rem; margin-bottom: 8px; }
.guest-card .ep-link { font-size: 0.8rem; }

/* ── Blog ── */
.blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 28px; }
.blog-card {
    background: var(--bg-card); border-radius: 16px; overflow: hidden;
    border: 1px solid var(--border); transition: all 0.3s;
}
.blog-card:hover { border-color: var(--accent); transform: translateY(-3px); }
.blog-card-body { padding: 28px; }
.blog-card .category {
    font-size: 0.72rem; font-weight: 700; color: var(--accent-light);
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px;
}
.blog-card h3 { font-size: 1.15rem; font-weight: 600; margin-bottom: 10px; line-height: 1.4; }
.blog-card h3 a { color: var(--text-primary); }
.blog-card h3 a:hover { color: var(--accent-light); }
.blog-card p { color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 16px; }
.blog-card .read-more { font-size: 0.85rem; font-weight: 600; color: var(--accent-light); }

/* ── Subscribe Page ── */
.platform-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }
.platform-card {
    background: var(--bg-card); border-radius: 16px; padding: 32px;
    border: 1px solid var(--border); text-align: center;
    transition: all 0.3s;
}
.platform-card:hover { border-color: var(--accent); transform: translateY(-4px); box-shadow: var(--shadow-glow); }
.platform-icon { font-size: 3rem; margin-bottom: 16px; }
.platform-card h3 { font-size: 1.2rem; margin-bottom: 8px; }
.platform-card p { color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 20px; }

/* ── Contact Form ── */
.contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px; color: var(--text-secondary); }
.form-group input, .form-group textarea, .form-group select {
    width: 100%; padding: 14px 16px; background: var(--bg-card);
    border: 1px solid var(--border); border-radius: 10px;
    color: var(--text-primary); font-size: 0.95rem; font-family: inherit;
    transition: border-color 0.3s;
}
.form-group input:focus, .form-group textarea:focus, .form-group select:focus {
    outline: none; border-color: var(--accent);
}
.form-group textarea { min-height: 140px; resize: vertical; }

/* ── Footer ── */
.footer {
    background: var(--bg-secondary); border-top: 1px solid var(--border);
    padding: 60px 0 30px;
}
.footer-grid {
    display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px;
    margin-bottom: 40px;
}
.footer-brand p { color: var(--text-secondary); font-size: 0.9rem; margin-top: 12px; max-width: 300px; }
.footer-col h4 { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 16px; }
.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 10px; }
.footer-col a { color: var(--text-secondary); font-size: 0.9rem; }
.footer-col a:hover { color: var(--text-primary); }
.footer-bottom {
    border-top: 1px solid var(--border); padding-top: 24px;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.8rem; color: var(--text-muted);
}

/* ── Episode Detail ── */
.episode-detail { padding: 120px 0 60px; }
.episode-detail .back-link { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px; display: inline-block; }
.episode-detail h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 16px; }
.episode-detail .meta-bar { display: flex; gap: 24px; color: var(--text-muted); font-size: 0.9rem; margin-bottom: 32px; flex-wrap: wrap; }
.episode-detail .spotify-embed { margin: 32px 0; border-radius: 12px; overflow: hidden; }
.episode-detail .content-section { margin: 40px 0; }
.episode-detail .content-section h2 { font-size: 1.5rem; margin-bottom: 16px; color: var(--accent-light); }
.guest-bio-card {
    background: var(--bg-card); border-radius: 16px; padding: 32px;
    border: 1px solid var(--border); margin: 32px 0;
    display: flex; gap: 24px; align-items: center;
}
.guest-bio-card .avatar {
    width: 80px; height: 80px; border-radius: 50%;
    background: var(--gradient-1); display: flex; align-items: center;
    justify-content: center; font-size: 2rem; font-weight: 700; color: #fff;
    flex-shrink: 0;
}
.related-episodes { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 20px; }

/* ── Blog Detail ── */
.blog-detail { padding: 120px 0 60px; }
.blog-detail .back-link { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px; display: inline-block; }
.blog-detail article { max-width: 760px; margin: 0 auto; }
.blog-detail h1 { font-size: 2.5rem; font-weight: 700; margin-bottom: 16px; }
.blog-detail .meta { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 32px; }
.blog-detail .content h2 { font-size: 1.5rem; margin: 32px 0 16px; }
.blog-detail .content h3 { font-size: 1.2rem; margin: 24px 0 12px; }
.blog-detail .content p { color: var(--text-secondary); margin-bottom: 16px; }
.blog-detail .content ul, .blog-detail .content ol { color: var(--text-secondary); margin: 0 0 16px 24px; }
.blog-detail .content li { margin-bottom: 8px; }
.blog-detail .content blockquote {
    border-left: 3px solid var(--accent); padding: 16px 24px; margin: 24px 0;
    background: var(--bg-card); border-radius: 0 10px 10px 0;
    color: var(--text-secondary); font-style: italic;
}

/* ── Search/Filter ── */
.search-bar {
    display: flex; gap: 12px; margin-bottom: 32px; flex-wrap: wrap;
}
.search-bar input {
    flex: 1; min-width: 260px; padding: 14px 20px; background: var(--bg-card);
    border: 1px solid var(--border); border-radius: 10px;
    color: var(--text-primary); font-size: 0.95rem;
}
.search-bar input:focus { outline: none; border-color: var(--accent); }
.search-bar select {
    padding: 14px 20px; background: var(--bg-card);
    border: 1px solid var(--border); border-radius: 10px;
    color: var(--text-primary); font-size: 0.95rem;
}

/* ── About ── */
.about-hero {
    display: grid; grid-template-columns: 1fr 1fr; gap: 60px;
    align-items: center; margin-bottom: 60px;
}
.about-content h2 { font-size: 1.8rem; margin-bottom: 16px; }
.about-content p { color: var(--text-secondary); margin-bottom: 16px; }
.values-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; }
.value-card {
    background: var(--bg-card); border-radius: 14px; padding: 28px;
    border: 1px solid var(--border);
}
.value-card .icon { font-size: 2rem; margin-bottom: 12px; }
.value-card h3 { font-size: 1.1rem; margin-bottom: 8px; }
.value-card p { color: var(--text-secondary); font-size: 0.9rem; }

/* ── Responsive ── */
@media (max-width: 768px) {
    .hero-grid { grid-template-columns: 1fr; text-align: center; }
    .hero-content h1 { font-size: 2.2rem; }
    .hero-content p { margin: 0 auto 32px; }
    .hero-buttons { justify-content: center; }
    .hero-artwork img { width: 280px; height: 280px; }
    .hero-stats { justify-content: center; }
    .nav-links { display: none; }
    .mobile-toggle { display: block; }
    .nav-links.active {
        display: flex; flex-direction: column;
        position: absolute; top: 72px; left: 0; right: 0;
        background: var(--bg-primary); padding: 24px; gap: 16px;
        border-bottom: 1px solid var(--border);
    }
    .footer-grid { grid-template-columns: 1fr 1fr; }
    .contact-grid { grid-template-columns: 1fr; }
    .about-hero { grid-template-columns: 1fr; }
    .episodes-grid { grid-template-columns: 1fr; }
    .blog-grid { grid-template-columns: 1fr; }
    .blog-detail h1, .episode-detail h1 { font-size: 1.8rem; }
    .guest-bio-card { flex-direction: column; text-align: center; }
}

@media (max-width: 480px) {
    .hero-content h1 { font-size: 1.8rem; }
    .section-title { font-size: 1.6rem; }
    .hero-stats { flex-direction: column; gap: 16px; align-items: center; }
    .footer-grid { grid-template-columns: 1fr; }
}
"""

# ─────────────────────────────────────────────
# JS
# ─────────────────────────────────────────────

JS = """
// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.mobile-toggle');
    const links = document.querySelector('.nav-links');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('active'));
    }

    // Episode search/filter
    const searchInput = document.getElementById('episode-search');
    const topicFilter = document.getElementById('topic-filter');
    if (searchInput) {
        searchInput.addEventListener('input', filterEpisodes);
    }
    if (topicFilter) {
        topicFilter.addEventListener('change', filterEpisodes);
    }
});

function filterEpisodes() {
    const search = (document.getElementById('episode-search')?.value || '').toLowerCase();
    const topic = document.getElementById('topic-filter')?.value || '';
    const cards = document.querySelectorAll('.episode-card');
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        const topics = card.dataset.topics || '';
        const matchSearch = !search || text.includes(search);
        const matchTopic = !topic || topics.includes(topic);
        card.style.display = (matchSearch && matchTopic) ? '' : 'none';
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
        e.preventDefault();
        document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});
    });
});
"""

# ─────────────────────────────────────────────
# BLOG ARTICLES
# ─────────────────────────────────────────────

BLOG_POSTS = [
    {
        "slug": "ultimate-guide-to-b2b-prospecting",
        "title": "The Ultimate Guide to B2B Prospecting in 2025",
        "category": "Prospecting",
        "date": "2025-01-15",
        "read_time": "8 min read",
        "excerpt": "Master the art of B2B prospecting with proven strategies for identifying, qualifying, and engaging high-value prospects.",
        "related_episodes": [158, 163, 170],
        "content": """<h2>What is B2B Prospecting?</h2>
<p>B2B prospecting is the process of identifying and reaching out to potential business clients who could benefit from your product or service. Unlike B2C sales, B2B prospecting requires a more strategic, relationship-driven approach that focuses on solving specific business problems.</p>
<p>On The Prospecting Show, Dr. Connor Robertson has interviewed hundreds of entrepreneurs who have mastered the art of prospecting. The common thread? They all prioritize building genuine relationships over making quick sales.</p>

<h2>The Modern Prospecting Framework</h2>
<p>The days of cold calling from a phone book are long gone. Today's most successful prospectors use a multi-channel approach that combines LinkedIn outreach, email sequences, content marketing, and strategic networking.</p>
<p>As discussed in multiple episodes of The Prospecting Show, the key elements of a modern prospecting framework include identifying your ideal customer profile, crafting personalized outreach messages, leveraging social proof through case studies and testimonials, and following up consistently without being pushy.</p>

<h2>LinkedIn as a Prospecting Tool</h2>
<p>LinkedIn remains the most powerful platform for B2B prospecting. With over 900 million professionals on the platform, it offers unparalleled access to decision-makers across every industry.</p>
<p>Stefan Smulders of Expandi shared powerful LinkedIn automation strategies on Episode 163 of The Prospecting Show. His approach combines personalized connection requests with value-driven content to build a pipeline of qualified leads.</p>

<h2>Email Prospecting Best Practices</h2>
<p>Email remains a cornerstone of effective prospecting. The key is personalization. Generic mass emails get ignored, but a well-crafted, personalized email that addresses a specific pain point can open doors to significant business opportunities.</p>
<p>Tools like Yesware, discussed on Episode 170 with Joel Stevenson, provide the analytics and automation needed to scale your email outreach while maintaining a personal touch.</p>

<h2>Building a Sustainable Pipeline</h2>
<p>The most successful prospectors think of their pipeline as a living system that requires daily attention. Consistency beats intensity. It is better to reach out to 10 well-researched prospects per day than to blast 100 generic messages once a week.</p>
<p>For more insights on building and scaling your prospecting system, subscribe to The Prospecting Show on Spotify or Apple Podcasts.</p>"""
    },
    {
        "slug": "scaling-your-business-with-systems",
        "title": "How to Scale Your Business with Systems and SOPs",
        "category": "Business Growth",
        "date": "2025-02-10",
        "read_time": "7 min read",
        "excerpt": "Learn how successful entrepreneurs use systems, SOPs, and automation to remove themselves from day-to-day operations and scale.",
        "related_episodes": [32, 116, 164],
        "content": """<h2>The Systems-First Mindset</h2>
<p>Every entrepreneur hits a ceiling. You can only work so many hours, take so many calls, and manage so many clients before you burn out. The solution is not working harder; it is building systems that work without you.</p>
<p>On Episode 32 of The Prospecting Show, Ravi Abuvala shared his framework for scaling businesses using systems and virtual teams. His approach has helped thousands of entrepreneurs break through their growth ceiling.</p>

<h2>What Makes a Good SOP?</h2>
<p>A Standard Operating Procedure should be clear enough that someone with no context can follow it and produce a consistent result. The best SOPs include a clear objective statement, step-by-step instructions with screenshots, quality checkpoints, and troubleshooting guidance for common issues.</p>

<h2>Automation Tools for Scale</h2>
<p>Ron Medlin discussed on Episode 164 how tools like Go High Level can automate entire marketing and sales workflows. From lead capture to follow-up sequences, the right automation stack can multiply your output without increasing your workload.</p>

<h2>Building Your Team Around Systems</h2>
<p>Systems are not just about software. They are about creating a framework that allows your team to operate independently. When every process is documented and optimized, you can hire confidently, onboard quickly, and maintain quality at scale.</p>
<p>Franbeau Beduya on Episode 116 demonstrated how SOPs enabled her to scale a digital marketing agency by creating repeatable processes for every client deliverable.</p>

<h2>The Path Forward</h2>
<p>Start by documenting your three most time-consuming processes. Record yourself performing each task, then create written and video SOPs. Test them with a team member and iterate based on their feedback. Within 90 days, you will have freed up hours of your week for higher-value activities.</p>"""
    },
    {
        "slug": "linkedin-outreach-strategies",
        "title": "LinkedIn Outreach Strategies That Actually Work",
        "category": "Sales",
        "date": "2025-03-05",
        "read_time": "6 min read",
        "excerpt": "Discover proven LinkedIn outreach strategies from top sales professionals who have generated millions in pipeline.",
        "related_episodes": [158, 163, 165],
        "content": """<h2>Why LinkedIn Outreach Matters</h2>
<p>LinkedIn is where business decisions are made. Over 80% of B2B leads generated through social media come from LinkedIn, making it the single most important platform for professional outreach.</p>

<h2>Crafting the Perfect Connection Request</h2>
<p>Your connection request is your first impression. Skip the generic "I'd like to add you to my professional network" message. Instead, reference something specific: a post they wrote, a mutual connection, or a recent achievement. Keep it under 300 characters and focus on what you admire about their work, not what you want to sell.</p>

<h2>The Value-First Approach</h2>
<p>Zach Thomas of Compound Marketing, featured on Episode 158 of The Prospecting Show, generates 5+ appointments per week on LinkedIn using a copywriting-first approach. His secret? Lead with value, not a pitch. Share insights, offer help, and build rapport before ever mentioning your service.</p>

<h2>Automation Done Right</h2>
<p>Stefan Smulders shared on Episode 163 how Expandi helps professionals automate their LinkedIn outreach while maintaining personalization. The key is using automation to handle the repetitive tasks while keeping your messaging human and relevant.</p>

<h2>Optimizing Your Profile</h2>
<p>Tim Madden from Episode 165 emphasized that your LinkedIn profile is your digital storefront. Before spending time on outreach, make sure your profile clearly communicates who you help, how you help them, and what results you deliver.</p>

<h2>Measuring What Matters</h2>
<p>Track your connection acceptance rate, response rate, and meeting booking rate. If your acceptance rate is below 30%, your connection requests need work. If your response rate is below 15%, your follow-up messages need improvement.</p>"""
    },
    {
        "slug": "from-side-hustle-to-full-time-business",
        "title": "From Side Hustle to Full-Time Business: The Transition Guide",
        "category": "Entrepreneurship",
        "date": "2025-04-12",
        "read_time": "9 min read",
        "excerpt": "A practical roadmap for transitioning from employee to full-time entrepreneur, based on real stories from The Prospecting Show.",
        "related_episodes": [6, 160, 155],
        "content": """<h2>When to Make the Leap</h2>
<p>The question every aspiring entrepreneur faces is: when do I quit my job? There is no universal answer, but there are clear signals that you are ready. Most guests on The Prospecting Show agree that you should have at least 3 to 6 months of living expenses saved, consistent revenue from your side business, and a clear growth trajectory.</p>

<h2>The Clinical-to-Sales Transition</h2>
<p>Demetri Nikoloulis, featured on Episode 6, made the transition from clinical work as a Doctor of Physical Therapy to a career in sales and business development. His story illustrates that the skills you build in one career often transfer powerfully to entrepreneurship.</p>

<h2>Building Before You Burn</h2>
<p>Dr. Terri Levine on Episode 155 emphasized two critical pieces of advice for new entrepreneurs: make sure you have appointments, and hire people. Too many new business owners try to do everything themselves and burn out before they ever hit their stride.</p>

<h2>The Exit Strategy That Funds Your Next Move</h2>
<p>Andrew Kroeze on Episode 160 shared how he created an offer from scratch, built a team, and scaled to multiple seven figures before executing an exit. His story shows that building with the end in mind creates options and financial freedom.</p>

<h2>Your First 90 Days</h2>
<p>The first three months of full-time entrepreneurship are critical. Focus on revenue-generating activities above everything else. Build relationships, make offers, and collect feedback. Everything else, including your website, your logo, and your business cards, can wait.</p>"""
    },
    {
        "slug": "seo-strategies-for-small-businesses",
        "title": "SEO Strategies Every Small Business Owner Should Know",
        "category": "Digital Marketing",
        "date": "2025-05-20",
        "read_time": "7 min read",
        "excerpt": "Practical SEO tactics that small business owners can implement today to increase organic traffic and generate more leads.",
        "related_episodes": [100, 167],
        "content": """<h2>Why SEO Matters for Small Businesses</h2>
<p>Search engine optimization is one of the highest-ROI marketing channels available to small businesses. Unlike paid advertising, organic traffic compounds over time. A blog post you write today can generate leads for years to come.</p>

<h2>The Content-First Approach</h2>
<p>Salik Muhammed shared on Episode 100 of The Prospecting Show how to scale SEO efforts for sustainable growth. The foundation is always quality content that answers the questions your ideal customers are asking.</p>

<h2>Tools That Accelerate Your SEO</h2>
<p>Market Muse, discussed on Episode 167, offers AI-powered content optimization that helps you create comprehensive, authoritative content faster. By analyzing top-ranking pages for your target keywords, these tools help you understand what topics to cover and how deeply to explore them.</p>

<h2>Local SEO for Service Businesses</h2>
<p>If you serve a specific geographic area, local SEO should be your top priority. Claim and optimize your Google Business Profile, get reviews from happy clients, and create location-specific content. For many service businesses, ranking in the local map pack can generate more leads than any other channel.</p>

<h2>Technical SEO Fundamentals</h2>
<p>Ensure your website loads quickly, is mobile-friendly, and has clean URL structures. Use schema markup to help search engines understand your content. These technical foundations make everything else you do with SEO more effective.</p>

<h2>Measuring SEO Success</h2>
<p>Track your organic traffic, keyword rankings, and most importantly, leads generated from organic search. SEO is a long game, so set expectations accordingly. Most businesses should expect to see meaningful results within 6 to 12 months of consistent effort.</p>"""
    },
    {
        "slug": "high-ticket-sales-framework",
        "title": "The High-Ticket Sales Framework: Closing Premium Deals",
        "category": "Sales",
        "date": "2025-06-08",
        "read_time": "8 min read",
        "excerpt": "Learn the frameworks and mindset shifts needed to sell premium services and close high-value deals consistently.",
        "related_episodes": [93, 171, 156],
        "content": """<h2>What Defines High-Ticket Sales?</h2>
<p>High-ticket sales typically involve deals worth $5,000 or more. These sales require a fundamentally different approach than transactional selling. The buyer needs more trust, more information, and more confidence before making a decision.</p>

<h2>The Consultative Approach</h2>
<p>Kelsey Oneal on Episode 93 discussed how high-ticket sales meet high-ticket solutions. The key insight is that you are not selling a product; you are selling a transformation. Your prospect needs to see clearly how their life or business will be different after working with you.</p>

<h2>Communication is Everything</h2>
<p>Eli Wilde, featured on Episode 171, built his career selling for Tony Robbins and from stage for some of the biggest brands in history. His approach centers on clear, confident communication that addresses both the logical and emotional needs of the buyer.</p>

<h2>Building a Premium Offer</h2>
<p>Mark Firth on Episode 156 shared how to grow a consulting business using unconventional marketing strategies and webinar-style funnels. The right offer structure can dramatically increase your close rate and average deal size.</p>

<h2>Handling Price Objections</h2>
<p>When selling premium services, price objections are inevitable. The solution is not to lower your price but to increase the perceived value. Use case studies, guarantees, and clear ROI projections to help prospects understand the true cost of not working with you.</p>

<h2>The Follow-Up System</h2>
<p>Most high-ticket deals are not closed on the first call. Build a follow-up system that stays top-of-mind without being pushy. Share relevant content, check in with genuine curiosity, and always provide value in every interaction.</p>"""
    },
    {
        "slug": "real-estate-investing-for-entrepreneurs",
        "title": "Real Estate Investing for Entrepreneurs: Getting Started",
        "category": "Investing",
        "date": "2025-07-15",
        "read_time": "7 min read",
        "excerpt": "How entrepreneurs can diversify their income through real estate investing, with insights from The Prospecting Show guests.",
        "related_episodes": [54, 175, 169],
        "content": """<h2>Why Entrepreneurs Should Consider Real Estate</h2>
<p>Real estate offers something that most businesses cannot: passive income that is not directly tied to your time. For entrepreneurs already building active income through their businesses, real estate provides diversification and long-term wealth building.</p>

<h2>Getting Started with Real Estate Investing</h2>
<p>Spencer Gatten on Episode 54 of The Prospecting Show broke down real estate investing strategies for entrepreneurs. His advice: start with education, build your network, and make your first deal within 90 days of deciding to invest.</p>

<h2>The Real Estate Tech Stack</h2>
<p>Sharjil Salim and the team at Souqh, featured on Episode 175, are building marketplace tools that connect property owners with service providers. Technology is making real estate investing more accessible than ever, from property analysis tools to marketplace platforms.</p>

<h2>Franchise Ownership as an Alternative</h2>
<p>Rich LeBrun on Episode 169 presented franchising as an alternative to starting from scratch. Franchises offer proven systems, established brands, and lower risk compared to building a business from zero.</p>

<h2>Building Your Investment Strategy</h2>
<p>Start by defining your investment goals. Are you looking for cash flow, appreciation, or tax benefits? Your strategy will differ based on your objectives. Connect with local investors, attend meetups, and consider partnering on your first deal to reduce risk while gaining experience.</p>"""
    },
    {
        "slug": "building-referral-network",
        "title": "Building a Referral Network That Generates Leads on Autopilot",
        "category": "Business Growth",
        "date": "2025-08-22",
        "read_time": "6 min read",
        "excerpt": "Strategies for building a referral network that consistently generates warm, qualified leads for your business.",
        "related_episodes": [168, 162, 174],
        "content": """<h2>The Power of Referrals</h2>
<p>Referral leads close at 3 to 5 times the rate of cold leads. They come with built-in trust, shorter sales cycles, and higher lifetime value. Yet most businesses leave referrals to chance instead of building a systematic approach.</p>

<h2>Systemizing Your Referral Process</h2>
<p>Peter Velardi of ReferMeIQ, featured on Episode 168, demonstrated how to scale referral marketing through outbound strategies. Instead of waiting for referrals to come to you, actively build and nurture a referral network.</p>

<h2>Leveraging Thought Leadership</h2>
<p>Ryan Estes of Kitcaster shared on Episode 162 how podcast appearances can fuel referral growth. When you position yourself as a thought leader through content and media appearances, your network naturally starts sending opportunities your way.</p>

<h2>Insurance and Financial Services Referrals</h2>
<p>Kelly Gordon on Episode 174 showed how insurance agents can rapidly grow through performance-based marketing and referral partnerships. The principles apply across industries: create value for your referral partners and make it easy for them to send you business.</p>

<h2>The Ask</h2>
<p>Most professionals never ask for referrals because it feels uncomfortable. Reframe it: you are not asking for a favor. You are offering your referral partner the chance to help someone they care about solve a real problem. Make the ask specific, make it easy, and always follow up with gratitude.</p>"""
    },
]

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def slug(text):
    """Convert text to URL-friendly slug."""
    s = text.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s).strip('-')
    return s[:80]

def get_initials(name):
    """Get initials from a name."""
    parts = name.split()
    if len(parts) >= 2:
        return parts[0][0] + parts[-1][0]
    return parts[0][0] if parts else '?'

def nav_html(active=''):
    """Generate navigation HTML."""
    links = [
        (f'{BASE_PATH}/', 'Home'), (f'{BASE_PATH}/episodes/', 'Episodes'), (f'{BASE_PATH}/about/', 'About'),
        (f'{BASE_PATH}/guests/', 'Guests'), (f'{BASE_PATH}/blog/', 'Blog'), (f'{BASE_PATH}/contact/', 'Contact')
    ]
    nav_items = ''
    for href, label in links:
        cls = ' class="active"' if label.lower() == active.lower() else ''
        nav_items += f'<li><a href="{href}"{cls}>{label}</a></li>'

    return f"""<nav class="nav">
    <div class="nav-inner">
        <a href="{BASE_PATH}/" class="nav-brand">
            <span>The Prospecting Show</span>
        </a>
        <ul class="nav-links">{nav_items}</ul>
        <a href="{BASE_PATH}/subscribe/" class="nav-cta">Subscribe</a>
        <button class="mobile-toggle" aria-label="Menu">&#9776;</button>
    </div>
</nav>"""

def footer_html():
    """Generate footer HTML."""
    return f"""<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="{BASE_PATH}/" class="nav-brand"><span>The Prospecting Show</span></a>
                <p>Every week, Dr. Connor Robertson interviews entrepreneurs and business owners about how they built, scaled, and grew their businesses.</p>
            </div>
            <div class="footer-col">
                <h4>Show</h4>
                <ul>
                    <li><a href="{BASE_PATH}/episodes/">All Episodes</a></li>
                    <li><a href="{BASE_PATH}/guests/">Guests</a></li>
                    <li><a href="{BASE_PATH}/about/">About</a></li>
                    <li><a href="{BASE_PATH}/blog/">Blog</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Listen</h4>
                <ul>
                    <li><a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener">Spotify</a></li>
                    <li><a href="{APPLE_PODCASTS_URL}" target="_blank" rel="noopener">Apple Podcasts</a></li>
                    <li><a href="{YOUTUBE_URL}" target="_blank" rel="noopener">YouTube</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>Connect</h4>
                <ul>
                    <li><a href="{HOST_SITE}" target="_blank" rel="noopener">Dr. Connor Robertson</a></li>
                    <li><a href="{ELIXIR_CONSULTING}" target="_blank" rel="noopener">Elixir Consulting Group</a></li>
                    <li><a href="{PITTSBURGH_WIRE}" target="_blank" rel="noopener">The Pittsburgh Wire</a></li>
                    <li><a href="{BASE_PATH}/contact/">Contact Us</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; {datetime.now().year} The Prospecting Show with Dr. Connor Robertson. All rights reserved.</span>
            <span>Hosted by <a href="{HOST_SITE}" target="_blank" rel="noopener">Dr. Connor Robertson</a></span>
        </div>
    </div>
</footer>"""

def head_html(title, description, path='/', og_type='website', schema=''):
    """Generate HTML head with SEO."""
    canonical = f"https://drconnorrobertson.github.io/the-prospecting-show{path}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="author" content="Dr. Connor Robertson">
    <link rel="canonical" href="{canonical}">

    <!-- Open Graph -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="The Prospecting Show">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="{BASE_PATH}/css/style.css">
    {schema}
</head>"""

def page_wrap(title, description, body, active='', path='/', og_type='website', schema=''):
    """Wrap content in full HTML page."""
    return f"""{head_html(title, description, path, og_type, schema)}
<body>
{nav_html(active)}
{body}
{footer_html()}
<script src="{BASE_PATH}/js/main.js"></script>
</body>
</html>"""

# ─────────────────────────────────────────────
# PAGE GENERATORS
# ─────────────────────────────────────────────

def generate_homepage():
    """Generate the homepage."""
    # Latest 6 episodes
    latest = EPISODES[:6]
    episode_cards = ''
    for ep in latest:
        topics_html = ''.join(f'<span class="topic-tag">{t}</span>' for t in ep['topics'][:3])
        ep_slug = slug(ep['title'])
        desc = ep['description'][:150] + '...' if len(ep['description']) > 150 else ep['description']
        episode_cards += f"""
        <div class="episode-card" data-topics="{','.join(ep['topics'])}">
            <span class="episode-num">Episode {ep['num']}</span>
            <h3><a href="{BASE_PATH}/episodes/{ep_slug}/">{ep['title']}</a></h3>
            <div class="episode-meta"><span>{ep['date']}</span><span>{ep['duration']}</span></div>
            <p class="episode-desc">{desc}</p>
            <div class="episode-topics">{topics_html}</div>
            <div class="episode-actions">
                <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="listen-btn">Listen on Spotify</a>
                <a href="{BASE_PATH}/episodes/{ep_slug}/" class="details-btn">Details</a>
            </div>
        </div>"""

    # Featured guests
    featured_guests = [ep for ep in EPISODES if ep.get('guest_company')][:8]
    guest_cards = ''
    for ep in featured_guests:
        initials = get_initials(ep['guest'])
        guest_cards += f"""
        <div class="guest-card">
            <div class="guest-avatar">{initials}</div>
            <h3>{ep['guest']}</h3>
            <p class="company">{ep['guest_company']}</p>
            <a href="{BASE_PATH}/episodes/{slug(ep['title'])}/" class="ep-link">Episode {ep['num']}</a>
        </div>"""

    # Blog cards
    blog_cards = ''
    for post in BLOG_POSTS[:3]:
        blog_cards += f"""
        <div class="blog-card">
            <div class="blog-card-body">
                <span class="category">{post['category']}</span>
                <h3><a href="{BASE_PATH}/blog/{post['slug']}/">{post['title']}</a></h3>
                <p>{post['excerpt']}</p>
                <a href="{BASE_PATH}/blog/{post['slug']}/" class="read-more">Read Article &rarr;</a>
            </div>
        </div>"""

    schema = f"""<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "PodcastSeries",
    "name": "The Prospecting Show with Dr. Connor Robertson",
    "description": "Every week Dr. Connor Robertson interviews small business owners about their businesses. The format of the show includes past, present and future stories of how entrepreneurs have been able to successfully scale their businesses.",
    "url": "https://drconnorrobertson.github.io/the-prospecting-show/",
    "author": {{
        "@type": "Person",
        "name": "Dr. Connor Robertson",
        "url": "{HOST_SITE}"
    }},
    "webFeed": "{SPOTIFY_SHOW_URL}",
    "genre": ["Business", "Entrepreneurship", "Sales"],
    "inLanguage": "en"
}}
</script>"""

    body = f"""
<section class="hero">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-content">
                <h1>The <span>Prospecting</span> Show</h1>
                <p>Every week, Dr. Connor Robertson interviews entrepreneurs and small business owners about how they built, scaled, and grew their businesses. Real stories. Real strategies. Real results.</p>
                <div class="hero-buttons">
                    <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="btn-primary">
                        &#9654; Listen on Spotify
                    </a>
                    <a href="{BASE_PATH}/episodes/" class="btn-secondary">Browse Episodes</a>
                </div>
                <div class="hero-stats">
                    <div class="stat"><div class="stat-num">178+</div><div class="stat-label">Episodes</div></div>
                    <div class="stat"><div class="stat-num">150+</div><div class="stat-label">Guests</div></div>
                    <div class="stat"><div class="stat-num">3+</div><div class="stat-label">Years Running</div></div>
                </div>
            </div>
            <div class="hero-artwork">
                <img src="https://i.scdn.co/image/ab6765630000ba8a0e3e8b2e25c8b1a3c7e1e4a0" alt="The Prospecting Show Podcast Artwork" onerror="this.style.display='none'">
            </div>
        </div>
    </div>
</section>

<section class="section section-alt">
    <div class="container">
        <h2 class="section-title">Latest Episodes</h2>
        <p class="section-subtitle">Catch up on the newest conversations with top entrepreneurs and business leaders.</p>
        <div class="episodes-grid">{episode_cards}</div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{BASE_PATH}/episodes/" class="btn-primary">View All Episodes &rarr;</a>
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <h2 class="section-title">Featured Guests</h2>
        <p class="section-subtitle">Learn from entrepreneurs who are building real businesses across every industry.</p>
        <div class="guests-grid">{guest_cards}</div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{BASE_PATH}/guests/" class="btn-secondary">View All Guests &rarr;</a>
        </div>
    </div>
</section>

<section class="section section-alt">
    <div class="container">
        <h2 class="section-title">From the Blog</h2>
        <p class="section-subtitle">Insights on prospecting, sales, and business growth from The Prospecting Show.</p>
        <div class="blog-grid">{blog_cards}</div>
        <div style="text-align:center; margin-top:40px;">
            <a href="{BASE_PATH}/blog/" class="btn-secondary">Read More &rarr;</a>
        </div>
    </div>
</section>

<section class="section" style="text-align:center;">
    <div class="container">
        <h2 class="section-title">Never Miss an Episode</h2>
        <p class="section-subtitle">Subscribe on your favorite platform and get notified when new episodes drop.</p>
        <div class="hero-buttons" style="justify-content:center;">
            <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">&#9654; Spotify</a>
            <a href="{APPLE_PODCASTS_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#8B5CF6;">&#127911; Apple Podcasts</a>
            <a href="{YOUTUBE_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#FF0000;">&#9654; YouTube</a>
        </div>
    </div>
</section>"""

    return page_wrap(
        "The Prospecting Show with Dr. Connor Robertson | Podcast",
        "Every week Dr. Connor Robertson interviews entrepreneurs and small business owners about scaling their businesses. Listen on Spotify, Apple Podcasts, and YouTube.",
        body, 'Home', '/', 'website', schema
    )


def generate_episodes_page():
    """Generate the episodes listing page."""
    # Collect all unique topics
    all_topics = set()
    for ep in EPISODES:
        all_topics.update(ep['topics'])
    topic_options = ''.join(f'<option value="{t}">{t}</option>' for t in sorted(all_topics))

    cards = ''
    for ep in EPISODES:
        topics_html = ''.join(f'<span class="topic-tag">{t}</span>' for t in ep['topics'][:3])
        ep_slug = slug(ep['title'])
        desc = ep['description'][:150] + '...' if len(ep['description']) > 150 else ep['description']
        cards += f"""
        <div class="episode-card" data-topics="{','.join(ep['topics'])}">
            <span class="episode-num">Episode {ep['num']}</span>
            <h3><a href="{BASE_PATH}/episodes/{ep_slug}/">{ep['title']}</a></h3>
            <div class="episode-meta"><span>{ep['date']}</span><span>{ep['duration']}</span></div>
            <p class="episode-desc">{desc}</p>
            <div class="episode-topics">{topics_html}</div>
            <div class="episode-actions">
                <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="listen-btn">Listen on Spotify</a>
                <a href="{BASE_PATH}/episodes/{ep_slug}/" class="details-btn">Details</a>
            </div>
        </div>"""

    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <h1 class="section-title">All Episodes</h1>
        <p class="section-subtitle">Browse {len(EPISODES)} episodes of The Prospecting Show. Search by guest name, topic, or keyword.</p>
        <div class="search-bar">
            <input type="text" id="episode-search" placeholder="Search episodes by guest, topic, or keyword...">
            <select id="topic-filter">
                <option value="">All Topics</option>
                {topic_options}
            </select>
        </div>
        <div class="episodes-grid">{cards}</div>
    </div>
</section>"""

    return page_wrap(
        "All Episodes | The Prospecting Show with Dr. Connor Robertson",
        "Browse all episodes of The Prospecting Show. Search by guest name, topic, or keyword. Featuring interviews with entrepreneurs and business leaders.",
        body, 'Episodes', '/episodes/'
    )


def generate_episode_detail(ep):
    """Generate individual episode page."""
    ep_slug = slug(ep['title'])
    topics_html = ''.join(f'<span class="topic-tag">{t}</span>' for t in ep['topics'])
    initials = get_initials(ep['guest'])

    # Guest bio section
    guest_link = ''
    if ep.get('guest_url'):
        guest_link = f' | <a href="{ep["guest_url"]}" target="_blank" rel="noopener">Website</a>'
    company_text = f' of {ep["guest_company"]}' if ep.get('guest_company') else ''

    # Related episodes (same topics)
    related = []
    for other in EPISODES:
        if other['num'] != ep['num'] and any(t in other['topics'] for t in ep['topics']):
            related.append(other)
            if len(related) >= 3:
                break

    related_html = ''
    for r in related:
        r_slug = slug(r['title'])
        related_html += f"""
        <div class="episode-card">
            <span class="episode-num">Episode {r['num']}</span>
            <h3><a href="{BASE_PATH}/episodes/{r_slug}/">{r['title']}</a></h3>
            <div class="episode-meta"><span>{r['date']}</span></div>
        </div>"""

    # Key takeaways
    takeaways = f"""<ul>
        <li>Insights from {ep['guest']}{company_text} on {ep['topics'][0].lower() if ep['topics'] else 'business growth'}</li>
        <li>Practical strategies for {ep['topics'][1].lower() if len(ep['topics']) > 1 else 'scaling your business'}</li>
        <li>How to apply these lessons to your own entrepreneurial journey</li>
    </ul>"""

    schema = f"""<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "PodcastEpisode",
    "name": "Episode {ep['num']} - {ep['title']}",
    "description": "{ep['description'][:200]}",
    "episodeNumber": {ep['num']},
    "datePublished": "{ep['date']}",
    "duration": "{ep['duration']}",
    "partOfSeries": {{
        "@type": "PodcastSeries",
        "name": "The Prospecting Show with Dr. Connor Robertson",
        "url": "https://drconnorrobertson.github.io/the-prospecting-show/"
    }},
    "author": {{
        "@type": "Person",
        "name": "Dr. Connor Robertson",
        "url": "{HOST_SITE}"
    }}
}}
</script>"""

    body = f"""
<section class="episode-detail">
    <div class="container">
        <a href="{BASE_PATH}/episodes/" class="back-link">&larr; Back to All Episodes</a>
        <span class="episode-num" style="display:block; margin-bottom:12px;">Episode {ep['num']}</span>
        <h1>{ep['title']}</h1>
        <div class="meta-bar">
            <span>Guest: <strong>{ep['guest']}</strong></span>
            <span>{ep['date']}</span>
            <span>{ep['duration']}</span>
        </div>
        <div class="episode-topics" style="margin-bottom:24px;">{topics_html}</div>

        <div class="spotify-embed">
            <iframe style="border-radius:12px" src="https://open.spotify.com/embed/show/{SPOTIFY_SHOW_ID}?utm_source=generator&theme=0" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>

        <div class="content-section">
            <h2>About This Episode</h2>
            <p style="color:var(--text-secondary); font-size:1.05rem;">{ep['description']}</p>
        </div>

        <div class="guest-bio-card">
            <div class="avatar">{initials}</div>
            <div>
                <h3>{ep['guest']}{company_text}</h3>
                <p style="color:var(--text-secondary); font-size:0.9rem;">Featured guest on Episode {ep['num']} of The Prospecting Show with Dr. Connor Robertson.{guest_link}</p>
            </div>
        </div>

        <div class="content-section">
            <h2>Key Takeaways</h2>
            {takeaways}
        </div>

        <div class="content-section" style="text-align:center; padding:40px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border);">
            <h2 style="color:var(--text-primary); margin-bottom:12px;">Listen to the Full Episode</h2>
            <p style="color:var(--text-secondary); margin-bottom:20px;">Catch the full conversation on your favorite podcast platform.</p>
            <div class="hero-buttons" style="justify-content:center;">
                <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">&#9654; Spotify</a>
                <a href="{APPLE_PODCASTS_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#8B5CF6;">&#127911; Apple Podcasts</a>
            </div>
        </div>

        {"<div class='content-section'><h2>Related Episodes</h2><div class='related-episodes'>" + related_html + "</div></div>" if related_html else ""}
    </div>
</section>"""

    return page_wrap(
        f"Episode {ep['num']}: {ep['title']} | The Prospecting Show",
        ep['description'][:160],
        body, 'Episodes', f'/episodes/{ep_slug}/', 'article', schema
    )


def generate_about_page():
    """Generate the about page."""
    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <div class="about-hero">
            <div class="about-content">
                <h1 class="section-title">About The Show</h1>
                <p>Every week, Dr. Connor Robertson hosts The Prospecting Show, where he interviews small business owners about their businesses. The format of the show includes past, present, and future stories of how entrepreneurs have been able to successfully scale their businesses.</p>
                <p>With over 178 episodes and counting, The Prospecting Show has become a go-to resource for entrepreneurs, sales professionals, and business owners looking to learn from people who have done it before.</p>
                <p>Topics covered on the show include sales and prospecting, lead generation, business systems and automation, digital marketing and SEO, real estate investing, franchise ownership, LinkedIn strategies, and much more.</p>
            </div>
            <div style="text-align:center;">
                <div style="width:300px; height:300px; border-radius:20px; background:var(--gradient-1); display:flex; align-items:center; justify-content:center; margin:0 auto;">
                    <span style="font-size:4rem; color:#fff; font-weight:800;">TPS</span>
                </div>
            </div>
        </div>

        <div class="content-section" style="margin:60px 0;">
            <h2 class="section-title">About Your Host</h2>
            <div class="guest-bio-card" style="max-width:800px;">
                <div class="avatar" style="width:100px; height:100px; font-size:2.5rem;">CR</div>
                <div>
                    <h3 style="font-size:1.3rem;">Dr. Connor Robertson</h3>
                    <p style="color:var(--text-secondary); margin-bottom:12px;">Dr. Connor Robertson is an entrepreneur, podcast host, and business strategist based in Pittsburgh, PA. Through The Prospecting Show, Connor brings together the most innovative entrepreneurs and business owners to share their stories, strategies, and insights.</p>
                    <p style="color:var(--text-secondary); margin-bottom:12px;">Connor is also the founder of <a href="{ELIXIR_CONSULTING}" target="_blank" rel="noopener">Elixir Consulting Group</a> and a contributor to <a href="{PITTSBURGH_WIRE}" target="_blank" rel="noopener">The Pittsburgh Wire</a>.</p>
                    <a href="{HOST_SITE}" target="_blank" rel="noopener" class="btn-secondary" style="display:inline-flex; margin-top:8px;">Visit drconnorrobertson.com &rarr;</a>
                </div>
            </div>
        </div>

        <h2 class="section-title">What We Cover</h2>
        <p class="section-subtitle">The Prospecting Show explores every aspect of building and growing a business.</p>
        <div class="values-grid">
            <div class="value-card">
                <div class="icon">&#128200;</div>
                <h3>Sales &amp; Prospecting</h3>
                <p>Learn proven strategies for generating leads, closing deals, and building a predictable sales pipeline from top performers.</p>
            </div>
            <div class="value-card">
                <div class="icon">&#9881;</div>
                <h3>Systems &amp; Automation</h3>
                <p>Discover how to build SOPs, automate workflows, and create systems that let you scale without burning out.</p>
            </div>
            <div class="value-card">
                <div class="icon">&#128640;</div>
                <h3>Business Growth</h3>
                <p>From side hustle to seven figures, hear real stories of entrepreneurs who built, scaled, and sometimes exited their businesses.</p>
            </div>
            <div class="value-card">
                <div class="icon">&#128187;</div>
                <h3>Digital Marketing</h3>
                <p>SEO, content marketing, LinkedIn strategies, email outreach, and every digital channel that drives business growth.</p>
            </div>
            <div class="value-card">
                <div class="icon">&#127968;</div>
                <h3>Real Estate &amp; Investing</h3>
                <p>Real estate investing, property tech, and alternative investment strategies for entrepreneurs looking to diversify.</p>
            </div>
            <div class="value-card">
                <div class="icon">&#129309;</div>
                <h3>Networking &amp; Referrals</h3>
                <p>Build referral networks, leverage thought leadership, and create partnerships that generate warm leads consistently.</p>
            </div>
        </div>
    </div>
</section>"""

    return page_wrap(
        "About The Prospecting Show | Dr. Connor Robertson",
        "Learn about The Prospecting Show podcast hosted by Dr. Connor Robertson. Every week, Connor interviews entrepreneurs about how they built and scaled their businesses.",
        body, 'About', '/about/'
    )


def generate_guests_page():
    """Generate the guests page."""
    guest_cards = ''
    seen_guests = set()
    for ep in EPISODES:
        if ep['guest'] in seen_guests:
            continue
        seen_guests.add(ep['guest'])
        initials = get_initials(ep['guest'])
        company = f'<p class="company">{ep["guest_company"]}</p>' if ep.get('guest_company') else '<p class="company">Entrepreneur</p>'
        link = ''
        if ep.get('guest_url'):
            link = f'<a href="{ep["guest_url"]}" target="_blank" rel="noopener" style="font-size:0.8rem; display:block; margin-bottom:6px;">Website</a>'
        ep_slug = slug(ep['title'])
        guest_cards += f"""
        <div class="guest-card">
            <div class="guest-avatar">{initials}</div>
            <h3>{ep['guest']}</h3>
            {company}
            {link}
            <a href="{BASE_PATH}/episodes/{ep_slug}/" class="ep-link">Episode {ep['num']}</a>
        </div>"""

    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <h1 class="section-title">Our Guests</h1>
        <p class="section-subtitle">The Prospecting Show has featured {len(seen_guests)}+ entrepreneurs, founders, and business leaders. Here are some of our featured guests.</p>
        <div class="guests-grid">{guest_cards}</div>
    </div>
</section>"""

    return page_wrap(
        "Guests | The Prospecting Show with Dr. Connor Robertson",
        "Browse the entrepreneurs, founders, and business leaders who have appeared on The Prospecting Show podcast with Dr. Connor Robertson.",
        body, 'Guests', '/guests/'
    )


def generate_subscribe_page():
    """Generate the subscribe page."""
    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <h1 class="section-title" style="text-align:center;">Subscribe to The Prospecting Show</h1>
        <p class="section-subtitle" style="text-align:center; max-width:600px; margin:0 auto 48px;">Choose your favorite platform and never miss an episode. New episodes drop weekly.</p>

        <div class="platform-grid">
            <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="platform-card">
                <div class="platform-icon">&#127911;</div>
                <h3>Spotify</h3>
                <p>Listen on Spotify with video episodes, show notes, and seamless playback across all your devices.</p>
                <span class="btn-primary" style="background:#1DB954;">Listen on Spotify</span>
            </a>
            <a href="{APPLE_PODCASTS_URL}" target="_blank" rel="noopener" class="platform-card">
                <div class="platform-icon">&#127911;</div>
                <h3>Apple Podcasts</h3>
                <p>Subscribe on Apple Podcasts for automatic downloads and notifications when new episodes are available.</p>
                <span class="btn-primary" style="background:#8B5CF6;">Listen on Apple</span>
            </a>
            <a href="{YOUTUBE_URL}" target="_blank" rel="noopener" class="platform-card">
                <div class="platform-icon">&#9654;</div>
                <h3>YouTube</h3>
                <p>Watch video episodes on YouTube. See the conversations come to life with full video interviews.</p>
                <span class="btn-primary" style="background:#FF0000;">Watch on YouTube</span>
            </a>
        </div>

        <div style="text-align:center; margin-top:60px; padding:40px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border);">
            <h2 style="margin-bottom:12px;">Want to Be a Guest?</h2>
            <p style="color:var(--text-secondary); margin-bottom:20px; max-width:500px; margin-left:auto; margin-right:auto;">If you are an entrepreneur or business owner with a story to share, we would love to hear from you.</p>
            <a href="{BASE_PATH}/contact/" class="btn-primary">Apply to Be a Guest &rarr;</a>
        </div>
    </div>
</section>"""

    return page_wrap(
        "Subscribe | The Prospecting Show with Dr. Connor Robertson",
        "Subscribe to The Prospecting Show on Spotify, Apple Podcasts, YouTube, and more. Never miss an episode with Dr. Connor Robertson.",
        body, '', '/subscribe/'
    )


def generate_blog_index():
    """Generate the blog listing page."""
    cards = ''
    for post in BLOG_POSTS:
        cards += f"""
        <div class="blog-card">
            <div class="blog-card-body">
                <span class="category">{post['category']}</span>
                <h3><a href="{BASE_PATH}/blog/{post['slug']}/">{post['title']}</a></h3>
                <p>{post['excerpt']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.8rem; color:var(--text-muted);">{post['date']} &middot; {post['read_time']}</span>
                    <a href="{BASE_PATH}/blog/{post['slug']}/" class="read-more">Read &rarr;</a>
                </div>
            </div>
        </div>"""

    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <h1 class="section-title">The Prospecting Show Blog</h1>
        <p class="section-subtitle">Insights on sales, prospecting, business growth, and entrepreneurship. Inspired by conversations on The Prospecting Show.</p>
        <div class="blog-grid">{cards}</div>
    </div>
</section>"""

    return page_wrap(
        "Blog | The Prospecting Show - Sales, Prospecting & Business Growth",
        "Read articles on B2B prospecting, sales strategies, business growth, and entrepreneurship from The Prospecting Show with Dr. Connor Robertson.",
        body, 'Blog', '/blog/'
    )


def generate_blog_detail(post):
    """Generate individual blog post page."""
    # Related episode links
    related_links = ''
    for ep_num in post.get('related_episodes', []):
        ep = next((e for e in EPISODES if e['num'] == ep_num), None)
        if ep:
            ep_slug = slug(ep['title'])
            related_links += f'<li><a href="{BASE_PATH}/episodes/{ep_slug}/">Episode {ep["num"]}: {ep["title"]}</a></li>'

    schema = f"""<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{post['title']}",
    "description": "{post['excerpt']}",
    "datePublished": "{post['date']}",
    "author": {{
        "@type": "Person",
        "name": "Dr. Connor Robertson",
        "url": "{HOST_SITE}"
    }},
    "publisher": {{
        "@type": "Organization",
        "name": "The Prospecting Show"
    }}
}}
</script>"""

    body = f"""
<section class="blog-detail">
    <div class="container">
        <article>
            <a href="{BASE_PATH}/blog/" class="back-link">&larr; Back to Blog</a>
            <span class="category" style="display:block; font-size:0.75rem; font-weight:700; color:var(--accent-light); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">{post['category']}</span>
            <h1>{post['title']}</h1>
            <div class="meta">By <a href="{HOST_SITE}" target="_blank" rel="noopener">Dr. Connor Robertson</a> &middot; {post['date']} &middot; {post['read_time']}</div>

            <div class="content">
                {post['content']}
            </div>

            {"<div class='content-section' style='margin-top:40px;'><h2>Related Episodes</h2><ul>" + related_links + "</ul></div>" if related_links else ""}

            <div style="margin-top:40px; padding:32px; background:var(--bg-card); border-radius:16px; border:1px solid var(--border); text-align:center;">
                <h3 style="margin-bottom:8px;">Want More Insights?</h3>
                <p style="color:var(--text-secondary); margin-bottom:16px;">Subscribe to The Prospecting Show for weekly interviews with top entrepreneurs.</p>
                <a href="{SPOTIFY_SHOW_URL}" target="_blank" rel="noopener" class="btn-primary" style="background:#1DB954;">&#9654; Listen on Spotify</a>
            </div>
        </article>
    </div>
</section>"""

    return page_wrap(
        f"{post['title']} | The Prospecting Show Blog",
        post['excerpt'],
        body, 'Blog', f'/blog/{post["slug"]}/', 'article', schema
    )


def generate_contact_page():
    """Generate the contact page."""
    body = f"""
<section class="section" style="padding-top:120px;">
    <div class="container">
        <h1 class="section-title">Get in Touch</h1>
        <p class="section-subtitle">Interested in being a guest, sponsoring the show, or just want to say hi? We would love to hear from you.</p>

        <div class="contact-grid">
            <div>
                <form action="https://formspree.io/f/placeholder" method="POST">
                    <div class="form-group">
                        <label>Your Name</label>
                        <input type="text" name="name" required placeholder="John Smith">
                    </div>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" name="email" required placeholder="john@company.com">
                    </div>
                    <div class="form-group">
                        <label>Inquiry Type</label>
                        <select name="type">
                            <option value="guest">Guest Application</option>
                            <option value="sponsorship">Sponsorship Inquiry</option>
                            <option value="general">General Question</option>
                            <option value="feedback">Feedback</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Your Website (optional)</label>
                        <input type="url" name="website" placeholder="https://yourcompany.com">
                    </div>
                    <div class="form-group">
                        <label>Message</label>
                        <textarea name="message" required placeholder="Tell us about yourself and what you would like to discuss..."></textarea>
                    </div>
                    <button type="submit" class="btn-primary" style="border:none; cursor:pointer; font-size:1rem;">Send Message</button>
                </form>
            </div>
            <div>
                <div class="value-card" style="margin-bottom:24px;">
                    <h3 style="margin-bottom:12px;">Want to Be a Guest?</h3>
                    <p style="color:var(--text-secondary);">We are always looking for entrepreneurs and business owners with compelling stories. If you have built, scaled, or sold a business, we want to hear from you. Fill out the form with "Guest Application" selected and tell us about your story.</p>
                </div>
                <div class="value-card" style="margin-bottom:24px;">
                    <h3 style="margin-bottom:12px;">Sponsorship Opportunities</h3>
                    <p style="color:var(--text-secondary);">The Prospecting Show reaches thousands of entrepreneurs and business professionals every week. If you are interested in getting your brand in front of this audience, let us know.</p>
                </div>
                <div class="value-card">
                    <h3 style="margin-bottom:12px;">Connect with Connor</h3>
                    <p style="color:var(--text-secondary);">Visit <a href="{HOST_SITE}" target="_blank" rel="noopener">drconnorrobertson.com</a> to learn more about Connor and his other projects including <a href="{ELIXIR_CONSULTING}" target="_blank" rel="noopener">Elixir Consulting Group</a>.</p>
                </div>
            </div>
        </div>
    </div>
</section>"""

    return page_wrap(
        "Contact | The Prospecting Show with Dr. Connor Robertson",
        "Get in touch with The Prospecting Show. Apply to be a guest, inquire about sponsorships, or send us feedback.",
        body, 'Contact', '/contact/'
    )


def generate_sitemap():
    """Generate sitemap.xml."""
    base = "https://drconnorrobertson.github.io/the-prospecting-show"
    urls = [
        ('/', '1.0', 'weekly'),
        ('/episodes/', '0.9', 'weekly'),
        ('/about/', '0.8', 'monthly'),
        ('/guests/', '0.8', 'weekly'),
        ('/subscribe/', '0.7', 'monthly'),
        ('/blog/', '0.8', 'weekly'),
        ('/contact/', '0.6', 'monthly'),
    ]

    for ep in EPISODES:
        ep_slug = slug(ep['title'])
        urls.append((f'/episodes/{ep_slug}/', '0.7', 'monthly'))

    for post in BLOG_POSTS:
        urls.append((f'/blog/{post["slug"]}/', '0.7', 'monthly'))

    entries = ''
    for path, priority, freq in urls:
        entries += f"""  <url>
    <loc>{base}{path}</loc>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlmap xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}</urlmap>"""


def generate_robots():
    """Generate robots.txt."""
    return f"""User-agent: *
Allow: /

Sitemap: https://drconnorrobertson.github.io/the-prospecting-show/sitemap.xml
"""


def generate_404():
    """Generate 404 page."""
    body = """
<section class="section" style="padding-top:160px; text-align:center; min-height:60vh;">
    <div class="container">
        <h1 style="font-size:6rem; font-weight:800; background:var(--gradient-1); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">404</h1>
        <h2 style="margin-bottom:16px;">Page Not Found</h2>
        <p style="color:var(--text-secondary); margin-bottom:32px;">The page you are looking for does not exist or has been moved.</p>
        <a href="{BASE_PATH}/" class="btn-primary">Back to Home</a>
    </div>
</section>"""
    return page_wrap("Page Not Found | The Prospecting Show", "The page you are looking for does not exist.", body)


# ─────────────────────────────────────────────
# MAIN BUILD
# ─────────────────────────────────────────────

def build():
    """Build the entire site."""
    base = '/sessions/quirky-kind-gates/the-prospecting-show'

    # CSS and JS
    os.makedirs(f'{base}/css', exist_ok=True)
    os.makedirs(f'{base}/js', exist_ok=True)
    with open(f'{base}/css/style.css', 'w') as f:
        f.write(CSS)
    with open(f'{base}/js/main.js', 'w') as f:
        f.write(JS)

    # Homepage
    with open(f'{base}/index.html', 'w') as f:
        f.write(generate_homepage())
    print("Generated: index.html")

    # Episodes index
    os.makedirs(f'{base}/episodes', exist_ok=True)
    with open(f'{base}/episodes/index.html', 'w') as f:
        f.write(generate_episodes_page())
    print("Generated: episodes/index.html")

    # Individual episode pages
    for ep in EPISODES:
        ep_slug = slug(ep['title'])
        ep_dir = f'{base}/episodes/{ep_slug}'
        os.makedirs(ep_dir, exist_ok=True)
        with open(f'{ep_dir}/index.html', 'w') as f:
            f.write(generate_episode_detail(ep))
    print(f"Generated: {len(EPISODES)} episode pages")

    # About
    os.makedirs(f'{base}/about', exist_ok=True)
    with open(f'{base}/about/index.html', 'w') as f:
        f.write(generate_about_page())
    print("Generated: about/index.html")

    # Guests
    os.makedirs(f'{base}/guests', exist_ok=True)
    with open(f'{base}/guests/index.html', 'w') as f:
        f.write(generate_guests_page())
    print("Generated: guests/index.html")

    # Subscribe
    os.makedirs(f'{base}/subscribe', exist_ok=True)
    with open(f'{base}/subscribe/index.html', 'w') as f:
        f.write(generate_subscribe_page())
    print("Generated: subscribe/index.html")

    # Blog index
    os.makedirs(f'{base}/blog', exist_ok=True)
    with open(f'{base}/blog/index.html', 'w') as f:
        f.write(generate_blog_index())
    print("Generated: blog/index.html")

    # Blog posts
    for post in BLOG_POSTS:
        post_dir = f'{base}/blog/{post["slug"]}'
        os.makedirs(post_dir, exist_ok=True)
        with open(f'{post_dir}/index.html', 'w') as f:
            f.write(generate_blog_detail(post))
    print(f"Generated: {len(BLOG_POSTS)} blog posts")

    # Contact
    os.makedirs(f'{base}/contact', exist_ok=True)
    with open(f'{base}/contact/index.html', 'w') as f:
        f.write(generate_contact_page())
    print("Generated: contact/index.html")

    # Sitemap, robots, 404
    with open(f'{base}/sitemap.xml', 'w') as f:
        f.write(generate_sitemap())
    with open(f'{base}/robots.txt', 'w') as f:
        f.write(generate_robots())
    with open(f'{base}/404.html', 'w') as f:
        f.write(generate_404())
    print("Generated: sitemap.xml, robots.txt, 404.html")

    print(f"\nBuild complete! Total pages: {4 + len(EPISODES) + len(BLOG_POSTS) + 4}")


if __name__ == '__main__':
    build()
