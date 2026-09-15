#!/usr/bin/env python3
"""
Single Blocklist Compiler Script
- Reads all domain categories from src/
- Strips protocols, trailing paths, and comments
- Removes exact duplicates (via sets)
- Removes redundant subdomains (if example.com is blocked, ads.example.com is removed)
- Applies exclusions from src/whitelist.txt
- Compiles into a single unified subscription list: dist/blocklist.txt
"""

import os
import re
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
DIST_DIR = os.path.join(BASE_DIR, "dist")

os.makedirs(DIST_DIR, exist_ok=True)

def load_whitelist():
    whitelist = set()
    wl_file = os.path.join(SRC_DIR, "whitelist.txt")
    if os.path.exists(wl_file):
        with open(wl_file, "r", encoding="utf-8") as f:
            for line in f:
                domain = clean_domain(line)
                if domain:
                    whitelist.add(domain)
    return whitelist

def clean_domain(raw_line):
    line = raw_line.strip().lower()
    if not line or line.startswith("#") or line.startswith("!"):
        return None
    line = re.sub(r"^\|\|", "", line)
    line = re.sub(r"\^.*$", "", line)
    line = re.sub(r"^0\.0\.0\.0\s+", "", line)
    line = re.sub(r"^127\.0\.0\.1\s+", "", line)
    line = re.sub(r"^https?://", "", line)
    line = re.sub(r"^www\.", "", line)
    line = line.split("/")[0].split(":")[0].strip()
    if re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", line):
        return line
    return None

def deduplicate_subdomains(domains):
    """
    If 'example.com' is already in domains, removes 'sub.example.com'
    because AdGuard syntax '||example.com^' already blocks all subdomains.
    """
    optimized = set()
    for d in domains:
        parts = d.split(".")
        redundant = False
        # Check all parent suffixes (e.g. for a.b.c.com -> b.c.com, c.com)
        for i in range(1, len(parts) - 1):
            parent = ".".join(parts[i:])
            if parent in domains:
                redundant = True
                break
        if not redundant:
            optimized.add(d)
    return optimized

def main():
    whitelist = load_whitelist()
    print(f"Loaded {len(whitelist)} whitelisted domains.")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    raw_domains = set()
    category_stats = []

    for filename in sorted(os.listdir(SRC_DIR)):
        if not filename.endswith(".txt") or filename == "whitelist.txt":
            continue

        src_path = os.path.join(SRC_DIR, filename)
        count = 0

        with open(src_path, "r", encoding="utf-8") as f:
            for line in f:
                domain = clean_domain(line)
                if domain and domain not in whitelist:
                    raw_domains.add(domain)
                    count += 1

        category_stats.append((filename, count))

    print(f"Total raw domain entries across all categories: {sum(c[1] for c in category_stats)}")
    print(f"Unique domains after removing exact duplicates: {len(raw_domains)}")

    # Remove redundant subdomains
    final_domains = deduplicate_subdomains(raw_domains)
    print(f"Final optimized rules after removing redundant subdomains: {len(final_domains)}")

    # Clean out dist/
    for item in os.listdir(DIST_DIR):
        item_path = os.path.join(DIST_DIR, item)
        if os.path.isfile(item_path):
            os.remove(item_path)

    # Write single unified blocklist
    output_path = os.path.join(DIST_DIR, "blocklist.txt")
    with open(output_path, "w", encoding="utf-8", newline="\n") as out:
        out.write("! Title: DNSfilters Unified Blocklist\n")
        out.write(f"! Updated: {now_utc}\n")
        out.write(f"! Total Rules: {len(final_domains)}\n!\n")
        for domain in sorted(final_domains):
            out.write(f"||{domain}^\n")

    print("\n--- Category Breakdown ---")
    for fname, count in category_stats:
        print(f"  {fname:<25} -> {count} entries")
    print(f"  {'blocklist.txt':<25} -> {len(final_domains)} optimized unique rules")
    print("---------------------------\nBuild completed successfully.")

if __name__ == "__main__":
    main()
