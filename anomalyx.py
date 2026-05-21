# Passive Cybersecurity Scanner 🛡️
# No external installs required
# Uses only built-in Python libraries

import os
import time
import socket
import platform
import subprocess

THREAT_SCORE = 0


# -------------------------------
# CLEAR SCREEN
# -------------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# -------------------------------
# GET ACTIVE NETWORK CONNECTIONS
# -------------------------------
def get_connections():
    connections = []

    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("netstat -n", shell=True).decode()

            for line in output.splitlines():
                if "TCP" in line or "UDP" in line:
                    connections.append(line.strip())

        else:
            output = subprocess.check_output(["netstat", "-tun"]).decode()

            for line in output.splitlines():
                if "tcp" in line or "udp" in line:
                    connections.append(line.strip())

    except:
        pass

    return connections



# GET RUNNING TASKS

def get_processes():
    tasks = []

    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("tasklist", shell=True).decode(errors="ignore")

            for line in output.splitlines()[3:]:
                tasks.append(line.strip())

        else:
            output = subprocess.check_output(["ps", "-e"]).decode()

            for line in output.splitlines()[1:]:
                tasks.append(line.strip())

    except:
        pass

    return tasks



# BASIC NETWORK TEST

def ping_google():
    try:
        start = time.time()

        socket.create_connection(("8.8.8.8", 53), timeout=2)

        end = time.time()

        ping = round((end - start) * 1000, 2)

        return ping

    except:
        return None



# DETECT SUSPICIOUS THINGS

def analyze(processes, connections, ping):

    global THREAT_SCORE

    suspicious_keywords = [
        "temp",
        "powershell",
        "cmd.exe",
        "wscript",
        "unknown"
    ]

    alerts = []

    # Suspicious process names
    for process in processes:

        lower = process.lower()

        for keyword in suspicious_keywords:

            if keyword in lower:
                alerts.append(
                    f"[!] Suspicious process keyword detected -> {keyword}"
                )

                THREAT_SCORE += 10

    # Too many connections
    if len(connections) > 50:
        alerts.append("[!] High number of active network connections detected")
        THREAT_SCORE += 15

    # High ping spike
    if ping and ping > 200:
        alerts.append(f"[!] Unusual network latency detected -> {ping} ms")
        THREAT_SCORE += 10

    return alerts


# -------------------------------
# THREAT LEVEL
# -------------------------------
def threat_level(score):

    if score < 20:
        return "LOW"

    elif score < 50:
        return "MEDIUM"

    else:
        return "HIGH"


# -------------------------------
# MAIN LOOP
# -------------------------------
while True:

    clear()

    print("=" * 55)
    print("      PASSIVE CYBERSECURITY SCANNER 🛡️")
    print("=" * 55)

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    print(f"\nSystem      : {hostname}")
    print(f"Local IP    : {ip}")

    print("\nMonitoring system activity...")
    print("Scanning active processes...")
    print("Analyzing network behavior...\n")

    processes = get_processes()
    connections = get_connections()
    ping = ping_google()

    alerts = analyze(processes, connections, ping)

    print(f"Running Processes    : {len(processes)}")
    print(f"Active Connections   : {len(connections)}")

    if ping:
        print(f"Network Latency      : {ping} ms")
    else:
        print("Network Latency      : OFFLINE")

    print(f"Threat Level         : {threat_level(THREAT_SCORE)}")

    print("\n" + "-" * 55)

    if alerts:

        print("\nALERTS DETECTED 🚨\n")

        for alert in alerts[:10]:
            print(alert)

    else:
        print("\nNo suspicious behavior detected ")

    print("\n" + "-" * 55)

    print("\nRefreshing in 10 seconds...")
    
    time.sleep(10)