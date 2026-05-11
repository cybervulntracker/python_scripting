import os
import time
from datetime import datetime


# File you want to track
FILE_TO_WATCH = input("Enter file path: ")

# Keeps old modified time
last_modified_time = None

# Counts total changes
change_count = 0


# Small helper for clean logs
def log(message):

    current_time = datetime.now().strftime("%H:%M:%S")

    print(f"[{current_time}] {message}")


print("\nFile Change Tracker Started...")
print(f"Tracking: {FILE_TO_WATCH}")
print("Press CTRL + C to stop.\n")


try:

    # First file timestamp
    last_modified_time = os.path.getmtime(FILE_TO_WATCH)

    while True:

        try:

            # Current modified timestamp
            current_modified_time = os.path.getmtime(FILE_TO_WATCH)

            # File changed
            if current_modified_time != last_modified_time:

                change_count += 1

                log(f"File changed! Total changes: {change_count}")

                # Save latest timestamp
                last_modified_time = current_modified_time

        except FileNotFoundError:

            log("File not found.")

        # Prevents high CPU usage
        time.sleep(1)

except KeyboardInterrupt:

    print("\nTracking stopped.")

    print(f"Final Change Count: {change_count}")