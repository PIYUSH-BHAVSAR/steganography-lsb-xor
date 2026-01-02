from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from io import BytesIO
from typing import Optional
import traceback

# Import steganography functions
from stegano import (
    encrypt_message,
    decrypt_message,
    embed_message,
    extract_encrypted_message
)
from config import MAX_IMAGE_SIZE_MB, ALLOWED_EXTENSIONS, API_PREFIX
from validators import validate_image_file, validate_message, validate_key

app = FastAPI(
    title="StegoSecure API",
    description="Secure image steganography with encryption",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper Functions
def image_bytes_to_binary(image_bytes: bytes):
    """Convert image bytes to binary string"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")
    binary_string = ''.join(format(pixel, '08b') for pixel in image.flatten())
    return binary_string, image.shape

def binary_to_image_bytes(binary_string: str, image_shape: tuple) -> bytes:
    """Convert binary string back to image bytes"""
    pixel_values = [int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8)]
    image_array = np.array(pixel_values, dtype=np.uint8).reshape(image_shape)
    
    # Encode to PNG format in memory
    success, buffer = cv2.imencode('.png', image_array)
    if not success:
        raise ValueError("Failed to encode image")
    
    return buffer.tobytes()

# API Endpoints

@app.get(f"{API_PREFIX}/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "StegoSecure API"
    }

@app.post(f"{API_PREFIX}/encrypt")
async def encrypt_image(
    image: UploadFile = File(...),
    message: str = Form(...),
    key: str = Form(...)
):
    """
    Encrypt a message and embed it into an image using steganography
    
    - **image**: Image file (JPG/PNG, max 5MB)
    - **message**: Secret message to hide
    - **key**: Encryption key
    """
    try:
        # Step 1: Validate inputs
        validate_image_file(image)
        validate_message(message)
        validate_key(key)
        
        # Step 2: Read image into memory
        image_bytes = await image.read()
        
        # Validate size
        if len(image_bytes) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"Image size exceeds {MAX_IMAGE_SIZE_MB}MB limit"
            )
        
        # Step 3: Convert image to binary
        binary_data, shape = image_bytes_to_binary(image_bytes)
        
        # Step 4: Encrypt message
        encrypted_message = encrypt_message(message, key)
        
        # Step 5: Check if message fits in image
        required_bits = 32 + len(encrypted_message)  # 32-bit header + message
        available_bits = len(binary_data) // 8
        
        if required_bits > available_bits:
            raise HTTPException(
                status_code=400,
                detail="Message too large for selected image"
            )
        
        # Step 6: Embed encrypted message
        modified_binary = embed_message(binary_data, encrypted_message)
        
        # Step 7: Convert binary back to image
        stego_image_bytes = binary_to_image_bytes(modified_binary, shape)
        
        # Step 8: Return image as downloadable response
        return StreamingResponse(
            BytesIO(stego_image_bytes),
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=stego_image.png"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Encryption error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Encryption failed: {str(e)}"
        )

@app.post(f"{API_PREFIX}/decrypt")
async def decrypt_image(
    image: UploadFile = File(...),
    key: str = Form(...)
):
    """
    Extract and decrypt a hidden message from a stego image
    
    - **image**: Stego image file (JPG/PNG)
    - **key**: Decryption key
    """
    try:
        # Step 1: Validate inputs
        validate_image_file(image)
        validate_key(key)
        
        # Step 2: Read image into memory
        image_bytes = await image.read()
        
        # Step 3: Convert stego image to binary
        stego_binary, _ = image_bytes_to_binary(image_bytes)
        
        # Step 4: Extract encrypted message
        extracted_encrypted_message = extract_encrypted_message(stego_binary)
        
        # Step 5: Decrypt message
        retrieved_message = decrypt_message(extracted_encrypted_message, key)
        
        # Step 6: Return decrypted message
        return JSONResponse(
            content={
                "status": "success",
                "message": retrieved_message
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid encryption key or corrupted image"
        )
    except Exception as e:
        print(f"Decryption error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Decryption failed: {str(e)}"
        )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "StegoSecure API",
        "docs": "/docs",
        "health": f"{API_PREFIX}/health"
    }
