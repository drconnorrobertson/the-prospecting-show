"""Keep reviewed links to existing archive owners after page regeneration."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
sections=json.loads((ROOT/'scripts/discovery-links.json').read_text())
for item in sections:
    page=ROOT/item['file'];text=page.read_text()
    links=[]
    for link in item['links']:
        target=ROOT/link['path'].lstrip('/')/'index.html'
        if not target.is_file():raise ValueError('Missing discovery target: '+link['path'])
        links.append('<li><a href="'+escape(link['path'],quote=True)+'">'+escape(link['label'])+'</a></li>')
    marker='reviewed-discovery:'+item['id']
    block='<!-- '+marker+':start --><section class="section" id="'+escape(item['id'])+'"><div class="container"><h2>'+escape(item['heading'])+'</h2><p>'+escape(item['description'])+'</p><ul>'+''.join(links)+'</ul></div></section><!-- '+marker+':end -->'
    pattern=r'<!-- '+re.escape(marker)+r':start -->.*?<!-- '+re.escape(marker)+r':end -->'
    if re.search(pattern,text,re.S):text=re.sub(pattern,lambda _:block,text,flags=re.S)
    elif '</main>' in text:text=text.replace('</main>',block+'</main>',1)
    elif '<footer' in text:text=text.replace('<footer',block+'<footer',1)
    else:raise ValueError('No content boundary in '+str(page))
    page.write_text(text)
print('Existing archive discovery links verified and applied.')
