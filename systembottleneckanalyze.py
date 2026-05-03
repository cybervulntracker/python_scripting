import time
from datetime import datetime

log = []

def get_cpu_usage():
    with open("/proc/stat", "r") as f:
        line = f.readline()
        values = list(map(int, line.split()[1:]))
        idle = values[3]
        total = sum(values)
    return idle, total


def calculate_cpu(prev, curr):
    idle_diff = curr[0] - prev[0]
    total_diff = curr[1] - prev[1]
    cpu = 100 * (1 - idle_diff / total_diff)
    return round(cpu, 2)


def get_ram_usage():
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key] = int(value.strip().split()[0])

    total = meminfo["MemTotal"]
    available = meminfo["MemAvailable"]
    used = total - available
    return round((used / total) * 100, 2)

    return round(cpu, 2)


def get_ram_usage():
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key] = int(value.strip().split()[0])

    total = meminfo["MemTotal"]
    available = meminfo["MemAvailable"]
    used = total - available
    return round((used / total) * 100, 2)


def get_top_process():
    try:
        processes = []
        for pid in filter(str.isdigit, __import__("os").listdir("/proc")):
            try:
                with open(f"/proc/{pid}/comm") as f:
                    name = f.read().strip()
                processes.append(name)
            except:
                continue

        return processes[0] if processes else "unknown"
    except:
        return "unknown"


def monitor(duration=60):
    print("Monitoring system...\n")

def get_top_process():
    try:
        processes = []
        for pid in filter(str.isdigit, __import__("os").listdir("/proc")):
            try:
                with open(f"/proc/{pid}/comm") as f:
                    name = f.read().strip()
                processes.append(name)
            except:
                continue

        return processes[0] if processes else "unknown"
    except:
        return "unknown"


def monitor(duration=60):
    print("Monitoring system...\n")

    prev_cpu = get_cpu_usage()

    for _ in range(duration // 3):
        time.sleep(2)
        curr_cpu = get_cpu_usage()

        cpu = calculate_cpu(prev_cpu, curr_cpu)
        ram = get_ram_usage()
        process = get_top_process()

        now = datetime.now().strftime("%H:%M:%S")
        log.append((cpu, ram, process))

        print(f"[{now}] CPU: {cpu}% | RAM: {ram}% | Sample process: {process}")

        prev_cpu = curr_cpu


def analyze():
    cpu_spikes = [x for x in log if x[0] > 75]
    ram_spikes = [x for x in log if x[1] > 80]

    print("\n--- Report ---\n")

    if cpu_spikes:
        print(f"CPU was high {len(cpu_spikes)} times")
    else:
        print("CPU looked stable")

    if ram_spikes:
        print(f"RAM was high {len(ram_spikes)} times")
    else:
        print("RAM looked fine")

    print("\nSuggestions:")

    if cpu_spikes:
        print("- High CPU usage detected, reduce heavy tasks")
    if ram_spikes:
        print("- Memory usage high, close background apps")
    if not cpu_spikes and not ram_spikes:
        print("- System is running smoothly 👍")


monitor(60)
analyze()