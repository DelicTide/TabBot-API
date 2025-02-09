from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")

# Train the model
train_results = model.train(
    data="detect.yaml",  # path to your dataset YAML file
    epochs=100,  # number of training epochs
    imgsz=640,  # image size for training
    batch=4,  # batch size
    device=0,  # specify GPU (0 = first GPU)
    project="./runs"
)

# Evaluate model performance on the validation set
metrics = model.val()

results = model("data/images/test/", save=True)  # Save results to 'runs/detect/exp'

# Export the model to ONNX format for interoperability
path = model.export(format="onnx")
print(f"Model exported to {path}")

