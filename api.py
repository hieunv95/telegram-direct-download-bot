from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from telethon import TelegramClient
import io
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

# Set up the FastAPI app
app = FastAPI()

# Create a Telethon client for bot
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Function to download file via MTProto (no local saving)
async def fetch_file(file_id):
    file = await client.download_media(file_id)
    return file

@app.get("/download/{filename}")
async def download_file(filename: str):
    # Get the Telegram file URL using MTProto
    file_id = filename  # Here, we would map filename to file_id (you might store this mapping elsewhere)
    
    file_content = await fetch_file(file_id)

    if file_content:
        return StreamingResponse(io.BytesIO(file_content), media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})
    else:
        raise HTTPException(status_code=404, detail="File not found on Telegram")

