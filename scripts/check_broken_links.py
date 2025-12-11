#!/usr/bin/env python3
"""
Script to check for broken links in the documentation.
This helps with the final QA of the entire site.
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse


def find_markdown_files(docs_dir):
    """Find all markdown files in the docs directory."""
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files


def extract_links(file_path):
    """Extract all links from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex patterns for markdown links and image links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    links = re.findall(link_pattern, content)
    img_links = re.findall(img_pattern, content)

    # Extract just the URLs
    urls = [link[1] for link in links] + [img[1] for img in img_links]

    return urls, file_path


def is_valid_url(url, base_path):
    """Check if a URL is valid (either external or internal)."""
    parsed = urlparse(url)

    # If it's an absolute URL (external)
    if parsed.scheme and parsed.netloc:
        try:
            # Skip certain URLs that might cause issues
            if url.startswith(('mailto:', 'tel:')):
                return True  # Consider these valid

            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code < 400
        except requests.RequestException:
            # Try with GET if HEAD fails
            try:
                response = requests.get(url, timeout=10)
                return response.status_code < 400
            except requests.RequestException:
                return False

    # If it's a relative path (internal)
    else:
        # Resolve relative to the file's directory
        file_dir = os.path.dirname(base_path)
        full_path = os.path.join(file_dir, url)
        # Remove fragments (e.g., #section)
        full_path = full_path.split('#')[0]

        # Check if the file exists
        return os.path.exists(full_path) or os.path.exists(full_path + '.md')


def main():
    """Main function to check for broken links."""
    docs_dir = "docs/docs"

    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist.")
        return

    md_files = find_markdown_files(docs_dir)
    print(f"Found {len(md_files)} markdown files to check for broken links.")

    all_broken_links = []

    for md_file in md_files:
        print(f"\nChecking file: {md_file}")

        urls, file_path = extract_links(md_file)
        broken_links = []

        for url in urls:
            # Skip anchor links (internal page anchors)
            if url.startswith('#'):
                continue

            # Skip relative links that are likely Docusaurus-style internal links
            if url.startswith('/'):
                continue

            if not is_valid_url(url, file_path):
                broken_links.append(url)

        if broken_links:
            print(f"  Found {len(broken_links)} broken links:")
            for link in broken_links:
                print(f"    - {link}")
            all_broken_links.append({
                'file': md_file,
                'links': broken_links
            })
        else:
            print(f"  ✓ No broken links found")

    print(f"\n--- Link Check Summary ---")
    print(f"Files checked: {len(md_files)}")
    print(f"Files with broken links: {len(all_broken_links)}")

    if all_broken_links:
        print(f"\n--- Files with Broken Links ---")
        for item in all_broken_links:
            print(f"File: {item['file']}")
            for link in item['links']:
                print(f"  - {link}")
            print("-" * 40)

    # Return success if no broken links found
    success = len(all_broken_links) == 0
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)