from fastapi import UploadFile, HTTPException
from config import ALLOWED_EXTENSIONS, MIN_MESSAGE_LENGTH, MIN_KEY_LENGTH

def validate_image_file(file: UploadFile):
    """Validate uploaded image file"""
    if not file:
        raise HTTPException(status_code=400, detail="No image file provided")
    
    # Check file extension
    filename = file.filename.lower()
    if not any(filename.endswith(f".{ext}") for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid content type. Must be JPEG or PNG"
        )

def validate_message(message: str):
    """Validate message content"""
    if not message or len(message.strip()) < MIN_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

def validate_key(key: str):
    """Validate encryption key"""
    if not key or len(key.strip()) < MIN_KEY_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Encryption key cannot be empty"
        )