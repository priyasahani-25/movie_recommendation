import os
import cv2
import sys

# Ensure the app module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.face_detector import FaceDetector
from app.services.face_recognition import FaceRecognizer
from app.database import get_sync_db

def generate_embeddings():
    faces_dir = "actor_faces"
    
    if not os.path.exists(faces_dir):
        print(f"Error: Directory {faces_dir} not found.")
        return

    print("Initializing models...")
    try:
        detector = FaceDetector()
        recognizer = FaceRecognizer()
    except Exception as e:
        print(f"Failed to initialize models: {e}")
        return

    db = get_sync_db()
    embeddings_col = db["actor_embeddings"]
    embeddings_col.delete_many({}) # Clear existing
    
    actors = [d for d in os.listdir(faces_dir) if os.path.isdir(os.path.join(faces_dir, d))]
    
    if not actors:
        print(f"No actor directories found in {faces_dir}. Please create folders like 'Tom Cruise', 'Brad Pitt' and put images inside them.")
        return

    print(f"Found {len(actors)} actors. Processing images...")

    for actor in actors:
        actor_path = os.path.join(faces_dir, actor)
        images = [f for f in os.listdir(actor_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not images:
            print(f"  Skipping {actor} (no images found)")
            continue
            
        print(f"  Processing {actor} ({len(images)} images)...")
        actor_embeddings = []
        
        for img_name in images:
            img_path = os.path.join(actor_path, img_name)
            img = cv2.imread(img_path)
            
            if img is None:
                print(f"    Warning: Could not read {img_name}")
                continue
                
            # 1. Detect and crop
            cropped, error = detector.detect_and_crop(img)
            if error:
                print(f"    Warning for {img_name}: {error}")
                continue
                
            # 2. Get embedding
            embedding, error = recognizer.get_embedding(cropped)
            if error:
                print(f"    Warning for {img_name}: {error}")
                continue
                
            actor_embeddings.append(embedding)
            
        if actor_embeddings:
            doc = {
                "actor_name": actor,
                "embeddings": actor_embeddings
            }
            embeddings_col.insert_one(doc)
            print(f"    -> Saved {len(actor_embeddings)} embeddings for {actor}.")
        else:
            print(f"    -> Failed to generate any embeddings for {actor}.")

    print("Finished generating embeddings.")

if __name__ == "__main__":
    generate_embeddings()
