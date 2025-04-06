import os
from telethon import TelegramClient, events
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, HTTPException
import io
import requests

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

# Create FastAPI app for serving the files
app = FastAPI()

# Create a Telethon client for bot
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Function to download files via MTProto
async def download_file_from_telegram(file_id):
    file = await client.download_media(file_id)
    return file

# Handler for new messages (forwarded files)
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.file:
        file_name = event.message.file.name or "file"
        # Generate the public Koyeb URL for downloading
        download_url = f"https://{koyeb_app_name}.koyeb.app/download/{file_name}"

        await event.reply(f"✅ File received and ready for download.\n🔗 Download link: {download_url}")
    else:
        await event.reply("📎 Please send a file to get a direct download link.")

# Run the bot to handle incoming events
client.start()
client.run_until_disconnected()
