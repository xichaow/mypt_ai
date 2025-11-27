from fastapi import UploadFile
from .exceptions import ValidationError

ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_EXERCISES = ["squat", "deadlift", "rdl", "bench_press", "shoulder_press"]


def validate_upload_file(file: UploadFile) -> None:
    """Validate uploaded file for type and size constraints."""
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise ValidationError(f"Invalid file type. Supported: {ALLOWED_MIME_TYPES}")
    
    if file.size and file.size > MAX_FILE_SIZE:
        raise ValidationError(f"File too large. Max size: {MAX_FILE_SIZE/1024/1024}MB")


def validate_exercise_type(exercise_type: str) -> bool:
    """Validate if exercise type is supported."""
    if exercise_type is None:
        return True
    return exercise_type.lower() in SUPPORTED_EXERCISES