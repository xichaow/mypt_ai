# 🏋️ Gym Exercise Form Coach

A GenAI-powered **Gym Exercise Form Coach** that analyzes user-uploaded photos of workouts and returns PT-style feedback using Vision AI + LLM reasoning.

## ✨ Features

- **🎯 Exercise Form Analysis**: Upload photos and get expert coaching feedback
- **🏃 Multiple Exercise Support**: Squat, Deadlift/RDL, Bench Press, Shoulder Press  
- **🤖 AI-Powered Analysis**: Uses OpenAI GPT-4o Vision API for detailed assessment
- **👨‍⚕️ PT-Style Feedback**: Provides actionable coaching cues and safety recommendations
- **⚠️ Risk Assessment**: Evaluates risk levels with safety notes
- **🌐 Beautiful Web Interface**: Easy-to-use drag & drop interface
- **📱 Mobile Friendly**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation & Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your OpenAI API key:**
```bash
# Edit the .env file and add your API key
OPENAI_API_KEY=your_actual_api_key_here
```

3. **Start the application:**
```bash
uvicorn app.main:app --reload
```

## 🌐 **WHERE TO USE THE APP**

### **Main Web Interface (Recommended)**
**🔗 http://localhost:8000**

Beautiful drag & drop interface where you can:
- **📸 Upload exercise photos** (drag & drop or click)
- **🎯 Select exercise type** (or let AI auto-detect)
- **📊 Get instant feedback** with scores and coaching tips
- **📱 Use on any device** - mobile friendly!

### **API Documentation** 
**🔗 http://localhost:8000/docs**

Interactive API explorer for developers

### **Health Check**
**🔗 http://localhost:8000/health**

Check if the service is running

### Key Endpoints

- `POST /api/v1/analyze` - Analyze exercise form from uploaded image
- `GET /api/v1/health` - Health check
- `GET /api/v1/supported-exercises` - List supported exercise types

### Example Usage

```bash
# Analyze a squat image
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/squat.jpg" \
  -F "exercise_type=squat"
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Linting
ruff check --fix .

# Type checking  
mypy .
```

## Architecture

```
app/
├── main.py              # FastAPI application entry point
├── core/
│   ├── config.py        # Environment variables, API keys
│   └── dependencies.py  # Shared dependencies
├── routers/
│   └── analysis.py      # Exercise analysis endpoints
├── services/
│   ├── vision_service.py     # OpenAI Vision API integration
│   ├── image_service.py      # Image processing utilities
│   └── analysis_service.py   # Form analysis logic
├── models/
│   └── analysis.py      # Pydantic models for request/response
├── utils/
│   ├── validators.py    # File validation utilities
│   └── exceptions.py    # Custom exception classes
tests/
├── test_analysis.py     # Endpoint tests
├── test_vision_service.py    # Service unit tests
└── conftest.py          # Pytest configuration
```

## Response Format

```json
{
  "form_score": 75,
  "key_issues": [
    "Lower back rounding",
    "Knees caving inward"
  ],
  "coaching_cues": [
    "Brace your core harder before descending",
    "Push knees out over toes"
  ],
  "risk_level": "medium",
  "safety_note": "Use a lighter load until depth and spinal alignment become consistent.",
  "exercise_type": "squat"
}
```

## Supported Exercises

- **Squat**: Analyzes depth, knee valgus, back angle, foot stance
- **Deadlift/RDL**: Evaluates bar distance, hip hinge, back neutrality
- **Bench Press**: Checks wrist stacking, elbow angle, scapular position
- **Shoulder Press**: Assesses lumbar arch, elbow path, head/neck alignment

## License

MIT License