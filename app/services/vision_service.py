import json
import asyncio
from typing import Dict, Optional
from openai import OpenAI
from ..core.config import settings
from ..utils.exceptions import VisionAPIError, ConfigurationError


class VisionAnalysisService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ConfigurationError("OpenAI API key not configured")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.system_prompt = """You are an expert strength and conditioning coach analyzing exercise form.

CRITICAL: Your response must be ONLY valid JSON, no other text.

Analyze the exercise technique shown and respond with this exact JSON structure:
{
    "form_score": 85,
    "key_issues": ["example issue 1", "example issue 2"],
    "coaching_cues": ["example cue 1", "example cue 2"],
    "risk_level": "low",
    "safety_note": "Example safety guidance."
}

- form_score: integer 0-100
- key_issues: array of specific problems you observe
- coaching_cues: array of actionable improvement tips
- risk_level: must be exactly "low", "medium", or "high"
- safety_note: 1-2 sentence safety recommendation

Focus on posture, alignment, and exercise fundamentals. Be constructive and specific."""

    async def analyze_form(self, image_base64: str, exercise_type: Optional[str] = None) -> Dict:
        """Analyze exercise form using OpenAI Vision API."""
        try:
            # Construct exercise-specific prompt
            prompt = self._construct_prompt(exercise_type)
            
            # Call OpenAI Vision API with retry logic
            response = await self._call_vision_api_with_retry(image_base64, prompt)
            
            # Parse and validate response
            return self._parse_response(response)
            
        except Exception as e:
            if isinstance(e, VisionAPIError):
                raise
            raise VisionAPIError(f"Vision analysis failed: {str(e)}")
    
    def _construct_prompt(self, exercise_type: Optional[str]) -> str:
        """Construct exercise-specific prompt for analysis."""
        base_prompt = self.system_prompt
        
        if exercise_type:
            exercise_guidance = self._get_exercise_guidance(exercise_type.lower())
            base_prompt += f"\n\nFocus specifically on {exercise_type} technique:\n{exercise_guidance}"
        
        return base_prompt
    
    def _get_exercise_guidance(self, exercise_type: str) -> str:
        """Get exercise-specific guidance for analysis."""
        guidance = {
            "squat": """
- Check depth (hip crease below knee cap)
- Assess knee valgus (knees caving inward)
- Evaluate back angle and spinal neutrality
- Check foot stance and weight distribution
- Look for forward lean or chest collapse""",
            
            "deadlift": """
- Assess bar distance from body
- Check hip hinge pattern
- Evaluate back neutrality (no rounding)
- Look at shoulder position over bar
- Check foot positioning and stance""",
            
            "rdl": """
- Evaluate hip hinge movement
- Check back neutrality throughout
- Assess knee bend (slight, not excessive)
- Look at bar path (close to body)
- Check weight shift to heels""",
            
            "bench_press": """
- Assess wrist stacking over elbows
- Check elbow angle (45-75 degrees)
- Evaluate scapular retraction
- Look at arch and leg drive
- Check bar path over chest""",
            
            "shoulder_press": """
- Check lumbar arch (avoid excessive)
- Assess elbow path (straight up)
- Evaluate head and neck alignment
- Look at core bracing
- Check weight distribution in feet"""
        }
        
        return guidance.get(exercise_type, "Focus on general posture, alignment, and safety.")
    
    async def _call_vision_api_with_retry(self, image_base64: str, prompt: str, max_retries: int = 3) -> str:
        """Call OpenAI Vision API with exponential backoff retry."""
        if max_retries <= 0:
            raise VisionAPIError("max_retries must be greater than 0")
            
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}",
                                        "detail": "high"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500,
                    temperature=0.1
                )
                
                return response.choices[0].message.content or ""
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise VisionAPIError(f"OpenAI API failed after {max_retries} attempts: {str(e)}")
                
                # Exponential backoff
                await asyncio.sleep(2 ** attempt)
        
        # This should never be reached due to the exception handling above
        raise VisionAPIError("Unexpected error in retry logic")
    
    def _parse_response(self, response_text: str) -> Dict:
        """Parse and validate OpenAI response."""
        try:
            # Try to extract JSON from response
            response_text = response_text.strip()
            
            # Look for JSON content
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()
            
            data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ["form_score", "key_issues", "coaching_cues", "risk_level", "safety_note"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate data types and ranges
            if not isinstance(data["form_score"], int) or not (0 <= data["form_score"] <= 100):
                raise ValueError("form_score must be integer between 0-100")
            
            if data["risk_level"] not in ["low", "medium", "high"]:
                raise ValueError("risk_level must be 'low', 'medium', or 'high'")
            
            if not isinstance(data["key_issues"], list) or not isinstance(data["coaching_cues"], list):
                raise ValueError("key_issues and coaching_cues must be lists")
            
            return data
            
        except json.JSONDecodeError as e:
            raise VisionAPIError(f"Invalid JSON response from OpenAI: {str(e)}")
        except Exception as e:
            raise VisionAPIError(f"Failed to parse response: {str(e)}")