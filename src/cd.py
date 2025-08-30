import os

def search_directory(directory, target):
    """
    Recursively search for a directory named `target` starting from `directory`.
    
    Searches the filesystem depth-first: first checks immediate subdirectories under `directory` for a name match, then recursively searches each subdirectory. Prints progress for each directory checked. PermissionError and OSError while listing a directory are caught, a diagnostic message is printed, and the search continues.
    
    Parameters:
        directory (str): Filesystem path to start searching from.
        target (str): Name of the directory to find.
    
    Returns:
        str or None: The full path to the first found directory named `target`, or None if not found or if an error prevents accessing parts of the tree.
    """

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
    """
    Search for a directory named `find_item` starting from the current working directory, print progress, and if found attempt to change into it.
    
    Displays a sorted list of immediate subdirectories in the current working directory, then performs a recursive search for the first directory whose name matches `find_item`. Prints status messages for start, progress, errors, success, and failure. If the target is found, attempts to change the process's current working directory to the found path; any permission or OS errors are caught and only reported (not raised).
    
    Parameters:
        find_item (str): Name of the directory to locate (matched against directory basenames). The search is case-sensitive and returns the first match found in a depth-first traversal.
    """
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