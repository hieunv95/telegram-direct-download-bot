from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import io

load_dotenv()

# Fetch environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

app = FastAPI()

# Initialize Telegram client (MTProto API)
client = TelegramClient("bot", api_id, api_hash)

# Connect the client
client.start(bot_token=bot_token)

# Index route to download file using file_id as query parameter
@app.get("/")
async def index(file_id: str):
    try:
        # Download file directly from Telegram servers using MTProto
        file = client.download_media(file_id)

        # Convert file content to bytes (streaming response)
        file_bytes = io.BytesIO(file)
        return StreamingResponse(file_bytes, media_type="application/octet-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching file: {e}")
