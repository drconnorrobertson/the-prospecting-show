#!/usr/bin/env python3
import re
from pathlib import Path

SOCIAL_URLS = [
    "https://medium.com/@dr.connor.robertson",
    "https://www.linkedin.com/in/dr-connor-robertson",
    "https://x.com/drconnorre",
    "https://youtube.com/@connorrobertsonacquisitions",
    "https://www.threads.com/@creative_acquisitions",
    "https://open.substack.com/pub/drconnorrobertson1",
    "https://open.spotify.com/show/4VDPOlbe2RSSqukaSuYniX",
    "https://podcasts.apple.com/us/podcast/the-prospecting-show-with-dr-connor-robertson/id1488353384",
]

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"sameAs"\s*:\s*\[([^\]]*)\]'
    
    def replace_sameas(match):
        array_content = match.group(1)
        existing_urls = re.findall(r'"(https?://[^"]+)"', array_content)
        all_urls = set(existing_urls + SOCIAL_URLS)
        sorted_urls = sorted(all_urls)
        urls_str = ',\n    '.join(f'"{url}"' for url in sorted_urls)
        return f'"sameAs": [\n    {urls_str}\n  ]'
    
    updated_content = re.sub(pattern, replace_sameas, content, flags=re.DOTALL)
    
    if updated_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    return False

repo_root = '/tmp/the-prospecting-show'
html_files = list(Path(repo_root).rglob('index.html'))

updated_count = 0
for html_file in sorted(html_files):
    if update_file(str(html_file)):
        updated_count += 1
        print(f"Updated: {html_file.relative_to(repo_root)}")

print(f"Total updated: {updated_count}")
