import requests

def get_metadata(url):
    try:
        
        response = requests.get(url)

        print("\n Metadata for:", url)
        print("Status Code :", response.status_code)

        server = response.headers.get("Server", "Not Available")
        content_type = response.headers.get("Content-Type", "Not Available")

        print("Server      :", server)
        print("Content-Type:", content_type)

    except requests.exceptions.RequestException as e:
        print(" Error:", e)


while True:
    url = input("\nEnter URL (with https://) or 'exit': ").strip()

    if url.lower() == "exit":
        print(" Exiting...")
        break

    get_metadata(url)