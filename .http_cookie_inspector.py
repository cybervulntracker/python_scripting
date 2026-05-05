import requests

TRACKERS = [
    "google-analytics",
    "googletagmanager",
    "doubleclick",
    "facebook.net"
]

KEYWORDS = [
    "collect",
    "third-party",
    "personal data",
    "cookies"
]

def fetch_site(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return None

def check_https(url):
    return url.startswith("https")

def detect_trackers(html):
    found = []
    for tracker in TRACKERS:
        if tracker in html:
            found.append(tracker)
    return found

def keyword_scan(html):
    count = 0
    for word in KEYWORDS:
        if word in html.lower():
            count += 1
    return count

def calculate_score(https, trackers, keyword_count):
    score = 100

    if not https:
        score -= 30

    score -= len(trackers) * 10
    score -= keyword_count * 2

    return max(score, 0)

def main():
    site = input("Enter website: ")

    if not site.startswith("http"):
        site = "https://" + site

    html = fetch_site(site)

    if not html:
        print(" Could not access website")
        return

    https = check_https(site)
    trackers = detect_trackers(html)
    keyword_count = keyword_scan(html)
    score = calculate_score(https, trackers, keyword_count)

    print("\n Privacy Report")
    print("-------------------")
    print(f"Website: {site}")
    print(f"Score: {score}/100")

    print("\nDetails:")
    print(f"HTTPS: {'Yes' if https else 'No'}")
    print(f"Trackers Found: {len(trackers)}")
    print(f"Privacy Keywords: {keyword_count}")

    if score > 70:
        print("\nRisk: Low ")
    elif score > 40:
        print("\nRisk: Medium ")
    else:
        print("\nRisk: High ")

main()