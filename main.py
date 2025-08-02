from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client(
    "media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.chat(GROUP_ID) & filters.all)
async def handler(client, message):
    # 1️⃣ Forward qilingan media → "Qiziqarli videolar" topic’ga
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward media topildi → qiziqarli videolar ga yuborilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    # 2️⃣ User noto‘g‘ri joyga yozsa (Qiziqarli topic ichida text/video/audio) → General topic’ga ko‘chirish
    if (
        message.from_user and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.video or message.audio)
    ):
        print("↩️ Noto'g'ri topikka yozilgan xabar → General ga ko'chirilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None
        )
        return

    # 3️⃣ /start buyrug‘i
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishlayapti.")

# --- Flask server ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
