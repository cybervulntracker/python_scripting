# WiFi Congestion Visualizer 📡
# Simple terminal-based live network congestion monitor

import os
import time
import platform
import subprocess
import statistics

PING_TARGET = "8.8.8.8"   # Google DNS
MAX_HISTORY = 40

history = []


def ping():
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", PING_TARGET]
    else:
        command = ["ping", "-c", "1", PING_TARGET]

    try:
        result = subprocess.check_output(command).decode()

        if "time=" in result:
            latency = result.split("time=")[-1].split()[0]
            latency = latency.replace("ms", "")
            return float(latency)

    except:
        return None


def get_wave(value):
    if value < 20:
        return "▁"
    elif value < 40:
        return "▂"
    elif value < 60:
        return "▃"
    elif value < 80:
        return "▄"
    elif value < 100:
        return "▅"
    elif value < 150:
        return "▆"
    elif value < 200:
        return "▇"
    else:
        return "█"


while True:
    latency = ping()

    if latency is not None:
        history.append(latency)

        if len(history) > MAX_HISTORY:
            history.pop(0)

        avg = round(statistics.mean(history), 2)

        jitter = 0
        if len(history) > 1:
            diffs = [
                abs(history[i] - history[i - 1])
                for i in range(1, len(history))
            ]
            jitter = round(statistics.mean(diffs), 2)

        wave = "".join(get_wave(x) for x in history)

        os.system("clear" if os.name != "nt" else "cls")

        print(" WiFi Congestion Visualizer\n")

        print(f"Target      : {PING_TARGET}")
        print(f"Latency     : {latency} ms")
        print(f"Average Ping: {avg} ms")
        print(f"Jitter      : {jitter} ms\n")

        print("Network Flow:")
        print(wave)

        print("\nConnection Mood:")

        if jitter < 5:
            print(" Stable")
        elif jitter < 15:
            print(" Slight Congestion")
        elif jitter < 30:
            print(" Network Under Stress")
        else:
            print(" Digital Storm Detected ")

    else:
        print("Connection lost...")

    time.sleep(1)