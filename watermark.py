
def create_file():
    with open("my_file.txt", "w") as f:
        f.write("This is my secret message.")
    print("✓ File created!")


def add_watermark(owner):
    with open("my_file.txt", "r") as f:      
        content = f.read()
    
    watermark = f"OWNER: {owner}\n\n"        
    
    with open("watermarked_file.txt", "w") as f: 
        f.write(watermark + content)             


create_file()        
add_watermark("John") 