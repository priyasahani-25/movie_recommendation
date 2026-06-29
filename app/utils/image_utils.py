import cv2
import numpy as np

def decode_image(image_bytes: bytes) -> np.ndarray:
    """
    Decodes an uploaded image file from bytes into an OpenCV format (BGR).
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
