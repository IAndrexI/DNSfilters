import urllib.request
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
os.makedirs(SRC_DIR, exist_ok=True)

# Whitelist to protect essential domains
WHITELIST = {
    "apple.com", "icloud.com", "google.com", "gmail.com", "youtube.com",
    "microsoft.com", "windowsupdate.com", "live.com", "github.com",
    "githubusercontent.com", "netflix.com", "nflxvideo.net", "spotify.com",
    "amazon.com", "steampowered.com", "playstation.com", "xboxlive.com",
    "nintendo.com", "cloudflare.com", "quad9.net", "tplinkwifi.net"
}

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

def fetch_domains(url):
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    domains = set()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                d = clean_domain(line)
                if d and d not in WHITELIST:
                    domains.add(d)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    print(f"  -> Found {len(domains)} valid domains")
    return domains

def append_to_file(filename, new_domains, header=""):
    filepath = os.path.join(SRC_DIR, filename)
    existing = set()
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                d = clean_domain(line)
                if d:
                    existing.add(d)
    
    total = existing.union(new_domains)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        if header:
            f.write(f"# ==============================================================================\n")
            f.write(f"# {header}\n")
            f.write(f"# ==============================================================================\n\n")
        for d in sorted(total):
            f.write(f"{d}\n")
    print(f"Updated {filename}: now has {len(total)} domains.")

def main():
    # 1. Adult Ads & Popunders
    adult_domains = set()
    adult_urls = [
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/nsfw.txt"
    ]
    for u in adult_urls:
        adult_domains.update(fetch_domains(u))
    append_to_file("adult-ads.txt", adult_domains, "Adult Advertising & Pop-under Networks")

    # 2. Scams & Malware (Fake shops, scareware, tech support scams)
    scam_domains = set()
    scam_urls = [
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/fake.txt"
    ]
    for u in scam_urls:
        scam_domains.update(fetch_domains(u))
    append_to_file("scam-malware.txt", scam_domains, "Scams, Phishing, Fake Shops & Scareware")

    # 3. Smart TV & Streaming Device Telemetry
    smart_tv_domains = set()
    smart_tv_urls = [
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.samsung.txt",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.lgwebos.txt",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.roku.txt",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/native.amazon.txt"
    ]
    for u in smart_tv_urls:
        smart_tv_domains.update(fetch_domains(u))
    append_to_file("smart-tv.txt", smart_tv_domains, "Smart TV Telemetry (Samsung, LG, Roku, FireTV)")

    # 4. Tracking & Analytics Telemetry
    tracking_domains = set()
    tracking_urls = [
        "https://raw.githubusercontent.com/anudeepND/blacklist/master/adservers.txt"
    ]
    for u in tracking_urls:
        tracking_domains.update(fetch_domains(u))
    append_to_file("tracking-telemetry.txt", tracking_domains, "Advertising & Tracking Telemetry Networks")

    # 5. DoH Bypass Prevention (Ensures devices don't bypass AdGuard)
    doh_domains = set()
    doh_urls = [
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/doh-vpn-proxy-bypass.txt"
    ]
    for u in doh_urls:
        doh_domains.update(fetch_domains(u))
    append_to_file("doh-bypass.txt", doh_domains, "Encrypted DNS / VPN / Bypass Servers")

if __name__ == "__main__":
    main()
