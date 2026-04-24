import csv

# ------------------------------
# 1. CREATE A SAMPLE CSV FILE
# ------------------------------
csv_filename = "sample.csv"
pipe_filename = "sample_pipe.txt"

# Sample data: name, age, city (with a tricky field containing a comma)
data = [
    ["Alice", "30", "New York"],
    ["Bob", "25", "Los Angeles"],
    ["Charlie", "35", "London, UK"],   # comma inside field -> CSV quoting needed
    ['Diana', '28', 'Paris, France']
]

# Write the CSV file (using csv.writer)
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Age", "City"])   # header
    writer.writerows(data)

print(f" Created sample CSV file: {csv_filename}")
print("Contents of sample.csv:")
with open(csv_filename, 'r', encoding='utf-8') as f:
    print(f.read())

# ------------------------------
# 2. CONVERT CSV TO PIPE-SEPARATED
# ------------------------------
with open(csv_filename, 'r', newline='', encoding='utf-8') as infile, \
     open(pipe_filename, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter='|')   # pipe as delimiter

    for row in reader:
        writer.writerow(row)

print(f"\n Converted to pipe-separated file: {pipe_filename}")
print("Contents of sample_pipe.txt:")
with open(pipe_filename, 'r', encoding='utf-8') as f:
    print(f.read())