import os

def find_crust_folder():
    current_dir = os.getcwd()

    while True:
        candidate = os.path.join(current_dir, '.crust')
        if os.path.isdir(candidate):
            return candidate  # Found the .crust folder

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            # Reached the root directory, .crust not found
            return None

        current_dir = parent_dir

if __name__ == "__main__":
    path = find_crust_folder()
    if path:
        print(f"Found .crust folder at: {path}")
    else:
        print("No .crust folder found in current or parent directories.")

