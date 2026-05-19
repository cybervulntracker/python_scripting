import psutil
import time

print("=" * 55)
print("   Suspicious Process Activity Monitor")
print("   Monitoring unusual system behavior...")
print("=" * 55)

# Thresholds
CPU_LIMIT = 80
RAM_LIMIT = 500  # in MB

# Common trusted process names
trusted_processes = [
    "chrome.exe",
    "firefox.exe",
    "explorer.exe",
    "system",
    "svchost.exe",
    "python.exe",
    "code.exe",
]

already_alerted = set()

while True:
    print("\nScanning processes...\n")

    for process in psutil.process_iter(
        ['pid', 'name', 'cpu_percent', 'memory_info', 'exe']
    ):
        try:
            pid = process.info['pid']
            name = process.info['name']
            cpu = process.info['cpu_percent']

            # Convert RAM to MB
            ram = process.info['memory_info'].rss / (1024 * 1024)

            exe_path = str(process.info['exe']).lower()

            alerts = []

            
            if cpu > CPU_LIMIT:
                alerts.append(f"High CPU Usage ({cpu}%)")

            
            if ram > RAM_LIMIT:
                alerts.append(f"High RAM Usage ({ram:.0f} MB)")

            # Running from suspicious folders
            suspicious_locations = ["temp", "appdata", "tmp"]

            if any(folder in exe_path for folder in suspicious_locations):
                alerts.append("Running from suspicious location")

            # Unknown process name
            if name and name.lower() not in trusted_processes:
                if cpu > 30 or ram > 200:
                    alerts.append("Unknown process consuming resources")

            # Print alert once
            if alerts:
                unique_id = f"{pid}-{name}"

                if unique_id not in already_alerted:
                    print(f"[!] ALERT DETECTED")
                    print(f"Process : {name}")
                    print(f"PID     : {pid}")
                    print(f"CPU     : {cpu}%")
                    print(f"RAM     : {ram:.0f} MB")

                    for alert in alerts:
                        print(f"Reason  : {alert}")

                    print("-" * 55)

                    already_alerted.add(unique_id)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            continue

    time.sleep(5)