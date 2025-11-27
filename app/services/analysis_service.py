from typing import Dict, Optional
from fastapi import UploadFile
from .image_service import ImageProcessingService
from .vision_service import VisionAnalysisService
from ..models.analysis import FormAnalysisResponse
from ..utils.validators import validate_exercise_type
from ..utils.exceptions import ValidationError


class FormAnalysisService:
    def __init__(self):
        self.image_service = ImageProcessingService()
        self.vision_service = VisionAnalysisService()
    
    async def analyze_exercise_form(
        self, 
        file: UploadFile, 
        exercise_type: Optional[str] = None
    ) -> FormAnalysisResponse:
        """Analyze exercise form from uploaded image."""
        
        # Validate exercise type if provided
        if exercise_type and not validate_exercise_type(exercise_type):
            raise ValidationError(f"Unsupported exercise type: {exercise_type}")
        
        # Process image
        image_base64 = await self.image_service.process_upload(file)
        
        # Analyze form using Vision AI
        analysis_result = await self.vision_service.analyze_form(image_base64, exercise_type)
        
        # Add detected exercise type if not provided
        if not exercise_type:
            analysis_result["exercise_type"] = self._detect_exercise_type(analysis_result)
        else:
            analysis_result["exercise_type"] = exercise_type
        
        # Return structured response
        return FormAnalysisResponse(**analysis_result)
    
    def _detect_exercise_type(self, analysis_result: Dict) -> Optional[str]:
        """Attempt to detect exercise type from analysis results."""
        # Simple heuristic based on key issues and coaching cues
        text_content = " ".join(analysis_result.get("key_issues", []) + 
                               analysis_result.get("coaching_cues", [])).lower()
        
        # Look for exercise-specific keywords
        if any(keyword in text_content for keyword in ["squat", "depth", "knee valgus"]):
            return "squat"
        elif any(keyword in text_content for keyword in ["deadlift", "hip hinge", "bar path"]):
            return "deadlift"
        elif any(keyword in text_content for keyword in ["bench", "elbow angle", "chest"]):
            return "bench_press"
        elif any(keyword in text_content for keyword in ["press", "shoulder", "overhead"]):
            return "shoulder_press"
        
        return None