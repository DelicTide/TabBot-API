import os
import shutil
import random

# Define paths
project_root = os.getcwd()  # Assumes script is run from project root
pre_batch_dir = os.path.join(project_root, 'pre_batch')
post_batch_dir = os.path.join(project_root, 'post_batch')
output_dir = os.path.join(project_root, 'data')

# Create output directories
output_image_dir = os.path.join(output_dir, 'images')
output_label_dir = os.path.join(output_dir, 'labels')
os.makedirs(os.path.join(output_image_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(output_image_dir, 'val'), exist_ok=True)
os.makedirs(os.path.join(output_image_dir, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_label_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(output_label_dir, 'val'), exist_ok=True)
os.makedirs(os.path.join(output_label_dir, 'test'), exist_ok=True)

# Function to get all batch folders
def get_batch_folders(root_dir):
    return [f for f in os.listdir(root_dir) if f.startswith('batch_') and os.path.isdir(os.path.join(root_dir, f))]

# Get batch folders from both directories
pre_batch_folders = get_batch_folders(pre_batch_dir)
post_batch_folders = get_batch_folders(post_batch_dir)

# Ensure both directories have the same batch folders
if set(pre_batch_folders) != set(post_batch_folders):
    print("Error: Batch folders in /pre_batch and /post_batch do not match.")
    exit(1)

# Collect all matched image and label pairs
matched_files = []

# Iterate through each batch folder
for batch_folder in pre_batch_folders:
    pre_batch_path = os.path.join(pre_batch_dir, batch_folder)
    post_batch_path = os.path.join(post_batch_dir, batch_folder)

    # Get all image files in the pre_batch folder
    image_files = [f for f in os.listdir(pre_batch_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Process each image file
    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]
        txt_file = f"{image_name}.txt"

        # Check if corresponding .txt file exists in post_batch
        txt_path = os.path.join(post_batch_path, txt_file)
        if os.path.exists(txt_path):
            matched_files.append((os.path.join(pre_batch_path, image_file), txt_path))
        else:
            print(f"Removing {image_file} (no corresponding .txt file)")

# Shuffle the matched files to ensure random distribution
random.shuffle(matched_files)

# Split the data into train, val, and test sets
total_files = len(matched_files)
val_size = int(total_files * 0.1)  # 10% for validation
test_size = int(total_files * 0.1)  # 10% for testing
train_size = total_files - val_size - test_size  # Remaining for training

train_files = matched_files[:train_size]
val_files = matched_files[train_size:train_size + val_size]
test_files = matched_files[train_size + val_size:]

# Function to copy files to their respective directories
def copy_files(file_pairs, image_output_dir, label_output_dir):
    for image_path, label_path in file_pairs:
        image_name = os.path.basename(image_path)
        label_name = os.path.basename(label_path)
        shutil.copy(image_path, os.path.join(image_output_dir, image_name))
        shutil.copy(label_path, os.path.join(label_output_dir, label_name))

# Copy files to their respective directories
copy_files(train_files, os.path.join(output_image_dir, 'train'), os.path.join(output_label_dir, 'train'))
copy_files(val_files, os.path.join(output_image_dir, 'val'), os.path.join(output_label_dir, 'val'))
copy_files(test_files, os.path.join(output_image_dir, 'test'), os.path.join(output_label_dir, 'test'))

print(f"Recombination and splitting complete!")
print(f"Total files: {total_files}")
print(f"Training set: {train_size} files")
print(f"Validation set: {val_size} files")
print(f"Test set: {test_size} files")
print(f"Check the 'data' folder for the organized dataset.")