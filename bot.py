import os
import logging
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Fetch environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

# Check if all variables are set
if not api_id or not api_hash or not bot_token or not koyeb_app_name:
    logging.error("Missing environment variables!")
    exit(1)

# Create a Telethon client for bot
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Handler for new messages (forwarded files)
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        if event.message.file:
            file_name = event.message.file.name or "file"
            # Generate the public Koyeb URL for downloading
            download_url = f"https://{koyeb_app_name}.koyeb.app/download/{file_name}"

            # Log the received message and file name
            logging.debug(f"Received file: {file_name}")

            # Respond with the download link
            await event.reply(f"✅ File received and ready for download.\n🔗 Download link: {download_url}")
        else:
            await event.reply("📎 Please send a file to get a direct download link.")
    except Exception as e:
        logging.error(f"Error processing the message: {e}")
        await event.reply(f"⚠️ An error occurred while processing the file: {e}")

# Run the bot to handle incoming events
client.start()
client.run_until_disconnected()
