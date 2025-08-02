from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client(
    "media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.chat(GROUP_ID))
async def handler(client: Client, message: Message):
    # 1. Forward qilingan media (video, audio, photo, document) → Qiziqarli videolar
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward media topildi → qiziqarli videolar ga yuborilyapti.")
        if message.video:
            await client.send_video(GROUP_ID, video=message.video.file_id, caption=message.caption or "")
        elif message.audio:
            await client.send_audio(GROUP_ID, audio=message.audio.file_id, caption=message.caption or "")
        elif message.photo:
            await client.send_photo(GROUP_ID, photo=message.photo.file_id, caption=message.caption or "")
        elif message.document:
            await client.send_document(GROUP_ID, document=message.document.file_id, caption=message.caption or "")
        return

    # 2. Instagram/Youtube ssilkalar → Qiziqarli videolar
    if message.text and (
        "instagram.com" in message.text.lower() or
        "youtu.be" in message.text.lower() or
        "youtube.com" in message.text.lower()
    ):
        print("🔗 Link topildi → Qiziqarli videolar ga yuborilyapti.")
        await client.send_message(GROUP_ID, text=message.text)
        return

    # 3. Qiziqarli videolar topic ga yozilgan text/audio/video → General ga ko'chirish
    if message.from_user and message.text:
        try:
            if message.chat.id == GROUP_ID and message.reply_to_message:
                replied_topic = message.reply_to_message.message_id  # workaround
                print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga ko'chirilyapti.")
                await client.send_message(GROUP_ID, text=message.text)
                return
        except:
            pass

    # /start komandasi
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishga tushdi.")

# Flask server
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
