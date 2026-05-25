import socket
import time
import json
import os
import platform



print("=" * 45)
print("        DNSENTINEL ")
print(" DNS Behavior & Trust Analyzer")
print("=" * 45)



trusted_dns = {
    "8.8.8.8": "Google DNS",
    "8.8.4.4": "Google DNS",
    "1.1.1.1": "Cloudflare DNS",
    "1.0.0.1": "Cloudflare DNS",
    "9.9.9.9": "Quad9 DNS",
    "208.67.222.222": "OpenDNS"
}



def get_dns():
    system = platform.system()

    try:
        if system == "Windows":
            import subprocess

            output = subprocess.check_output(
                "ipconfig /all",
                shell=True,
                text=True
            )

            lines = output.splitlines()

            dns_servers = []

            for i, line in enumerate(lines):
                if "DNS Servers" in line:
                    dns = line.split(":")[-1].strip()
                    dns_servers.append(dns)

                    j = i + 1
                    while j < len(lines) and lines[j].startswith(" " * 10):
                        extra = lines[j].strip()
                        if extra:
                            dns_servers.append(extra)
                        j += 1

            return dns_servers

        else:
            
            dns_servers = []

            with open("/etc/resolv.conf", "r") as file:
                for line in file:
                    if line.startswith("nameserver"):
                        dns_servers.append(line.split()[1])

            return dns_servers

    except:
        return []

# Reverse DNS Lookup


def reverse_lookup(ip):
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except:
        return "Unknown"

# Latency Test


def latency_test(ip):
    try:
        start = time.time()

        socket.setdefaulttimeout(2)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 53))

        end = time.time()

        s.close()

        latency = round((end - start) * 1000, 2)

        return latency

    except:
        return None

# Previous DNS History


history_file = "dns_history.json"

def load_old_dns():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_dns(dns):
    with open(history_file, "w") as f:
        json.dump(dns, f)


# Threat Scoring


def calculate_score(ip, trusted, latency, hostname, changed):

    score = 0

    if not trusted:
        score += 25

    if latency is not None and latency > 200:
        score += 15

    if hostname == "Unknown":
        score += 10

    if changed:
        score += 25

    return score

# Main Analysis


current_dns = get_dns()

if not current_dns:
    print("\n[!] Could not detect DNS settings.")
    exit()

old_dns = load_old_dns()

changed = current_dns != old_dns

for dns in current_dns:

    print(f"\n[+] Detected DNS : {dns}")

    # Trusted Check
    trusted = dns in trusted_dns

    if trusted:
        provider = trusted_dns[dns]
    else:
        provider = "Unknown Provider"

    print(f"[+] Provider     : {provider}")

    # Hostname Lookup
    hostname = reverse_lookup(dns)
    print(f"[+] Hostname     : {hostname}")

    # Latency
    latency = latency_test(dns)

    if latency:
        print(f"[+] Response Time: {latency} ms")
    else:
        print("[!] DNS server did not respond")

    # Threat Score
    score = calculate_score(
        dns,
        trusted,
        latency,
        hostname,
        changed
    )

    print(f"[+] Threat Score : {score}/100")

    # Risk Level
    if score <= 20:
        status = "SAFE "

    elif score <= 50:
        status = "SUSPICIOUS "

    else:
        status = "HIGH RISK "

    print(f"[+] Status       : {status}")



if changed and old_dns:
    print("\n[!] ALERT:")
    print("DNS configuration changed recently ⚠")

save_dns(current_dns)



print("\n[+] Recommended Secure DNS Providers:")
print("    Google DNS     : 8.8.8.8")
print("    Cloudflare DNS : 1.1.1.1")
print("    Quad9 DNS      : 9.9.9.9")

print("\n[✓] Scan Completed.")