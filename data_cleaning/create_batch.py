import os
import shutil

# Function to split files into subdirectories
def split_images_into_dirs(source_dir, dest_base_dir, batch_size=100):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return

    # Create the base directory for output
    os.makedirs(dest_base_dir, exist_ok=True)

    # Get a sorted list of all files in the source directory
    files = sorted(os.listdir(source_dir))
    total_files = len(files)
    print(f"Total files found: {total_files}")

    batch_number = 1
    for i in range(0, total_files, batch_size):
        # Determine the start and end of the current batch
        batch_files = files[i:i + batch_size]
        batch_dir = os.path.join(dest_base_dir, f"batch_{batch_number:03d}")

        # Create the directory for the current batch
        os.makedirs(batch_dir, exist_ok=True)

        # Move files into the batch directory
        for file_name in batch_files:
            src_path = os.path.join(source_dir, file_name)
            dest_path = os.path.join(batch_dir, file_name)

            # Only process files (skip directories)
            if os.path.isfile(src_path):
                shutil.move(src_path, dest_path)

        print(f"Batch {batch_number} created with {len(batch_files)} files.")
        batch_number += 1

    print(f"All files have been split into {batch_number - 1} batches.")

# Main function to configure and run the script
if __name__ == "__main__":
    # Set the source directory containing images
    source_directory = "640_padded_data"

    # Set the base destination directory for batches
    destination_base_directory = "batches"

    # Batch size
    batch_size = 100

    # Run the splitting function
    split_images_into_dirs(source_directory, destination_base_directory, batch_size)
