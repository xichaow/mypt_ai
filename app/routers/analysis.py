from typing import Optional
from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from ..services.analysis_service import FormAnalysisService
from ..models.analysis import FormAnalysisResponse
from ..utils.exceptions import ValidationError, ImageProcessingError, VisionAPIError, ConfigurationError

router = APIRouter(tags=["analysis"])

analysis_service = FormAnalysisService()


@router.post("/analyze", response_model=FormAnalysisResponse)
async def analyze_exercise_form(
    file: UploadFile = File(..., description="Exercise image file"),
    exercise_type: Optional[str] = Form(None, description="Exercise type (optional)")
) -> FormAnalysisResponse:
    """
    Analyze exercise form from uploaded image.
    
    Returns PT-style feedback including:
    - Form score (0-100)
    - Key issues identified
    - Actionable coaching cues
    - Risk level assessment
    - Safety notes
    """
    try:
        result = await analysis_service.analyze_exercise_form(file, exercise_type)
        return result
        
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail={"error_type": "validation_error", "message": str(e)}
        )
    
    except ImageProcessingError as e:
        raise HTTPException(
            status_code=400,
            detail={"error_type": "image_processing_error", "message": str(e)}
        )
    
    except VisionAPIError as e:
        raise HTTPException(
            status_code=503,
            detail={"error_type": "vision_api_error", "message": str(e)}
        )
    
    except ConfigurationError as e:
        raise HTTPException(
            status_code=500,
            detail={"error_type": "configuration_error", "message": str(e)}
        )
    
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={"error_type": "internal_error", "message": "Internal server error"}
        )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "gym-exercise-form-coach"}


@router.get("/supported-exercises")
async def get_supported_exercises():
    """Get list of supported exercise types."""
    from ..utils.validators import SUPPORTED_EXERCISES
    return {"supported_exercises": SUPPORTED_EXERCISES}