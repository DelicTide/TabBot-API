import os
import shutil
import cv2
import numpy as np
import onnxruntime as ort


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f"Tab ({confidence:.2f})"
    color = (0, 255, 0)  # Green for detected tabs
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def preprocess_image(image, target_size=(640, 640)):
    """
    Preprocess the image for YOLOv11:
    - Resize while maintaining aspect ratio.
    - Pad to the target size (640x640).
    - Normalize pixel values to [0, 1].
    """
    original_h, original_w = image.shape[:2]
    target_w, target_h = target_size

    # Resize while maintaining aspect ratio
    scale = min(target_w / original_w, target_h / original_h)
    resized_w = int(original_w * scale)
    resized_h = int(original_h * scale)
    resized_image = cv2.resize(image, (resized_w, resized_h))

    # Pad the resized image to reach the target size
    pad_top = (target_h - resized_h) // 2
    pad_bottom = target_h - resized_h - pad_top
    pad_left = (target_w - resized_w) // 2
    pad_right = target_w - resized_w - pad_left
    padded_image = cv2.copyMakeBorder(
        resized_image, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )

    # Normalize pixel values to [0, 1]
    normalized_image = padded_image.astype(np.float32) / 255.0

    return normalized_image


def process_images(onnx_model, input_folder, with_tabs_folder, without_tabs_folder):
    """
    Process images using the YOLOv11 ONNX model with ONNX Runtime:
    - Detect tabs in each image.
    - Move images to appropriate folders based on detection results.
    """
    # Load the ONNX model with ONNX Runtime
    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]  # Use GPU if available, otherwise CPU
    session = ort.InferenceSession(onnx_model, providers=providers)

    # Get input and output names
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # Create output folders if they don't exist
    os.makedirs(with_tabs_folder, exist_ok=True)
    os.makedirs(without_tabs_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)
        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue  # Skip non-image files

        print(f"Processing: {file_path}")

        original_image = cv2.imread(file_path)
        if original_image is None:
            print(f"Error reading file: {file_path}")
            continue

        # Preprocess the image for YOLOv11 (640x640)
        preprocessed_image = preprocess_image(original_image, target_size=(640, 640))

        # Prepare input tensor
        input_tensor = np.transpose(preprocessed_image, (2, 0, 1))  # HWC to CHW
        input_tensor = np.expand_dims(input_tensor, axis=0)  # Add batch dimension

        # Run inference
        outputs = session.run([output_name], {input_name: input_tensor})[0]

        # Process detections
        tab_detected = False
        for detection in outputs[0]:
            confidence = detection[4]
            if confidence >= 0.51:  # Confidence threshold
                tab_detected = True
                break

        if tab_detected:
            output_path = os.path.join(with_tabs_folder, file_name)
            print(f"Tab detected. Moving {file_name} to {with_tabs_folder}")
        else:
            output_path = os.path.join(without_tabs_folder, file_name)
            print(f"No tab detected. Moving {file_name} to {without_tabs_folder}")

        # Move the image to the appropriate folder
        shutil.move(file_path, output_path)


if __name__ == "__main__":
    # Define paths relative to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, "../")

    onnx_model_path = os.path.join(project_root, "models/best.onnx")
    input_dir = os.path.join(project_root, "static/images")
    with_tabs_dir = os.path.join(input_dir, "with_tabs")
    without_tabs_dir = os.path.join(input_dir, "without_tabs")

    # Process images
    process_images(onnx_model_path, input_dir, with_tabs_dir, without_tabs_dir)