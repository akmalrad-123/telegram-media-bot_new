from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

# --- Pyrogram Client ---
app = Client(
    "media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Xabarni qayta ishlash ---
@app.on_message(filters.chat(GROUP_ID) & filters.all)
async def handler(client, message):
    # 1️⃣ Boshqa manbadan forward qilingan MEDIA → Qiziqarli videolar topikiga
    if message.forward_date and any([message.video, message.audio, message.photo, message.document]):
        print("📥 Forward qilingan media topildi → qiziqarli videolar ga yuborilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    # 2️⃣ Guruh a'zosi noto'g'ri Qiziqarli videolar topikiga yozgan bo‘lsa → General ga ko‘chirish
    if (
        message.from_user is not None and
        message.chat.id == GROUP_ID and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        any([message.text, message.audio, message.video])
    ):
        print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga ko'chirilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None  # General topic
        )
        return

    # 3️⃣ /start komandasi
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishlayapti.")

# --- Flask server (Render uchun port ochish) ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# --- Botni ishga tushirish ---
if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
