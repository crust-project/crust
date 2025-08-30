import os

def search_directory(directory, target):
    """Iteratively search for a directory named target using BFS with cycle detection"""
    
    # Use a stack for iterative traversal (could also use deque for true BFS)
    stack = [directory]
    visited_inodes = set()
    
    while stack:
        current_dir = stack.pop()
        
        try:
            # Get inode info for cycle detection
            stat_info = os.stat(current_dir)
            inode_key = (stat_info.st_dev, stat_info.st_ino)
            
            # Skip if we've already visited this inode (handles hard links and cycles)
            if inode_key in visited_inodes:
                continue
            visited_inodes.add(inode_key)
            
            # Use os.scandir for better performance
            with os.scandir(current_dir) as entries:
                # First pass: check if target exists in current directory
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        print(f"    📁 Checking directory: {entry.name}")
                        if entry.name == target:
                            return entry.path
                
                # Second pass: add subdirectories to stack for further searching
                # Reset the scandir iterator
                pass
            
            # Rescan for subdirectories to add to stack
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    if entry.is_dir(follow_symlinks=False):
                        # Skip symlinked directories to prevent infinite recursion
                        if entry.is_symlink():
                            print(f"    🔗 Skipping symlinked directory: {entry.name}")
                            continue
                        
                        # Check if we've already visited this inode
                        try:
                            entry_stat = entry.stat(follow_symlinks=False)
                            entry_inode = (entry_stat.st_dev, entry_stat.st_ino)
                            if entry_inode not in visited_inodes:
                                stack.append(entry.path)
                        except (PermissionError, OSError):
                            # Skip directories we can't stat
                            continue
                            
        except (PermissionError, OSError) as e:
            print(f"    ❌ Permission denied or error in {current_dir}: {e}")
            continue
    
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