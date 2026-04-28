import hashlib
import os

def calculate_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()


def save_hash(file_path):
    file_hash = calculate_hash(file_path)

    with open("hash.txt", "w") as f:
        f.write(file_hash)

    print("✅ Hash saved successfully!")


def check_file(file_path):
    if not os.path.exists("hash.txt"):
        print("❌ No saved hash found! Run save first.")
        return

    current_hash = calculate_hash(file_path)

    with open("hash.txt", "r") as f:
        saved_hash = f.read()

    print("Saved Hash  :", saved_hash)
    print("Current Hash:", current_hash)

    if current_hash == saved_hash:
        print("✅ File is NOT modified")
    else:
        print("⚠️ File has been modified!")


# -------- LOOP --------
while True:
    file_path = input("\nEnter file path: ").strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print("❌ File not found!")
        continue

    choice = input("Type 'save', 'check' or 'exit': ").lower()

    if choice == "save":
        save_hash(file_path)

    elif choice == "check":
        check_file(file_path)

    elif choice == "exit":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid option!")