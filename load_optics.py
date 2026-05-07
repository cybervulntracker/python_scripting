import urllib.request
import urllib.parse
import re
from html.parser import HTMLParser
from collections import Counter


# Tiny parser to collect website resources like JS, CSS, and images.
class ResourceParser(HTMLParser):
    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.resources = []

    # Checking HTML tags for resource links.
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        resource_url = None

        if tag == 'script' and 'src' in attrs:
            resource_url = attrs['src']

        elif tag == 'link' and 'href' in attrs:
            resource_url = attrs['href']

        elif tag == 'img' and 'src' in attrs:
            resource_url = attrs['src']

        if resource_url:
            full_url = urllib.parse.urljoin(self.base_url, resource_url)
            self.resources.append(full_url)


# Quick way to identify resource types.
# Detect resource type
# --------------------------------------------------
def detect_type(url):
    url = url.lower()

    if '.js' in url:
        return 'JavaScript'
    elif '.css' in url:
        return 'CSS'
    elif any(ext in url for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg']):
        return 'Image'
    elif any(ext in url for ext in ['.woff', '.woff2', '.ttf', '.otf']):
        return 'Font'
    else:
        return 'Other'


# Convert bytes into readable KB / MB sizes.
# Convert bytes into readable size
# --------------------------------------------------
def readable_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"


# Main analyzer logic.
# Main analyzer
# --------------------------------------------------
def analyze_website(url):
    print("\n")
    print(" WEBSITE RESOURCE BREAKDOWN")
    print("\n")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        request = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(request, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')

    except Exception as e:
        print(f"Error loading website: {e}")
        return

    parser = ResourceParser(url)
    parser.feed(html)

    resources = parser.resources

    if not resources:
        print("No resources found.")
        return

    print(f"Website: {url}")
    print(f"Total Resources Found: {len(resources)}\n")

    resource_data = []
    total_size = 0
    type_counter = Counter()

    print("Analyzing resources... This may take a few seconds depending on the website.\n")

    for resource in resources:
        resource_type = detect_type(resource)

        try:
            req = urllib.request.Request(resource, headers=headers)

            with urllib.request.urlopen(req, timeout=5) as res:
                size = res.headers.get('Content-Length')

                if size:
                    size = int(size)
                else:
                    size = 0

        except:
            size = 0

        total_size += size
        type_counter[resource_type] += 1

        resource_data.append({
            'url': resource,
            'type': resource_type,
            'size': size
        })

    # Sort biggest resources first.
    # Sort largest resources
    resource_data.sort(key=lambda x: x['size'], reverse=True)

    print("\n")
    print(" RESOURCE SUMMARY")
    print("\n")

    print(f"Total Estimated Size: {readable_size(total_size)}")

    print("\nResource Types:")

    for rtype, count in type_counter.items():
        print(f"- {rtype}: {count}")

    print("\n=")
    print(" LARGEST RESOURCES")
    print("\n")

    for item in resource_data[:10]:
        print(f"[{item['type']}] {readable_size(item['size'])}")
        print(item['url'])
        print()

    print("")
    print(" PERFORMANCE WARNINGS")
    print("\n")

    if total_size > 5 * 1024 * 1024:
        print("- Heavy website detected (>5 MB)")

    if type_counter['JavaScript'] > 15:
        print("- Too many JavaScript files")

    if type_counter['Image'] > 30:
        print("- Large number of images detected")

    if type_counter['CSS'] > 10:
        print("- Too many CSS files")

    if total_size < 2 * 1024 * 1024:
        print("- Website appears lightweight")

    print("\nDone.\n")


# Program starts here.
# Run program
# --------------------------------------------------
if __name__ == '__main__':
    website = input('Enter website URL: ').strip()

    if not website.startswith('http'):
        website = 'https://' + website

    analyze_website(website)
