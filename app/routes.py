from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas import HealthResponse, PredictResponse, MovieResponse
from app.utils.validators import validate_image_upload
from app.utils.image_utils import decode_image
from app.services.face_detector import FaceDetector
from app.services.face_recognition import FaceRecognizer
from app.services.embedding_service import EmbeddingService
from app.services.recommender import RecommenderService

router = APIRouter()

# Global instances of AI models
detector = None
recognizer = None

def init_models():
    global detector, recognizer
    print("Initializing YOLO and InsightFace...")
    detector = FaceDetector()
    recognizer = FaceRecognizer()

@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "running"}

@router.post("/predict", response_model=PredictResponse)
async def predict(image: UploadFile = File(...)):
    # 1. Validate Upload
    validate_image_upload(image)
    
    # 2. Decode Image
    try:
        contents = await image.read()
        img = decode_image(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image: {e}")
        
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    # 3. Detect Face
    cropped_face, det_error = detector.detect_and_crop(img)
    if det_error:
        raise HTTPException(status_code=400, detail=det_error)

    # 4. Generate Embedding
    embedding, rec_error = recognizer.get_embedding(cropped_face)
    if rec_error:
        raise HTTPException(status_code=400, detail=rec_error)

    # 5. Compare with Cached Embeddings
    recognized_actor = EmbeddingService.recognize_face(embedding)
    
    if not recognized_actor:
        raise HTTPException(status_code=404, detail="Unknown actor. No match found in the database.")

    # 6. Retrieve Matching Movies
    try:
        movies_data = await RecommenderService.get_movies_by_actor(recognized_actor)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failure.")
        
    if not movies_data:
        raise HTTPException(status_code=404, detail=f"No matching movies found for actor: {recognized_actor}")

    # 7. Return JSON Response
    movies_resp = [
        MovieResponse(
            title=m["title"], 
            rating=m["rating"], 
            genre=m["genre"], 
            year=m["year"]
        ) for m in movies_data
    ]

    return PredictResponse(actor=recognized_actor, movies=movies_resp)
