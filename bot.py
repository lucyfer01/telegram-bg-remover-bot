import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import io

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, ERROR_MESSAGES
from image_processor import ImageProcessor

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    """Send welcome message when the command /start is issued."""
    logger.info(f"Start command received from user {update.effective_user.id}")
    update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')

def help_command(update: Update, context: CallbackContext):
    """Send help message when the command /help is issued."""
    logger.info(f"Help command received from user {update.effective_user.id}")
    update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')

def process_image(update: Update, context: CallbackContext):
    """Process the uploaded image and remove its background."""
    user_id = update.effective_user.id
    logger.info(f"Processing image request from user {user_id}")

    try:
        # Send processing message
        status_message = update.message.reply_text("⌛ Processing your image...")
        logger.info("Processing status message sent")

        # Get the largest available photo
        photo = update.message.photo[-1]
        logger.info(f"Received photo with file_id: {photo.file_id}")

        # Download the photo
        image_file = context.bot.get_file(photo.file_id)
        image_bytes = image_file.download_as_bytearray()
        logger.info("Successfully downloaded image")

        # Validate image format
        file_extension = image_file.file_path.split('.')[-1].lower()
        logger.info(f"Image file extension: {file_extension}")

        if not ImageProcessor.validate_image_format(f"image/{file_extension}"):
            logger.warning(f"Unsupported image format: {file_extension}")
            status_message.edit_text(ERROR_MESSAGES['unsupported_format'])
            return

        # Process the image
        logger.info("Starting background removal process")
        result = ImageProcessor.remove_background(io.BytesIO(image_bytes))

        if result is None:
            logger.error("Background removal failed")
            status_message.edit_text(ERROR_MESSAGES['api_error'])
            return

        # Send the processed image
        logger.info("Sending processed image back to user")
        context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=io.BytesIO(result),
            filename='background_removed.png',
            caption="✨ Here's your image with the background removed!"
        )

        # Delete the processing status message
        status_message.delete()
        logger.info("Image processing completed successfully")

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        update.message.reply_text(ERROR_MESSAGES['api_error'])

def main():
    """Start the bot."""
    logger.info("Starting the bot")

    # Create the Updater and pass it your bot's token
    updater = Updater(TELEGRAM_TOKEN)
    logger.info("Updater created successfully")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.photo, process_image))
    logger.info("Handlers registered successfully")

    # Start the Bot
    logger.info("Starting bot polling")
    updater.start_polling()
    logger.info("Bot is running")
    updater.idle()

if __name__ == '__main__':
    main()
