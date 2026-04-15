with open("text.txt", "r") as f:
    content = f.read()

with open("uppercase.txt", "w") as f:
    f.write(content.upper())