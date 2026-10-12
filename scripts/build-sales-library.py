#!/usr/bin/env python3
"""Build scenario-based sales resources from editable editorial source files."""
from pathlib import Path
import csv,html,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
BASE='https://prospectingshow.com'
PERSON='https://www.drconnorrobertson.com/#person'
PREFIX='/blog/sales-playbooks/'
DATE='2026-10-12'
E=lambda x:html.escape(str(x),quote=True)
contexts=[dict(zip(('slug','name','buyer','pain','metrics','trigger','constraints','artifact','next'),line.split('|'))) for line in (ROOT/'content/sales-contexts.txt').read_text().splitlines() if line]
flows=[dict(zip(('slug','name','purpose','steps','output','metric','failure','exit'),line.split('|'))) for line in (ROOT/'content/sales-workflows.txt').read_text().splitlines() if line]
assert len(contexts)==40 and len(flows)==25
CSS='''<style>.library{max-width:940px;margin:0 auto;padding:115px 24px 60px}.library h1{font-size:clamp(2rem,5vw,3rem);line-height:1.15;margin:20px 0}.library h2{font-size:1.6rem;margin:36px 0 14px}.library h3{margin:24px 0 10px}.library p,.library ul,.library ol,.library table,.library blockquote{margin:16px 0}.library li{margin:10px 0}.library ul,.library ol{padding-left:24px}.library table{border-collapse:collapse;width:100%}.library th,.library td{border:1px solid var(--border);padding:12px;text-align:left;vertical-align:top}.library blockquote,.library .note{background:var(--bg-card);padding:20px;border-left:3px solid var(--accent-light)}.library .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.library .tile{padding:18px;border:1px solid var(--border);border-radius:12px}.library input{width:100%;padding:14px;font:inherit;margin:12px 0;background:var(--bg-card);color:var(--text-primary);border:1px solid var(--border)}.library .small{color:var(--text-secondary);font-size:.9rem}.library summary{cursor:pointer;font-weight:600}.library :focus-visible{outline:3px solid var(--accent-light);outline-offset:4px}.library pre{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg-card);padding:20px}.library button{padding:10px 18px;font:inherit;cursor:pointer}.library .table-wrap{overflow-x:auto}@media(max-width:600px){.nav-inner{height:auto;min-height:90px;flex-wrap:wrap;gap:8px 20px;padding:12px 0}.nav-brand{width:100%}.library{padding-top:130px}.library footer{padding-top:24px}}@media print{.nav,.library button,footer{display:none}.library{padding:0;max-width:none}body{background:white;color:black}a{color:black}.library .note,.library blockquote,.library pre{background:#f5f5f5}.library tr{break-inside:avoid}}</style>'''
NAV='<nav class="nav"><div class="nav-inner"><a class="nav-brand" href="/">The Prospecting Show</a><a href="/host/">Dr. Connor Robertson</a><a href="'+PREFIX+'">Sales library</a></div></nav>'
FOOT='<footer class="library" style="padding-top:30px"><p><a href="/host/">Dr. Connor Robertson, host of The Prospecting Show</a> · <a href="https://www.drconnorrobertson.com/">Official website</a> · <a href="https://www.drconnorrobertsonbooks.com/">Books</a> · <a href="/episodes/">Podcast archive</a></p><p class="small">© 2026 The Prospecting Show. Examples are illustrative planning exercises, not claims about actual clients or results.</p></footer>'
urls=[]; records=[]
def write(path,title,desc,body,kind='WebPage',crumbs=None):
 url=BASE+path
 schema={'@context':'https://schema.org','@graph':[{'@type':kind,'@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':'en','isPartOf':{'@id':BASE+'/#website'},'publisher':{'@id':BASE+'/#publisher'},'about':{'@id':PERSON}}, {'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'The Prospecting Show with Dr. Connor Robertson','publisher':{'@id':BASE+'/#publisher'}},{'@type':'Organization','@id':BASE+'/#publisher','name':'The Prospecting Show','url':BASE+'/'},{'@type':'Person','@id':PERSON,'name':'Dr. Connor Robertson','url':'https://www.drconnorrobertson.com/','subjectOf':{'@id':BASE+'/host/'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+href} for i,(name,href) in enumerate(crumbs or [('Home','/'),('Sales library',PREFIX),(title,path)])]}]}
 if kind=='Article':schema['@graph'][0].update(headline=title,datePublished=DATE,dateModified=DATE,author={'@id':BASE+'/#publisher'},mainEntityOfPage=url)
 encoded_schema=json.dumps(schema,ensure_ascii=False).replace('</','<'+chr(92)+'/')
 page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Dr. Connor Robertson</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{E(url)}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="{("article" if kind=="Article" else "website")}"><meta property="og:url" content="{E(url)}"><meta property="og:site_name" content="The Prospecting Show with Dr. Connor Robertson"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="/css/style.css">{CSS}<script type="application/ld+json">{encoded_schema}</script></head><body>{NAV}<main class="library"><p class="small"><a href="/">Home</a> / <a href="{PREFIX}">Sales library</a></p><h1>{E(title)}</h1>{body}</main>{FOOT}</body></html>'
 dest=ROOT/path.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page);urls.append(url)
def link(path,label):return f'<a href="{E(path)}">{E(label)}</a>'
def guidepath(c,f):return PREFIX+c['slug']+'/'+f['slug']+'/'
def context_name(c):
 return ' '.join(w if w.isupper() and len(w)>1 else w.lower() for w in c['name'].split())
def example(c,f):
 buyer,pain,metrics,trigger,artifact=c['buyer'],c['pain'],c['metrics'],c['trigger'],c['artifact']
 examples={
 'ideal-customer-profile':f'Include an account only when its operating model makes {pain} plausible and the team can identify an owner. Exclude an account when the proposed service cannot support its operating requirements. Treat {trigger} as a reason to investigate, not an automatic qualification.',
 'account-research':f'Observation: a public page describes {trigger}. Hypothesis: the team may be reviewing {metrics}. Unknown: whether this affects a current priority. Research question: who owns the relevant workflow, and is a review actually underway?',
 'contact-mapping':f'Begin with the {buyer}. Record who experiences {pain}, who reviews {c["constraints"]}, and who can authorize a change. Ask: “Who would need to confirm that this approach works before you could make a decision?”',
 'list-building':f'For each account, capture the company, source URL, verification date, relevant role, fit reason, and suppression status. A fit reason should explain the possible connection to {pain}; “in our target industry” is not enough.',
 'trigger-prioritization':f'Place {trigger} in the research queue. Check the date and source, then ask whether it changes the priority of {pain}. Lower the priority if the relevant team reports no current issue, even when the signal looks impressive.',
 'value-proposition':f'“We help teams evaluate {pain} by making {metrics} visible and turning the findings into an owned next step.” Replace this planning statement with the actual capabilities and boundaries of your offer before using it.',
 'cold-email':f'Subject: Question about your operating review\n\nHi [Name],\nI work with teams evaluating {context_name(c)}. When {trigger} is underway, is this an issue your team reviews: {pain}?\nIf relevant, I can share {artifact}. Would that help with your review?\n[Name, organization, and contact details]',
 'cold-call-opening':f'“Hi [Name], this is [Rep] with [Organization]. I’m calling about {context_name(c)}. Is this a workable moment for one question? When your team reviews {pain}, who usually owns that discussion?” Pause and respond to the answer rather than reading the rest of a script.',
 'voicemail':f'“Hi [Name], [Rep] from [Organization]. I have a question about {context_name(c)} and {pain}. I can share {artifact} if useful. You can reach me at [number], or reply to the email with the same subject. Thank you.”',
 'linkedin-outreach':f'“Hi [Name], I’m interested in how teams approach {context_name(c)}. Your professional role looks relevant to a question about {pain}. Is that an area you work on, or does another team own it?” Use a public professional observation only when you actually verified it.',
 'multichannel-sequence':f'First contact: ask whether {pain} is relevant. Second permitted contact: offer {artifact}. Third contact: clarify whether {trigger} affects timing. End the sequence when the prospect declines, the contact is wrong, or no useful reason to continue remains.',
 'follow-up':f'“You mentioned that {pain} was worth reviewing. I’ve outlined {artifact} so we can check the assumptions together. Does {c["next"]} still make sense, or should we close the loop for now?” Only reference a prior statement if the buyer actually made it.',
 'referral-request':f'“Do you know a team currently evaluating {context_name(c)} where {pain} is a real priority? If so, I can send a short note explaining {c["next"]}. Please make an introduction only if you think it would help them.”',
 'qualification':f'Confirm whether {pain} exists, whether the {buyer} owns the issue, and whether {c["constraints"]} can be addressed. Ask what evidence would justify {c["next"]}. Record a no-fit answer without trying to turn it into pipeline.',
 'discovery-questions':f'Ask: “Walk me through the last time {pain} affected the team.” Then explore: “How do you currently track {metrics}?” Finish with: “What would we need to learn before {c["next"]} would be worth your time?”',
 'meeting-agenda':f'Purpose: decide whether {c["next"]} is worthwhile. Inputs: a description of {pain}, the owner of {metrics}, and known constraints. Outcome: an agreed evidence request or an explicit decision to stop evaluation.',
 'solution-demo':f'Use a fictional case involving {pain}. Show the relevant inputs, action, exception, and output. Ask the {buyer} whether the demonstration reflects the actual workflow, especially {c["constraints"]}. Document the differences rather than claiming full fit.',
 'business-case':f'Baseline: current {metrics}. Proposed change: a defined deliverable addressing {pain}. Cost categories: implementation, staff time, ongoing service, and transition effort. Benefit assumptions must come from the buyer; do not insert industry averages as if they describe this account.',
 'proposal':f'Problem: {pain}. Evidence to review: {metrics}. Initial deliverable: {artifact}. Buyer responsibilities: provide an appropriate owner and approved sample information. Acceptance: both parties agree what a completed review contains before pricing the larger engagement.',
 'price-objection':f'“When you say the price is too high, is the concern the available budget, the scope, or confidence that we can address {pain}?” If a narrower review is sensible, define {c["next"]} as a separate scope with its own deliverables rather than discounting the original proposal without explanation.',
 'incumbent-objection':f'“It makes sense to keep what is working. Does your current approach already address {pain}, including {c["constraints"]}? If it does, there may be no reason to change. If there is a gap, what would you use to evaluate an alternative?”',
 'stalled-deals':f'Check whether the buyer ever committed to reviewing {metrics}. Then ask: “Is {pain} still a priority, or has the review changed?” Offer to agree on {c["next"]}, set a buyer-requested revisit condition, or close the opportunity.',
 'mutual-action-plan':f'Buyer confirms the owner of {metrics}; seller prepares {artifact}; both review {c["constraints"]}; buyer decides whether to proceed to {c["next"]}. Put a real owner and mutually agreed date beside each step. Leave unknown dependencies visible.',
 'pipeline-review':f'Inspect whether the record contains buyer-confirmed evidence of {pain}, a defined owner, and an agreed next step. If the only update is {trigger}, return the account to research until the buying hypothesis is confirmed.',
 'sales-coaching':f'Review whether the rep asked about {pain}, listened to the answer, and clarified who owns {metrics}. Practice one follow-up question using a fictional account. Score the next comparable conversation for that behavior rather than counting extra words or questions.'}
 return examples[f['slug']]
for ci,c in enumerate(contexts):
 for fi,f in enumerate(flows):
  path=guidepath(c,f);title=f'{f["name"]} for {context_name(c)}'
  desc=f'A practical {f["output"]} for {context_name(c)}: buyer context, worked example, checklist, and decision criteria from The Prospecting Show.'
  steps=''.join(f'<li>{E(step)}</li>' for step in f['steps'].split('~'))
  ex=example(c,f)
  related=[link(guidepath(c,flows[(fi+1)%25]),flows[(fi+1)%25]['name']),link(guidepath(c,flows[(fi-1)%25]),flows[(fi-1)%25]['name']),link(PREFIX+'workflows/'+f['slug']+'/',f['name']+' across selling contexts'),link(PREFIX+c['slug']+'/',c['name']+' sales guides')]
  body=f'''<p class="small">The Prospecting Show with <a href="/host/">Dr. Connor Robertson</a> · Editorial sales resource · October 12, 2026</p>
<p>{E(f['purpose'])} This guide applies the workflow to selling {E(context_name(c))}, where a useful conversation may involve the {E(c['buyer'])} and a practical review of {E(c['pain'])}.</p>
<p>The finished result is {E(f['output'])}. Work from information the buyer confirms. The examples below are planning models; replace bracketed fields and unsupported assumptions before using them with an actual account.</p>
<h2>Start with the buyer’s operating context</h2><p>For this selling context, a possible reason to investigate involves {E(c['trigger'])}. That event alone does not establish demand. Check whether the team experiences this issue: {E(c['pain'])}. Confirm who owns the workflow and whether a change is worth evaluating.</p>
<div class="table-wrap"><table><caption>Account facts to confirm before advancing</caption><thead><tr><th scope="col">Question</th><th scope="col">Working hypothesis</th><th scope="col">Evidence to request</th></tr></thead><tbody>
<tr><th scope="row">Who should participate?</th><td>{E(c['buyer'])}</td><td>The contact’s description of ownership and decision roles</td></tr>
<tr><th scope="row">What is happening?</th><td>{E(c['pain'])}</td><td>A recent example from the actual workflow</td></tr>
<tr><th scope="row">What can be measured?</th><td>{E(c['metrics'])}</td><td>A dated baseline with definitions and a named owner</td></tr>
<tr><th scope="row">What constrains a change?</th><td>{E(c['constraints'])}</td><td>Requirements confirmed by the people responsible</td></tr></tbody></table></div>
<h2>A practical sequence</h2><ol>{steps}</ol>
<p>Apply these steps to the same account rather than changing the hypothesis halfway through the exercise. If new evidence contradicts your starting assumption, update the record and reconsider the next action. The objective is a useful decision, not a completed form.</p>
<h2>Worked example: {E(f['name'].lower())}</h2><p class="small">Illustrative example, not a report of a client result.</p><pre>{E(ex)}</pre>
<h2>Use a concrete artifact</h2><p>A useful supporting resource in this context is {E(c['artifact'])}. It should help the {E(c['buyer'])} assess the current situation without forcing them through a generic sales presentation. Keep the scope narrow enough that the buyer can correct it.</p>
<p>For example, connect the artifact to {E(c['metrics'])}. Identify which inputs came from the buyer, which are public observations, and which remain assumptions. Do not request private operational records before the buyer has agreed an appropriate purpose and handling process.</p>
<h2>Build the working record</h2><p>Complete this worksheet during preparation, then revise it after the conversation. An unknown is a useful finding when it is recorded honestly.</p>
<div class="table-wrap"><table><thead><tr><th scope="col">Field</th><th scope="col">What to write</th></tr></thead><tbody>
<tr><th scope="row">Account and owner</th><td>[Account] · [Rep] · [Review date]</td></tr>
<tr><th scope="row">Confirmed problem</th><td>The buyer’s description of {E(c['pain'])}, or “not confirmed”</td></tr>
<tr><th scope="row">Baseline</th><td>Available evidence for {E(c['metrics'])}, with source and date</td></tr>
<tr><th scope="row">Deliverable</th><td>{E(f['output'])}, including scope and the person who reviews it</td></tr>
<tr><th scope="row">Open questions</th><td>Unconfirmed assumptions, required participants, and unresolved constraints</td></tr>
<tr><th scope="row">Next decision</th><td>Advance, gather evidence, revisit by request, or close the record</td></tr></tbody></table></div>
<button type="button" onclick="window.print()">Print this guide and worksheet</button>
<h2>Evaluate the result</h2><p>Track {E(f['metric'])}. Define the numerator, denominator, and review window before comparing results. Use comparable accounts and channels; otherwise an apparent improvement may simply reflect a different list or buying context.</p>
<p>For {E(context_name(c))}, pair the workflow measure with the quality of evidence about {E(c['pain'])}. A reply or meeting is useful only if it helps establish relevance. Record declined and unsuitable opportunities so the team can improve targeting as well as messaging.</p>
<h2>A common failure to avoid</h2><p>{E(f['failure'])}</p><p>In this context, the practical consequence is spending time on {E(c['next'])} before the buyer has confirmed a reason to do it. Revisit {E(c['constraints'])} early enough to discover a genuine mismatch.</p>
<h2>When to move forward</h2><p>{E(f['exit'])} A sensible next step may be {E(c['next'])}, but only when it follows from the evidence. If the buyer cannot identify a relevant problem or owner, close or reclassify the record instead of manufacturing urgency.</p>
<h2>Continue the workflow</h2><ul>{''.join('<li>'+x+'</li>' for x in related)}</ul>
<p>For the wider collection, visit <a href="{PREFIX}">the prospecting and sales library</a>. Learn about the host on the <a href="/host/">Dr. Connor Robertson profile</a> or explore the <a href="/episodes/">published podcast interviews</a>.</p>'''
  write(path,title,desc,body,'Article');records.append({'url':BASE+path,'title':title,'selling_context':c['name'],'workflow':f['name'],'output':f['output']})
# Two navigation axes keep every article close to a useful hub.
for c in contexts:
 cards=''.join(f'<article class="tile"><h2>{link(guidepath(c,f),f["name"])}</h2><p>{E(f["purpose"])}</p></article>' for f in flows)
 write(PREFIX+c['slug']+'/',c['name']+' prospecting and sales guides',f'25 practical sales workflows for {context_name(c)}, from account selection through qualification, proposals, and coaching.',f'<p>Use these 25 guides when selling {E(context_name(c))}. Begin with the workflow you need, then confirm whether {E(c["pain"])} is a relevant buyer issue. Examples are illustrative and should be adapted to your actual offer.</p><p>Potential buying roles: {E(c["buyer"])}. Evidence to discuss: {E(c["metrics"])}.</p><div class="grid">{cards}</div>','CollectionPage')
for f in flows:
 cards=''.join(f'<article class="tile"><h2>{link(guidepath(c,f),c["name"])}</h2><p>Apply this workflow to {E(c["pain"])} and evaluate {E(c["metrics"])}.</p></article>' for c in contexts)
 write(PREFIX+'workflows/'+f['slug']+'/',f['name']+': selling-context examples',f'Apply {f["name"].lower()} across 40 selling contexts with practical examples, buyer questions, and worksheets.',f'<p>{E(f["purpose"])} Choose a selling context below for a worked example and printable planning record.</p><div class="grid">{cards}</div>','CollectionPage')
contextcards=''.join(f'<article class="tile" data-search="{E(context_name(c))}"><h3>{link(PREFIX+c["slug"]+"/",c["name"])}</h3><p>25 workflows · {E(c["buyer"])}</p></article>' for c in contexts)
flowcards=''.join(f'<li>{link(PREFIX+"workflows/"+f["slug"]+"/",f["name"])}</li>' for f in flows)
write(PREFIX,'Prospecting and sales library', 'Explore 1,000 practical sales guides from The Prospecting Show with Dr. Connor Robertson: 25 workflows across 40 selling contexts.',f'''<p>The Prospecting Show with <a href="/host/">Dr. Connor Robertson</a> brings together 1,000 practical guides for prospecting and sales. Browse 25 workflows across 40 selling contexts, with examples, buyer questions, decision criteria, and printable worksheets.</p><p>Start with your selling context, or select a workflow to compare how the same task changes with buyer responsibilities and operating needs. These are editorial planning resources; they do not represent individual podcast episodes or documented client results.</p><h2>Choose a selling context</h2><label for="context-search">Filter selling contexts</label><input id="context-search" type="search" placeholder="Try software, consulting, or logistics"><p id="filter-status" role="status" aria-live="polite">40 selling contexts</p><div class="grid" id="contexts">{contextcards}</div><h2>Choose a sales workflow</h2><ul>{flowcards}</ul><h2>About the collection</h2><p>Each guide starts with a buyer hypothesis, walks through the task, and ends with the evidence needed to proceed or stop. Reuse the structure, but confirm account facts before outreach. No guide promises a response rate, revenue result, or guaranteed search ranking.</p><p><a href="/host/">Meet Dr. Connor Robertson</a> · <a href="/blog/">Read the blog</a> · <a href="/sales-library-index.csv">Download the complete guide index</a></p><script>const q=document.getElementById('context-search');q.addEventListener('input',()=>{{let count=0;document.querySelectorAll('[data-search]').forEach(card=>{{card.hidden=!card.dataset.search.includes(q.value.trim().toLowerCase());if(!card.hidden)count++;}});document.getElementById('filter-status').textContent=count+(count===1?' selling context':' selling contexts');}});</script>''','CollectionPage')
with (ROOT/'sales-library-index.csv').open('w',newline='') as out:
 writer=csv.DictWriter(out,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
# Add discoverability without rewriting the existing blog or historical articles.
for name in ('index.html','blog/index.html','host/index.html'):
 p=ROOT/name;s=p.read_text();marker='id="sales-library-entry"'
 if marker not in s:
  section=f'<section class="section" {marker}><div class="container"><h2>Prospecting and sales resources</h2><p>Explore 1,000 practical sales guides from The Prospecting Show with Dr. Connor Robertson, organized by workflow and selling context.</p><p><a href="{PREFIX}">Browse the prospecting and sales library</a></p></div></section>'
  s=s.replace('<footer',section+'\n<footer',1);p.write_text(s)
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
p=ROOT/'sitemap.xml';tree=ET.parse(p);root=tree.getroot();known={x.text.strip() for x in root.findall(f'{{{ns}}}url/{{{ns}}}loc')}
for url in urls:
 if url not in known:
  node=ET.SubElement(root,f'{{{ns}}}url');ET.SubElement(node,f'{{{ns}}}loc').text=url;ET.SubElement(node,f'{{{ns}}}lastmod').text=DATE
ET.indent(tree,space='  ');tree.write(p,encoding='utf-8',xml_declaration=True)
print(json.dumps({'articles':len(records),'hubs':len(urls)-len(records),'new_urls':len(urls)},indent=2))
