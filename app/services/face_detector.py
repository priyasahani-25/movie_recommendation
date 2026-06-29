import os
import requests
import cv2
from ultralytics import YOLO

WEIGHTS_URL = "https://github.com/akanametov/yolo-face/releases/download/1.0.0/yolov8n-face.pt"
WEIGHTS_PATH = "yolov8n-face.pt"

class FaceDetector:
    def __init__(self):
        self._ensure_weights()
        self.model = YOLO(WEIGHTS_PATH)

    def _ensure_weights(self):
        if not os.path.exists(WEIGHTS_PATH):
            print(f"Downloading YOLOv8-Face weights from {WEIGHTS_URL}...")
            response = requests.get(WEIGHTS_URL, stream=True)
            if response.status_code == 200:
                with open(WEIGHTS_PATH, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print("Download complete.")
            else:
                raise Exception(f"Failed to download weights. Status code: {response.status_code}")

    def detect_and_crop(self, image):
        """
        Detects a face in the image and returns the cropped face image.
        Args:
            image: numpy array (BGR format from OpenCV)
        Returns:
            cropped_face: numpy array (BGR format) or None if no face or multiple faces detected.
        """
        results = self.model(image, verbose=False)
        
        # Get bounding boxes
        boxes = results[0].boxes
        
        if len(boxes) == 0:
            return None, "No face detected"
        elif len(boxes) > 1:
            return None, "Multiple faces detected. Please upload an image with a single face."
            
        # Get the first (and only) bounding box coordinates
        box = boxes[0].xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = map(int, box)
        
        # Ensure coordinates are within image boundaries
        h, w = image.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        cropped_face = image[y1:y2, x1:x2]
        return cropped_face, None
