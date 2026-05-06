#!/usr/bin/env python3

# simple tech stack detector
# idea: just look at headers + page source and guess stuff from patterns

import urllib.request
import urllib.error
import re
import sys


def fetch_website(url):
    # try to get headers + html from the site
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}  # act like a browser
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            headers = dict(response.getheaders())
            html = response.read().decode("utf-8", errors="ignore")
            return headers, html
    except Exception as e:
        print(f"[!] couldn't fetch site: {e}")
        return None, None


def detect_server(headers):
    # most servers expose this directly
    return headers.get("Server", "Unknown")


def detect_backend(headers):
    # sometimes backend leaks here (not always tho)
    return headers.get("X-Powered-By", "Not exposed")


def detect_cdn(headers):
    # super basic cdn hints from headers
    cdn_signatures = {
        "cloudflare": "Cloudflare",
        "cf-ray": "Cloudflare",
        "akamai": "Akamai",
        "fastly": "Fastly",
        "x-cache": "Maybe CDN",
        "via": "Proxy/CDN"
    }

    found = []
    for key, value in headers.items():
        key_lower = key.lower()
        val_lower = str(value).lower()

        for sig in cdn_signatures:
            if sig in key_lower or sig in val_lower:
                found.append(cdn_signatures[sig])

    return list(set(found)) if found else ["Not detected"]


def detect_framework(html):
    # look for common fingerprints in html/js
    patterns = {
        "WordPress": ["wp-content", "wp-includes"],
        "React": ["react", "__next", "data-reactroot"],
        "Next.js": ["_next"],
        "Vue": ["vue", "data-v-"],
        "Angular": ["ng-app", "angular"],
        "Bootstrap": ["bootstrap.css", "bootstrap.min.js"]
    }

    html = html.lower()
    found = []

    for tech, keys in patterns.items():
        for k in keys:
            if k in html:
                found.append(tech)
                break

    return list(set(found)) if found else ["Not detected"]


def detect_generator(html):
  
    match = re.search(r'<meta name="generator" content="([^"]+)"', html, re.I)
    if match:
        return match.group(1)
    return "Not found"


def analyze(url):
    print(f"\n🔍 checking: {url}\n")

    headers, html = fetch_website(url)
    if not headers:
        return

    print(" server:", detect_server(headers))
    print(" backend:", detect_backend(headers))
    print(" cdn:", ", ".join(detect_cdn(headers)))
    print(" frameworks:", ", ".join(detect_framework(html)))
    print(" generator:", detect_generator(html))

    print("\n(note: just guessing based on patterns, not 100% accurate)\n")


if __name__ == "__main__":
    # basic cli usage
    if len(sys.argv) != 2:
        print("usage: python tech_detector.py example.com")
        sys.exit(1)

    url = sys.argv[1]

    # add https if user forgot
    if not url.startswith("http"):
        url = "https://" + url

    analyze(url)