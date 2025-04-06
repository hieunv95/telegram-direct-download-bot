import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from telethon import TelegramClient
from dotenv import load_dotenv
import io

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

# Initialize FastAPI and Telegram client
app = FastAPI()

# Initialize Telegram Client (MTProto API)
client = TelegramClient("bot", api_id, api_hash)

# Connect the Telegram client
client.start(bot_token=bot_token)

@app.get("/")
async def index(file_id: str = None):
    # Check if file_id is present and not empty
    if not file_id:
        logger.debug("file_id is missing or empty, returning welcome message.")
        return {"message": "Welcome! Please provide a valid file_id to download a file."}

    logger.debug(f"Received request with file_id: {file_id}")
    
    try:
        # Await the file download from Telegram using the file_id
        logger.debug(f"Attempting to download file with ID: {file_id}")
        file = await client.download_media(file_id)

        # Check if the file was successfully downloaded
        if not file:
            logger.error(f"Failed to download the file with ID: {file_id}")
            raise HTTPException(status_code=404, detail="File not found on Telegram.")

        # Convert the file into a BytesIO stream to return as a response
        file_bytes = io.BytesIO(file)
        logger.debug(f"File downloaded successfully, returning as streaming response.")
        
        return StreamingResponse(file_bytes, media_type="application/octet-stream")
    
    except Exception as e:
        logger.error(f"Error downloading the file with ID {file_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching file: {e}")
