from PIL import Image
import os

def resize_and_pad(image, target_size=(640, 640)):
    original_w, original_h = image.size
    target_w, target_h = target_size

    scale = min(target_w / original_w, target_h / original_h)
    resized_w = int(original_w * scale)
    resized_h = int(original_h * scale)
    resized_image = image.resize((resized_w, resized_h), Image.Resampling.LANCZOS)

    new_image = Image.new("RGB", target_size, (0, 0, 0))
    paste_x = (target_w - resized_w) // 2
    paste_y = (target_h - resized_h) // 2
    new_image.paste(resized_image, (paste_x, paste_y))

    return new_image

input_dir = "train"  # Replace with your directory
output_dir = "640"  # Replace with your directory

print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")

# Walk through the input directory
for root, dirs, files in os.walk(input_dir):
    print(f"Scanning directory: {root}")
    for file_name in files:
        print(f"Found file: {file_name}")
        if file_name.startswith("._") or not file_name.lower().endswith(".webp"):
            print(f"Skipping: {file_name}")
            continue

        input_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(input_path, input_dir)
        output_path = os.path.join(output_dir, relative_path.replace(".webp", ".jpg"))

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")
                resized_image = resize_and_pad(img, target_size=(640, 640))
                resized_image.save(output_path, "JPEG")
            print(f"Processed: {input_path} -> {output_path}")
        except Exception as e:
            print(f"Failed to process {input_path}: {e}")
