import urllib.request
import urllib.error
import time

def check_domain(domain):
    """
    Check if a domain is working
    Returns: (status, response_time, https_working)
    """

    domain = domain.strip().lower()
    domain = domain.replace('http://', '').replace('https://', '').replace('www.', '')
 
    https_url = f"https://{domain}"
    
    try:
        start = time.time()
        req = urllib.request.Request(https_url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        urllib.request.urlopen(req, timeout=5)
        end = time.time()
        
        response_time = round(end - start, 2)
        return "✅ WORKING", response_time, "Yes"
        
    except urllib.error.HTTPError as e:
        # Website exists but has error (like 404, 403)
        return f"⚠️ ERROR {e.code}", 0, "Yes"
        
    except Exception:
        # Try HTTP as fallback
        try:
            http_url = f"http://{domain}"
            start = time.time()
            req = urllib.request.Request(http_url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            urllib.request.urlopen(req, timeout=5)
            end = time.time()
            
            response_time = round(end - start, 2)
            return "⚠️ HTTP ONLY", response_time, "No"
            
        except:
            return "❌ DOWN/ERROR", 0, "No"

# ============= SIMPLE USAGE =============

# Method 1: Check one domain
print("Checking google.com...")
status, speed, https = check_domain("google.com")
print(f"Status: {status} | Speed: {speed}s | HTTPS: {https}")
print()

# Method 2: Check multiple domains from a list
domains_to_check = [
    "google.com",
    "github.com", 
    "python.org",
    "thiswebsitedoesntexist12345.com"
]

print("DOMAIN HEALTH REPORT")
print("-" * 50)

for domain in domains_to_check:
    print(f"\nChecking {domain}...")
    status, speed, https = check_domain(domain)
    print(f"  Result: {status}")
    print(f"  Speed: {speed} seconds")
    print(f"  Has HTTPS: {https}")

# Method 3: Read from a file (if you have one)
print("\n" + "="*50)
print("TO CHECK DOMAINS FROM A FILE:")
print("-" * 50)
print("1. Create a file called 'domains.txt'")
print("2. Put one domain per line like:")
print("   google.com")
print("   github.com")
print("   yahoo.com")
print()
print("3. Then uncomment this code:")
print("""
# with open('domains.txt', 'r') as f:
#     for line in f:
#         domain = line.strip()
#         if domain:
#             status, speed, https = check_domain(domain)
#             print(f"{domain}: {status} ({speed}s)")
""")