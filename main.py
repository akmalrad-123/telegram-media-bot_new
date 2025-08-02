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

@app.on_message(filters.chat(GROUP_ID) & filters.all)
async def handler(client: Client, message: Message):
    # 1. Forward qilingan MEDIA yoki SSILKA → Qiziqarli videolar topikiga
    if message.forward_date:
        if message.video or message.audio or message.photo or message.document:
            print("📥 Forward qilingan media → qiziqarli videolar.")
            await client.copy_message(
                chat_id=GROUP_ID,
                from_chat_id=GROUP_ID,
                message_id=message.id,
                reply_to_message_id=None  # topic kerak emas
            )
            return
        if message.text and "http" in message.text:
            print("🔗 Forward qilingan link → qiziqarli videolar.")
            await client.send_message(
                chat_id=GROUP_ID,
                text=message.text,
                message_thread_id=QIZIQARLI_TOPIC_ID
            )
            return

    # 2. O'zlari yozgan text/audio/video → noto‘g‘ri joyga yozilgan bo‘lsa → General ga
    if (
        message.from_user is not None and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)
    ):
        print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None
        )
        return

    # /start komandasi
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishga tushdi.")

# --- Flask server ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishga tushdi!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()

