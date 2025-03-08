import os

# Telegram Bot Token from environment variable
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Remove.bg API Key from environment variable with fallback
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY", "rw9rYHTtQQsgf3ESGWK2jJ56")

# Supported image formats by remove.bg
SUPPORTED_FORMATS = [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/webp',
    'image/heic'
]

# Welcome message
WELCOME_MESSAGE = """
Welcome to Background Remover Bot developed by *LUCKYONUS*⚡️

I can help you remove backgrounds from your images instantly.
Simply send me a photo and I'll process it for you.

Supported formats: JPEG, PNG, WebP, HEIC
"""

# Error messages
ERROR_MESSAGES = {
    'unsupported_format': "❌ Sorry, this image format is not supported. Please send a JPEG, PNG, WebP, or HEIC image.",
    'api_error': "❌ Sorry, there was an error processing your image. Please try again later.",
    'file_too_large': "❌ The image file is too large. Please send an image smaller than 25MB.",
}
