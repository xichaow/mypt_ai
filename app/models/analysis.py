from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class FormAnalysisRequest(BaseModel):
    exercise_type: Optional[str] = Field(None, description="Type of exercise (optional)")


class FormAnalysisResponse(BaseModel):
    form_score: int = Field(..., ge=0, le=100, description="Form score from 0-100")
    key_issues: List[str] = Field(..., description="List of key form issues identified")
    coaching_cues: List[str] = Field(..., description="List of short, actionable coaching cues")
    risk_level: Literal["low", "medium", "high"] = Field(..., description="Risk level assessment")
    safety_note: str = Field(..., description="Safety note (1-2 sentences)")
    exercise_type: Optional[str] = Field(None, description="Detected exercise type")


class ErrorResponse(BaseModel):
    detail: str
    error_type: str