import os
from io import BytesIO
from telethon import TelegramClient, events
from dotenv import load_dotenv
import requests

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
koyeb_app_name = os.getenv("KOYEB_APP_NAME")

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Check if the message is forwarded
    if event.message.fwd_from:
        if event.message.file:
            file_name = event.message.file.name or "file"
            file_bytes = await event.message.download_media()

            # Send the file to Koyeb's upload endpoint
            url = f"https://{koyeb_app_name}.koyeb.app/upload/{file_name}"
            response = requests.post(url, files={file_name: (file_name, BytesIO(file_bytes))})

            if response.status_code == 200:
                # Generate the download link
                download_url = f"https://{koyeb_app_name}.koyeb.app/download/{file_name}"
                await event.reply(f"✅ Forwarded file received!\n🔗 Download link: {download_url}")
            else:
                await event.reply("❌ Failed to forward file. Please try again.")
        else:
            await event.reply("📎 The forwarded message doesn't contain a file.")
    else:
        await event.reply("📎 Please forward a file to get a direct download link.")

client.start()
client.run_until_disconnected()
