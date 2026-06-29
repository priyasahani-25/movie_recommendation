from fastapi import UploadFile, HTTPException

def validate_image_upload(file: UploadFile):
    """
    Validates that the uploaded file is an image.
    """
    if not file:
        raise HTTPException(status_code=400, detail="Empty upload.")
        
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPEG and PNG are supported.")
