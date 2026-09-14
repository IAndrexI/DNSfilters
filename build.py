#!/usr/bin/env python3
"""
Blocklist Compiler Script
- Reads domain sources from src/
- Cleans, strips, de-duplicates, and validates domains
- Applies exclusions from src/whitelist.txt
- Exports AdGuard syntax lists into dist/
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
    # Strip protocols and paths if accidentally pasted
    line = re.sub(r"^https?://", "", line)
    line = re.sub(r"^www\.", "", line)
    line = line.split("/")[0].split(":")[0].strip()
    # Basic domain format validation
    if re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", line):
        return line
    return None

def main():
    whitelist = load_whitelist()
    print(f"Loaded {len(whitelist)} whitelisted domains.")

    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    all_domains = set()
    summary = []

    for filename in sorted(os.listdir(SRC_DIR)):
        if not filename.endswith(".txt") or filename == "whitelist.txt":
            continue

        src_path = os.path.join(SRC_DIR, filename)
        category_domains = set()

        with open(src_path, "r", encoding="utf-8") as f:
            for line in f:
                domain = clean_domain(line)
                if domain and domain not in whitelist:
                    category_domains.add(domain)

        # Write category dist file (AdGuard syntax)
        out_name = filename
        out_path = os.path.join(DIST_DIR, out_name)
        with open(out_path, "w", encoding="utf-8", newline="\n") as out:
            out.write(f"! Title: Custom DNS Blocklist - {filename.replace('.txt', '').title()}\n")
            out.write(f"! Updated: {now_utc}\n")
            out.write(f"! Total Rules: {len(category_domains)}\n!\n")
            for domain in sorted(category_domains):
                out.write(f"||{domain}^\n")

        all_domains.update(category_domains)
        summary.append((filename, len(category_domains)))

    # Write all-in-one compiled list
    all_in_one_path = os.path.join(DIST_DIR, "all-in-one.txt")
    with open(all_in_one_path, "w", encoding="utf-8", newline="\n") as out:
        out.write("! Title: Custom DNS Blocklist - All-in-One\n")
        out.write(f"! Updated: {now_utc}\n")
        out.write(f"! Total Rules: {len(all_domains)}\n!\n")
        for domain in sorted(all_domains):
            out.write(f"||{domain}^\n")

    print("\n--- Compilation Summary ---")
    for fname, count in summary:
        print(f"  {fname:<25} -> {count} rules")
    print(f"  {'all-in-one.txt':<25} -> {len(all_domains)} total unique rules")
    print("---------------------------\nBuild completed successfully.")

if __name__ == "__main__":
    main()
