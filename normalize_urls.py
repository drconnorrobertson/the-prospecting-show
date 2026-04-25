#!/usr/bin/env python3
import re
from pathlib import Path

def normalize_urls(urls):
    """Normalize and deduplicate URLs, preferring the newer format."""
    normalized = {}
    
    for url in urls:
        # Normalize LinkedIn URLs to the new format (without trailing slash)
        if 'linkedin.com/in/' in url.lower():
            # Extract the username part
            match = re.search(r'linkedin\.com/in/([^/]+)/?', url, re.IGNORECASE)
            if match:
                username = match.group(1)
                # Use the new format without trailing slash
                key = f"linkedin:{username.lower()}"
                normalized[key] = f"https://www.linkedin.com/in/{username}"
            continue
        
        # For all other URLs, use them as-is
        # Use lowercase version as key to detect duplicates
        key = url.lower()
        normalized[key] = url
    
    return list(normalized.values())

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"sameAs"\s*:\s*\[([^\]]*)\]'
    
    def replace_sameas(match):
        array_content = match.group(1)
        existing_urls = re.findall(r'"(https?://[^"]+)"', array_content)
        
        # Normalize and deduplicate
        normalized = normalize_urls(existing_urls)
        sorted_urls = sorted(normalized)
        
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
        print(f"Normalized: {html_file.relative_to(repo_root)}")

print(f"Total normalized: {updated_count}")
