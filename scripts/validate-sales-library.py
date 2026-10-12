from pathlib import Path
from html.parser import HTMLParser
import json,re,csv,xml.etree.ElementTree as ET,hashlib
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.h1=0;self.canonical=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='h1':self.h1+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
rows=list(csv.DictReader((ROOT/'sales-library-index.csv').open()))
assert len(rows)==1000
assert len({x['url'] for x in rows})==1000
assert len({x['title'] for x in rows})==1000
pages=list((ROOT/'blog/sales-playbooks').rglob('index.html'));assert len(pages)==1066
errors=[];wordcounts=[];hashes=set()
for p in pages:
 s=p.read_text();parser=Page();parser.feed(s)
 if parser.h1!=1:errors.append(f'{p}: H1 count')
 url='https://prospectingshow.com/'+str(p.relative_to(ROOT).parent)+'/'
 if parser.canonical!=[url]:errors.append(f'{p}: canonical')
 if re.search(r'real estate|realtor|rental propert|mortgage|property invest',s,re.I):errors.append(f'{p}: excluded subject')
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):json.loads(block)
 for href in parser.links:
  if href.startswith('/') and not href.startswith('//'):
   path=ROOT/href.split('#')[0].lstrip('/')
   if not path.is_file() and not (path/'index.html').is_file():errors.append(f'{p}: missing {href}')
 if '/workflows/' not in str(p) and p.parent.parent.name=='sales-playbooks':continue
 main=s.split('<main class="library">')[1].split('</main>')[0]
 if 'Editorial sales resource' in main:
  text=re.sub('<[^>]+>',' ',main);wordcounts.append(len(text.split()));hashes.add(hashlib.sha256(main.encode()).hexdigest())
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs={x.text.strip() for x in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)}
assert all(x['url'] in locs for x in rows)
assert len(hashes)==1000
if errors:raise SystemExit('\n'.join(errors[:30]))
print(json.dumps({'articles':len(rows),'new_pages':len(pages),'unique_article_bodies':len(hashes),'article_words_min':min(wordcounts),'article_words_max':max(wordcounts),'broken_internal_links':0,'excluded_topic_matches':0,'schema':'valid','sitemap':'all articles included'},indent=2))
