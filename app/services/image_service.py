import base64
import io
from PIL import Image
from fastapi import UploadFile
from ..utils.exceptions import ImageProcessingError, ValidationError
from ..utils.validators import validate_upload_file


class ImageProcessingService:
    @staticmethod
    async def process_upload(file: UploadFile) -> str:
        """Process uploaded file and return base64 encoded string."""
        try:
            # Validate file
            validate_upload_file(file)
            
            # Read file contents
            file_contents = await file.read()
            
            # Open image and validate
            image = Image.open(io.BytesIO(file_contents))
            
            # Resize if necessary (max 2048px on longest side)
            image = ImageProcessingService._resize_image(image)
            
            # Convert to RGB if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=90)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_base64
            
        except ValidationError:
            raise
        except Exception as e:
            raise ImageProcessingError(f"Failed to process image: {str(e)}")
    
    @staticmethod
    def _resize_image(image: Image.Image, max_size: int = 2048) -> Image.Image:
        """Resize image if larger than max_size on any dimension."""
        width, height = image.size
        
        if width <= max_size and height <= max_size:
            return image
        
        # Calculate new size maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int((height * max_size) / width)
        else:
            new_height = max_size
            new_width = int((width * max_size) / height)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def validate_image(file: UploadFile) -> bool:
        """Validate image file format and content."""
        try:
            validate_upload_file(file)
            return True
        except ValidationError:
            return False