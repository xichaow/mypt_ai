class ValidationError(Exception):
    """Raised when file validation fails"""
    pass


class ImageProcessingError(Exception):
    """Raised when image processing fails"""
    pass


class VisionAPIError(Exception):
    """Raised when OpenAI Vision API fails"""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid"""
    pass