import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.message.file:
        file_name = event.message.file.name or "file"
        file_path = f"downloads/{file_name}"
        await event.message.download_media(file_path)

        download_url = f"https://{koyeb_app_name}.koyeb.app/download/{file_name}"
        await event.reply(f"✅ File saved!\n🔗 Download link: {download_url}")
    else:
        await event.reply("📎 Please send a file to get a direct download link.")

client.start()
client.run_until_disconnected()
