import cv2
import torch
import numpy as np

def detect_waste(image, model, recyclable=["plastic", "paper", "glass", "cardboard", "metal"]):
    """Detect and classify waste items in an image."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model(image_rgb)

    labels = results.names
    detections = results.xyxy[0] 
    print(f"[DEBUG] Detected {len(detections)} items")

    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = labels[int(cls)]
        category = "Recyclable" if label.lower() in recyclable else "Non-Recyclable"
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(image, f"{label}: {category} ({conf:.2f})", (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return image, len(detections)

def load_model():
    """Load YOLOv5 model."""
    try:
        model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
        print("[INFO] YOLOv5 model loaded successfully.")
        print("[INFO] Model classes:", model.names)
        return model
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        return None
