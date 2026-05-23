

import urllib.parse
import difflib
import ssl
import socket

# Trusted brands database
trusted_brands = [
    "google",
    "facebook",
    "instagram",
    "amazon",
    "flipkart",
    "paytm",
    "netflix",
    "paypal",
    "microsoft",
    "apple",
    "whatsapp",
    "telegram",
    "discord",
    "steam"
]

# Suspicious keywords
suspicious_words = [
    "login",
    "secure",
    "verify",
    "update",
    "wallet",
    "banking",
    "gift",
    "free",
    "bonus",
    "account"
]


def extract_domain(url):
    parsed = urllib.parse.urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def similarity_check(domain):
    alerts = []

    for brand in trusted_brands:
        similarity = difflib.SequenceMatcher(None, brand, domain).ratio()

        if similarity > 0.55 and brand not in domain:
            alerts.append(f"Looks similar to '{brand}'")

    return alerts


def suspicious_keyword_check(domain):
    found = []

    for word in suspicious_words:
        if word in domain:
            found.append(word)

    return found


def structure_check(domain):
    issues = []


    if domain.count("-") >= 3:
        issues.append("Too many hyphens")

    if len(domain) > 35:
        issues.append("Very long domain name")

    if domain.count(".") >= 4:
        issues.append("Too many subdomains")

    return issues


def ssl_check(domain):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain):
                return True

    except:
        return False


def calculate_score(similarity_alerts, keywords, structure_issues, ssl_valid):
    score = 100

    score -= len(similarity_alerts) * 25
    score -= len(keywords) * 10
    score -= len(structure_issues) * 15

    if not ssl_valid:
        score -= 30

    if score < 0:
        score = 0

    return score


# MAIN

print("=" * 45)
print("      FAKE WEBSITE CLONE DETECTOR")
print("=" * 45)

url = input("\nEnter website URL: ")

if not url.startswith("http"):
    url = "https://" + url

domain = extract_domain(url)

print("\nScanning:", domain)
print("-" * 45)

similarity_alerts = similarity_check(domain)
keywords = suspicious_keyword_check(domain)
structure_issues = structure_check(domain)
ssl_valid = ssl_check(domain)

score = calculate_score(
    similarity_alerts,
    keywords,
    structure_issues,
    ssl_valid
)

# RESULTS

if similarity_alerts:
    print("\n[!] Brand Similarity Alerts")
    for alert in similarity_alerts:
        print(" -", alert)

if keywords:
    print("\n[!] Suspicious Keywords Found")
    for word in keywords:
        print(" -", word)

if structure_issues:
    print("\n[!] Structure Issues")
    for issue in structure_issues:
        print(" -", issue)

print("\n[+] SSL Certificate:", "VALID" if ssl_valid else "INVALID")

print("\n" + "=" * 45)
print("TRUST SCORE :", f"{score}/100")

if score >= 80:
    status = "SAFE "

elif score >= 50:
    status = "SUSPICIOUS "

else:
    status = "POSSIBLE PHISHING "

print("STATUS      :", status)
print("=" * 45)