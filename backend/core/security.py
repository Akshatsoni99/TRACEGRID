import os
import re
from fastapi import HTTPException, UploadFile
from backend.core.config import settings

def validate_uploaded_file(file: UploadFile) -> str:
    """Validate file extension and basic MIME type safely."""
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Allowed extensions are: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Sanitize filename
    clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return clean_name

def check_file_size(content: bytes) -> None:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

