import os

def search_directory(directory, target):
    """Recursively search for a directory named target starting from directory"""

    try:
        items = os.listdir(directory)

        # Check if target directory exists in current directory
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                print(f"    📁 Checking directory: {item}")
                if item == target:
                    return item_path
            else:
                pass

        # If not found, recursively search subdirectories
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result = search_directory(item_path, target)
                if result:
                    return result
    except (PermissionError, OSError) as e:
        print(f"    ❌ Permission denied or error in {directory}: {e}")
        pass

    return None

def main(find_item):
    start_dir = os.getcwd()
    print(f"Starting search from: {start_dir}")
    print(f"Looking for directory: {find_item}")

    try:
        items = os.listdir(start_dir)
        for item in sorted(items):
            item_path = os.path.join(start_dir, item)
            if os.path.isdir(item_path):
                print(f"📁 {item}/")
            else:
                pass
    except (PermissionError, OSError) as e:
        print(f"Error listing directory: {e}")
        return

    # Search for the target directory
    print(f"\nSearching for '{find_item}'...")
    found_path = search_directory(start_dir, find_item)

    if found_path:
        print(f"✅ Found directory: {found_path}")
        try:
            os.chdir(found_path)
        except (PermissionError, OSError) as e:
            print(f"Error changing directory to {found_path}: {e}")
    else:
        print(f"❌ Directory '{find_item}' not found in {start_dir} or its subdirectories")

if __name__ == "__main__":
    while True:
        main(input("find: "))