import os
import time
import random


# DIGITAL INSTINCT SYSTEM 


switch_count = 0
last_window = ""

behaviour_data = []
cpu_data = []
memory_data = []
network_data = []

print("\nDIGITAL INSTINCT SYSTEM ")
print("Starting 5-second behavioural scan...\n")

# =====================================
# 5 SECOND SCAN
# =====================================

for second in range(1, 6):

    # Active window
    try:
        current_window = os.popen(
            'powershell "(Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object -First 1).MainWindowTitle"'
        ).read().strip()

    except:
        current_window = "Unknown"

    # App switching detection
    if current_window != last_window and current_window != "":
        switch_count += 1
        last_window = current_window

    # Simulated system metrics
    cpu = random.randint(10, 100)
    memory = random.randint(20, 95)
    network = random.randint(5, 100)

    behaviour_score = random.randint(20, 100)

    # Store values
    behaviour_data.append(behaviour_score)
    cpu_data.append(cpu)
    memory_data.append(memory)
    network_data.append(network)

    # Live scan screen
    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 60)
    print("      DIGITAL INSTINCT SYSTEM ")
    print("=" * 60)

    print(f"\nScanning Second : {second}/5")
    print(f"Current Window  : {current_window}")
    print(f"App Switches    : {switch_count}")

    print("\nReading behavioural signals...")
    print("Analysing system stress...")
    print("Tracking multitasking intensity... ")

    time.sleep(1)

# =====================================
# GRAPH FUNCTION
# =====================================

def graph(data, title):

    print("\n" + title)
    print("-" * 40)

    for value in data:

        bars = "█" * int(value / 4)

        print(str(value).rjust(3), "|", bars)

# FINAL ANALYSIS


avg_behaviour = sum(behaviour_data) // len(behaviour_data)

avg_cpu = sum(cpu_data) // len(cpu_data)
avg_memory = sum(memory_data) // len(memory_data)
avg_network = sum(network_data) // len(network_data)

overall_stress = (avg_cpu + avg_memory + avg_network) // 3

# Behaviour state
if switch_count < 3:
    state = "FOCUSED"

elif switch_count < 6:
    state = "DISTRACTED"

elif switch_count < 10:
    state = "CHAOTIC"

else:
    state = "OVERLOADED"

# Threat state
if overall_stress < 35:
    threat = "SAFE"

elif overall_stress < 60:
    threat = "WATCHFUL"

elif overall_stress < 80:
    threat = "PARANOID"

else:
    threat = "CRITICAL"


# FINAL REPORT


os.system("cls" if os.name == "nt" else "clear")

print("=" * 65)
print("          DIGITAL INSTINCT REPORT ")
print("=" * 65)

print("\nSCAN COMPLETE ")

# Behaviour Analysis
print("\nBehaviour Analysis:")
print(f"• App Switches        : {switch_count}")
print(f"• Behaviour Score     : {avg_behaviour}/100")
print(f"• Behaviour State     : {state}")

# System Analysis
print("\nSystem Stress Analysis:")
print(f"• CPU Stress          : {avg_cpu}%")
print(f"• Memory Stress       : {avg_memory}%")
print(f"• Network Activity    : {avg_network}%")
print(f"• Overall Stress      : {overall_stress}%")

print(f"\nThreat Level          : {threat}")

# AI Insight
print("\nAI Insight:")

if state == "FOCUSED":
    print("> Stable workflow behaviour detected")

elif state == "DISTRACTED":
    print("> Frequent attention shifts observed")

elif state == "CHAOTIC":
    print("> Heavy multitasking intensity detected")

else:
    print("> Cognitive overload suspected 😭")

# Charts
graph(behaviour_data, "Behaviour Fluctuation")
graph(cpu_data, "CPU Stress")
graph(memory_data, "Memory Stress")
graph(network_data, "Network Activity")

print("\nBehavioural scan finished ⚡")