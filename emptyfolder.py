import os

FOLDER_PATH = "test_folder"

def find_empty_folders(path):
    empty_folders = []

    for root, dirs, files in os.walk(path, topdown=False):
        if not dirs and not files:
            empty_folders.append(root)

    return empty_folders


def delete_folders(folders):
    for folder in folders:
        try:
            os.rmdir(folder)
            print(f"Deleted: {folder}")
        except Exception as e:
            print(f"Error deleting {folder}: {e}")



empty_folders = find_empty_folders(FOLDER_PATH)

if not empty_folders:
    print(" No empty folders found")
else:
    print(" Empty folders found:\n")
    for f in empty_folders:
        print(f)

    confirm = input("\nDelete these folders? (yes/no): ")

    if confirm.lower() == "yes":
        delete_folders(empty_folders)
        print("\n Cleanup complete")
    else:
        print("\n No folders deleted")