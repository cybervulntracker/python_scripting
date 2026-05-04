import os
import re
import argparse

# patterns to catch common sensitive data in commands
patterns = [
    (r'password\s*=\s*\S+', "HIGH", "password usage"),
    (r'-p\S+', "HIGH", "password in flag"),
    (r'api[_-]?key\s*=\s*\S+', "HIGH", "API key"),
    (r'Authorization:\s*Bearer\s+\S+', "HIGH", "auth token"),
    (r'token\s*=\s*\S+', "MEDIUM", "token"),
    (r'[A-Za-z0-9]{20,}', "LOW", "long suspicious string")
]

def scan(file_path):
    # check if file exists before reading
    if not os.path.exists(file_path):
        print("file not found:", file_path)
        return

    total = 0
    results = []

    # read file line by line
    with open(file_path, "r", errors="ignore") as f:
        for line_no, line in enumerate(f, start=1):
            total += 1

    
            for pattern, level, msg in patterns:
                if re.search(pattern, line):
                    results.append((line_no, level, msg, line.strip()))
                    break 

    if not results:
        print("no sensitive data found")
        return

    print("\npossible sensitive entries:\n")

    for line_no, level, msg, content in results:
        print(f"[{level}] line {line_no} -> {msg}")
        print(f"   {content}\n")

    high = sum(1 for r in results if r[1] == "HIGH")
    medium = sum(1 for r in results if r[1] == "MEDIUM")
    low = sum(1 for r in results if r[1] == "LOW")

    print("summary:")
    print("total lines:", total)
    print("matches:", len(results))
    print(f"high: {high}, medium: {medium}, low: {low}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["scan"])
    parser.add_argument("--file", help="custom file path")

    args = parser.parse_args()

  
    path = args.file if args.file else os.path.expanduser("~/.bash_history")

    if args.command == "scan":
        scan(path)


if __name__ == "__main__":
    main()