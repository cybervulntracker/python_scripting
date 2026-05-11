

from urllib.request import urlopen, Request
from urllib.parse import urlparse
import re


# WEBSITE INPUT


url = input("Enter website URL: ")

# add https if missing
if not url.startswith("http"):
    url = "https://" + url

print("\nAnalyzing website vibes...\n")

try:
    # fake browser header
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # request website
    req = Request(url, headers=headers)

    # get HTML
    response = urlopen(req, timeout=10)

    # convert bytes to text
    html = response.read().decode("utf-8", errors="ignore")

    # lowercase for easier matching
    text = html.lower()

    # -----------------------------
    # KEYWORDS
    # -----------------------------

    startup_words = [
        "ai", "future", "innovation", "creator",
        "community", "modern", "startup",
        "build", "productivity", "next generation"
    ]

    corporate_words = [
        "enterprise", "solutions", "business",
        "global", "trusted", "professional",
        "compliance", "company", "customers"
    ]

    suspicious_words = [
        "win now", "claim bonus", "100% free",
        "urgent", "limited offer", "click here",
        "instant reward", "free money"
    ]

   
    # SCORES
   

    startup_score = 0
    corporate_score = 0
    suspicious_score = 0

    # TEXT ANALYSIS
    for word in startup_words:
        if word in text:
            startup_score += 2

    for word in corporate_words:
        if word in text:
            corporate_score += 2

    for word in suspicious_words:
        if word in text:
            suspicious_score += 3


    # DOMAIN ANALYSIS
  

    domain = urlparse(url).netloc

    weird_domains = [".xyz", ".top", ".buzz", ".click"]

    for ext in weird_domains:
        if domain.endswith(ext):
            suspicious_score += 4

    # random numbers in domain
    if any(char.isdigit() for char in domain):
        suspicious_score += 1


    # HTML PATTERNS


    # lots of buttons
    button_count = text.count("<button")

    if button_count > 15:
        suspicious_score += 3

    
    popup_words = ["popup", "subscribe", "notification"]

    for word in popup_words:
        if word in text:
            suspicious_score += 1

    # startup gradient vibes
    if "gradient" in text:
        startup_score += 2

    # dark mode vibes
    if "#000" in text or "dark" in text:
        startup_score += 1

    # lots of forms = marketing vibes
    form_count = text.count("<form")

    if form_count > 5:
        suspicious_score += 2

    # FINAL RESULT
   

    scores = {
        "Startup Energy ": startup_score,
        "Corporate MNC ": corporate_score,
        "Suspicious Marketing Vibes ": suspicious_score
    }

    final_mood = max(scores, key=scores.get)

    total = sum(scores.values()) + 1

    confidence = int((scores[final_mood] / total) * 100)


    # OUTPUT
  

    print("=" * 50)
    print(" WEBVIBE DETECTOR ")
    print("=" * 50)

    print(f"\nWebsite: {domain}")
    print(f"Mood Detected: {final_mood}")
    print(f"Confidence: {confidence}%\n")

    print("Mood Scores:")
    for mood, score in scores.items():
        print(f"- {mood}: {score}")

    print("\nFun Analysis ")

    if final_mood == "Startup Energy ☕":
        print("✔ Modern tech startup vibes detected")
        print("✔ Probably built with 27 animations")
        print("✔ Founder likely survives on coffee")

    elif final_mood == "Corporate MNC 🏢":
        print("✔ Professional enterprise language found")
        print("✔ Feels like a formal presentation")
        print("✔ Probably has weekly board meetings")

    else:
        print("✔ Aggressive marketing patterns detected")
        print("✔ Website may love popups a bit too much")
        print("✔ Your close button is about to suffer")

except Exception as e:
    print("Something went wrong while scanning ")
    print("Error:", e)