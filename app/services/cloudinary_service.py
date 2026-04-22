import os
import time
from typing import Union
from fastapi import UploadFile
import cloudinary
import cloudinary.uploader

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/jpg"}
ADMIN_MAX_SIZE = 5 * 1024 * 1024  # 5MB
USER_MAX_SIZE = 2 * 1024 * 1024   # 2MB

def upload_image(file: Union[bytes, UploadFile], is_admin: bool = False) -> dict:
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET")
    )

    max_size = ADMIN_MAX_SIZE if is_admin else USER_MAX_SIZE

    # More robust check for UploadFile
    if hasattr(file, "file") and hasattr(file, "content_type"):
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValueError(f"Invalid file type. Allowed types: image/jpeg, image/png, image/jpg")
        
        file_bytes = file.file.read()
        file.file.seek(0)
    else:
        file_bytes = file

    # Ensure file_bytes is a bytes-like object that has len()
    if not isinstance(file_bytes, (bytes, bytearray)):
        raise ValueError(f"Invalid file data. Expected bytes, got {type(file_bytes).__name__}")

    if len(file_bytes) > max_size:
        allowed_mb = max_size // (1024 * 1024)
        raise ValueError(f"File size exceeds limit of {allowed_mb}MB")

    public_id = f"product_{int(time.time())}"

    try:
        result = cloudinary.uploader.upload(
            file_bytes,
            folder="greenify/products",
            public_id=public_id,
            format="webp",
            transformation=[
                {"width": 800, "crop": "limit"},
                {"quality": 70}
            ]
        )
        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }
    except Exception as e:
        raise RuntimeError(f"Cloudinary upload failed: {str(e)}")

def delete_image(public_id: str) -> None:
    cloudinary.config(
        cloud_name=os.getenv("CLOUD_NAME"),
        api_key=os.getenv("API_KEY"),
        api_secret=os.getenv("API_SECRET")
    )
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception:
        pass