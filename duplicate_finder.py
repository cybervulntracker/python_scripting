"""
DUPLICATE FILE FINDER - Because I kept downloading the same meme 47 times
Author: Someone who finally admitted they have a hoarding problem

You know that feeling when you're looking for a file and find 3 copies of it?
Yeah, me too. This script finds all those sneaky duplicates eating your hard drive space.

How it works: It gives every file a unique fingerprint (like a DNA test for files)
and finds which ones have matching fingerprints = twins!
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

# ============================================
# THE DETECTIVE WORK - Making File Fingerprints
# ============================================

def get_file_fingerprint(filepath, chunk_size=8192):
    """
    Creates a unique fingerprint (hash) for any file
    Think of it like taking a file's DNA sample
    
    Why read in chunks? Because a 4K movie would eat all your RAM otherwise.
    We're smart, not wasteful.
    
    Parameters:
    - filepath: Where the file lives (like "C:/Users/Me/cat_video.mp4")
    - chunk_size: How much to read at once (8KB is the sweet spot)
    """
    
    # Create our fingerprinting tool (MD5 - it's fast and good enough)
    # Yes, I know MD5 isn't secure for passwords. But we're finding DUPLICATES,
    # not protecting nuclear codes. Relax.
    hasher = hashlib.md5()
    
    try:
        # Open the file in binary mode ('rb' = Read Binary)
        # We don't care if it's a cat pic, a Word doc, or a spreadsheet
        # Bytes are bytes - we treat them all the same
        with open(filepath, 'rb') as file:
            # Read the file one bite at a time (like eating a pizza slice by slice)
            while True:
                chunk = file.read(chunk_size)  # Take a bite
                if not chunk:
                    break  # No more pizza... I mean, no more file
                hasher.update(chunk)  # Feed this bite to the fingerprint machine
        
        # Return the fingerprint as a hex string (looks like random letters/numbers)
        # Example: "5d41402abc4b2a76b9719d911017c592"
        # Same file content = same fingerprint. Different content = different fingerprint.
        return hasher.hexdigest()
    
    except PermissionError:
        # Some files Windows is protective about (system files, etc.)
        # We'll just skip them instead of crashing. No big deal.
        return None
    except Exception as e:
        # Something else went wrong - maybe the file was deleted mid-scan?
        # Print a warning but keep going (don't let one bad apple spoil the bunch)
        print(f"  ⚠️ Couldn't read {filepath.name}: {e}")
        return None

# ============================================
# THE MAIN EVENT - Finding All The Twins
# ============================================

def find_duplicates(folder_path, show_progress=True):
    """
    Scans a folder (and all subfolders) to find duplicate files
    This is where the real magic happens
    
    Returns: A list of duplicate groups. Each group contains all the identical files.
    Example: [["cat.jpg", "cat_copy.jpg"], ["resume.pdf", "resume_final.pdf"]]
    """
    
    # This dictionary will store: fingerprint -> list of files with that fingerprint
    # Like a phone book where the number is the fingerprint and the names are files
    files_by_hash = defaultdict(list)
    
    # Get all files in the folder (and subfolders)
    # rglob("*") means "get everything recursively" (all files, anywhere inside)
    all_files = list(Path(folder_path).rglob("*"))
    
    # Filter out folders - we only care about files
    all_files = [f for f in all_files if f.is_file()]
    total_files = len(all_files)
    
    if total_files == 0:
        print("📭 No files found in that folder. Are you sure it exists?")
        return []
    
    print(f"\n🔍 Scanning {total_files} files... This might take a minute")
    print("   (Grab a coffee. Or tea. I don't judge.)\n")
    
    # Scan each file and calculate its fingerprint
    for i, filepath in enumerate(all_files):
        # Show progress so you know it's not frozen
        if show_progress and i % 50 == 0:  # Update every 50 files
            percent = (i / total_files) * 100
            print(f"   Progress: {percent:.1f}% ({i}/{total_files} files)")
        
        # Get the file's unique fingerprint
        fingerprint = get_file_fingerprint(filepath)
        
        if fingerprint:
            # Add this file to our dictionary under its fingerprint
            files_by_hash[fingerprint].append(filepath)
    
    print(f"   Progress: 100%! ({total_files}/{total_files} files)\n")
    
    # Filter out fingerprints that only appear once (not duplicates)
    # We only care about fingerprints with 2 or more files
    duplicates = {fp: files for fp, files in files_by_hash.items() if len(files) > 1}
    
    return duplicates

# ============================================
# SHOWING THE RESULTS (The "Oh no" moment)
# ============================================

def format_size(size_bytes):
    """
    Converts bytes to human-readable format (KB, MB, GB)
    Because nobody wants to see "1048576 bytes" - we say "1 MB"
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"  # If you have terabytes of duplicates... wow

def show_results(duplicates, folder_path):
    """
    Displays the duplicate files in a nice, readable format
    Also calculates how much space you're wasting
    """
    
    if not duplicates:
        print("\n" + "🎉" * 20)
        print("🎉 NO DUPLICATES FOUND! 🎉")
        print("🎉" * 20)
        print("\nYour files are all unique snowflakes. Good job!")
        return
    
    # Calculate total wasted space
    total_wasted = 0
    total_duplicate_groups = len(duplicates)
    total_duplicate_files = sum(len(files) for files in duplicates.values())
    
    print("\n" + "="*70)
    print("🔍 DUPLICATE FILES FOUND! 🔍")
    print("="*70)
    print(f"\n📊 SUMMARY:")
    print(f"   • Found {total_duplicate_groups} groups of duplicate files")
    print(f"   • {total_duplicate_files} total duplicate files (including originals)")
    
    # Show each group of duplicates
    group_num = 1
    for fingerprint, files in duplicates.items():
        # Get the size of the first file (all duplicates are same size)
        file_size = os.path.getsize(files[0])
        wasted_in_group = file_size * (len(files) - 1)  # Keep 1 copy, delete the rest
        total_wasted += wasted_in_group
        
        print(f"\n📁 GROUP {group_num}: {len(files)} identical files")
        print(f"   💾 Each file size: {format_size(file_size)}")
        print(f"   💰 Wasted space: {format_size(wasted_in_group)}")
        print(f"   📋 Files:")
        
        for filepath in files:
            print(f"      • {filepath}")
        
        group_num += 1
        print("   " + "-"*50)
    
    print("\n" + "="*70)
    print(f"💾 TOTAL WASTED SPACE: {format_size(total_wasted)}")
    print("="*70)
    
    # Helpful advice (because I'm nice like that)
    print("\n💡 WHAT NOW?")
    print("   1. Review the duplicates above carefully")
    print("   2. Delete the copies you don't need")
    print("   3. Keep at least ONE copy of each file!")
    print("\n⚠️  WARNING: This script only FINDS duplicates, it doesn't delete them")
    print("   (I don't trust myself with delete buttons either)")

# ============================================
# BONUS: Find Duplicates BY NAME (Faster)
# ============================================

def find_duplicates_by_name(folder_path):
    """
    Quick version: Finds files with the SAME NAME in different folders
    Much faster than fingerprinting, but less accurate
    
    Example: You have "report.pdf" in 3 different folders
    This finds those without checking if content is actually the same
    """
    
    print("\n⚡ Quick scan: Looking for duplicate FILE NAMES...")
    
    # Dictionary to store: filename -> list of paths
    names_dict = defaultdict(list)
    
    for filepath in Path(folder_path).rglob("*"):
        if filepath.is_file():
            names_dict[filepath.name].append(filepath)
    
    # Filter to only names that appear multiple times
    duplicates = {name: paths for name, paths in names_dict.items() if len(paths) > 1}
    
    if duplicates:
        print(f"\n📋 Found {len(duplicates)} filenames that appear multiple times:")
        for name, paths in list(duplicates.items())[:10]:  # Show first 10 only
            print(f"\n   📄 '{name}' appears {len(paths)} times:")
            for path in paths[:3]:  # Show first 3 locations
                print(f"      • {path.parent}")
            if len(paths) > 3:
                print(f"      • ... and {len(paths)-3} more")
    else:
        print("   No duplicate filenames found!")
    
    return duplicates

# ============================================
# INTERACTIVE MODE - Let User Choose
# ============================================

def delete_duplicates_interactive(duplicates):
    """
    Let's the user choose which duplicates to delete
    Because automatically deleting files is a BAD idea (trust me, I've learned)
    """
    
    if not duplicates:
        print("No duplicates to delete!")
        return
    
    print("\n" + "="*70)
    print("🗑️  INTERACTIVE DELETION MODE")
    print("="*70)
    print("\nI'll show you each group of duplicates.")
    print("You choose which ones to keep and which to delete.")
    print("(Don't worry, I won't delete anything without asking)\n")
    
    files_to_delete = []
    
    for group_num, (fingerprint, files) in enumerate(duplicates.items(), 1):
        print(f"\n📁 GROUP {group_num}: {len(files)} identical files")
        
        # Show each file with a number
        for i, filepath in enumerate(files, 1):
            size = format_size(os.path.getsize(filepath))
            print(f"   {i}. {filepath} ({size})")
        
        print(f"\n   Which one do you want to KEEP?")
        print(f"   (Enter number 1-{len(files)}, or 0 to skip this group)")
        
        try:
            choice = int(input("   Your choice: "))
            if 1 <= choice <= len(files):
                # Keep the chosen file, delete the rest
                keep_file = files[choice - 1]
                for filepath in files:
                    if filepath != keep_file:
                        files_to_delete.append(filepath)
                print(f"   ✅ Will keep: {keep_file.name}")
                print(f"   🗑️ Will delete: {len(files)-1} other copies")
            else:
                print("   ⏭️ Skipping this group")
        except ValueError:
            print("   ⏭️ Invalid input, skipping")
    
    # Show summary of what will be deleted
    if files_to_delete:
        print("\n" + "="*70)
        print("📋 SUMMARY OF FILES TO DELETE")
        print("="*70)
        total_saved = sum(os.path.getsize(f) for f in files_to_delete)
        print(f"\n💾 You'll save: {format_size(total_saved)}")
        print(f"🗑️ Files to delete: {len(files_to_delete)}")
        
        print("\n⚠️  LAST CHANCE! Type 'yes' to confirm deletion: ")
        if input().lower() == 'yes':
            for filepath in files_to_delete:
                try:
                    filepath.unlink()  # Delete the file
                    print(f"   ✅ Deleted: {filepath.name}")
                except Exception as e:
                    print(f"   ❌ Couldn't delete {filepath.name}: {e}")
            print("\n🎉 Deletion complete!")
        else:
            print("\n🛑 Deletion cancelled. Your files are safe.")
    else:
        print("\n📭 No files selected for deletion.")

# ============================================
# THE MAIN EVENT - Where Everything Comes Together
# ============================================

def main():
    """
    The main function - asks the user what they want to do
    And then does it (or tries to, at least)
    """
    
    print("="*70)
    print("🔍 DUPLICATE FILE FINDER")
    print("="*70)
    print("\nEver wondered how much space you're wasting on duplicate files?")
    print("This tool finds them for you. No judgment about your 50 selfies.")
    
    # Ask which folder to scan
    print("\n📁 Which folder should I scan?")
    print("   (Press Enter for Desktop, or type a path like C:/Users/Me/Documents)")
    folder_input = input("   Folder path: ").strip()
    
    if not folder_input:
        folder_path = Path.home() / "Desktop"
        print(f"   ✅ Using Desktop: {folder_path}")
    else:
        folder_path = Path(folder_input)
        if not folder_path.exists():
            print(f"❌ Folder '{folder_path}' doesn't exist!")
            return
    
    # Ask which scan method
    print("\n🔍 How do you want to scan?")
    print("   1. Deep scan (slow but accurate - checks file CONTENTS)")
    print("   2. Quick scan (fast but basic - checks only file NAMES)")
    print("   3. Both (do deep scan, then show quick results too)")
    
    choice = input("   Your choice (1/2/3): ").strip()
    
    if choice == "2":
        # Quick scan by name only
        duplicates_by_name = find_duplicates_by_name(folder_path)
        if not duplicates_by_name:
            print("\n💡 Try the deep scan for more accurate results!")
    else:
        # Deep scan by content (or both)
        duplicates = find_duplicates(folder_path)
        show_results(duplicates, folder_path)
        
        # Ask if user wants to delete
        if duplicates:
            print("\n🗑️ Do you want to delete some duplicates? (y/n): ")
            if input().lower() == 'y':
                delete_duplicates_interactive(duplicates)
        
        # If they chose "both", also show quick scan results
        if choice == "3":
            find_duplicates_by_name(folder_path)
    
    print("\n✨ All done! Thanks for using Duplicate File Finder!")
    print("   Remember: Always keep at least one copy of important files!")

# ============================================
# LET'S GO!
# ============================================

if __name__ == "__main__":
    main()