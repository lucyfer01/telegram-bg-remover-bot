import requests
import logging
from config import REMOVE_BG_API_KEY, SUPPORTED_FORMATS

logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    def validate_image_format(mime_type):
        """Validate if the image format is supported by remove.bg"""
        is_valid = mime_type.lower() in SUPPORTED_FORMATS
        logger.info(f"Image format validation: {mime_type} - {'Valid' if is_valid else 'Invalid'}")
        return is_valid

    @staticmethod
    def remove_background(image_data):
        """Remove background from image using remove.bg API"""
        try:
            logger.info("Sending request to remove.bg API")
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': image_data},
                data={'size': 'auto'},
                headers={'X-Api-Key': REMOVE_BG_API_KEY},
            )
            response.raise_for_status()
            logger.info("Successfully received processed image from remove.bg API")
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in remove.bg API call: {str(e)}")
            return None
