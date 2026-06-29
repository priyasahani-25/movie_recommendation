import insightface
import cv2
import numpy as np

class FaceRecognizer:
    def __init__(self):
        # Initialize InsightFace FaceAnalysis app
        # Uses standard 'buffalo_l' model which includes detection and recognition.
        # Since we already crop with YOLO, we just pass the cropped face here, 
        # and InsightFace will re-detect (very quickly on a cropped image) and generate the embedding.
        self.app = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        # det_size can be smaller since we are passing a cropped face
        self.app.prepare(ctx_id=0, det_size=(320, 320))

    def get_embedding(self, face_image):
        """
        Generates a 512-dimensional embedding for the given face image.
        Args:
            face_image: numpy array (BGR format from OpenCV)
        Returns:
            embedding: list of floats representing the embedding, or None
            error_message: string if an error occurred, or None
        """
        faces = self.app.get(face_image)
        
        if len(faces) == 0:
            return None, "InsightFace could not process the face features."
            
        # Return the embedding of the first detected face (should only be one since it's already cropped)
        embedding = faces[0].normed_embedding
        if embedding is None:
            embedding = faces[0].embedding
            
        return embedding.tolist(), None
