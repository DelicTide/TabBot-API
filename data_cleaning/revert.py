import os
import shutil

def move_files_to_parent():
    """
    Move all .jpg files from 'with_tabs' and 'without_tabs' subfolders back to the parent directory.
    """
    # Get the current working directory (parent directory)
    parent_dir = os.getcwd()

    # Define subfolder paths
    with_tabs_dir = os.path.join(parent_dir, "with_tabs")
    without_tabs_dir = os.path.join(parent_dir, "without_tabs")

    # Check if subfolders exist
    if not os.path.exists(with_tabs_dir) or not os.path.exists(without_tabs_dir):
        print("Error: 'with_tabs' or 'without_tabs' subfolders not found.")
        return

    # Move files from 'with_tabs'
    for file_name in os.listdir(with_tabs_dir):
        if file_name.lower().endswith(".jpg"):
            file_path = os.path.join(with_tabs_dir, file_name)
            shutil.move(file_path, parent_dir)
            print(f"Moved {file_name} from 'with_tabs' to parent directory.")

    # Move files from 'without_tabs'
    for file_name in os.listdir(without_tabs_dir):
        if file_name.lower().endswith(".jpg"):
            file_path = os.path.join(without_tabs_dir, file_name)
            shutil.move(file_path, parent_dir)
            print(f"Moved {file_name} from 'without_tabs' to parent directory.")

    print("All files moved back to parent directory.")


if __name__ == "__main__":
    # Move files
    move_files_to_parent()