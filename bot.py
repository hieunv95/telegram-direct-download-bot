import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

# Fetch environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

# Initialize the Telegram client (MTProto API)
client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

# Handler for new messages (forwarded files)
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.file:
        file_id = event.message.file.id  # Use the file ID from the received message
        # Create the URL for file download via Koyeb's FastAPI index route
        download_url = f"https://{koyeb_app_name}.koyeb.app/?file_id={file_id}"

        await event.reply(f"✅ File received! You can download it using this link: \n🔗 {download_url}")
    else:
        await event.reply("📎 Please send a file to get a direct download link.")

# Run the bot to handle incoming events
client.start()
client.run_until_disconnected()
