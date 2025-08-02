from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client(
    "media_forward_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Flask server
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# Message handler
@app.on_message(filters.chat(GROUP_ID) & filters.all)
async def handler(client, message):
    # Check if the message is a forwarded media
    if message.forward_date and (message.video or message.audio or message.photo or message.document or message.text and "instagram.com" in message.text or "youtu" in message.text):
        print("📥 Forward qilingan media yoki link → Qiziqarli videolar ga yuborilmoqda.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.message_id,
            reply_to_message_id=message.id  # fallback if thread not supported
        )
        return

    # Agar user noto‘g‘ri Qiziqarli videolar topikiga yozgan bo‘lsa (text yoki media)
    if (
        message.from_user and
        getattr(message, "forum_topic_id", None) == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)
    ):
        print("↩️ Noto‘g‘ri topikka yozilgan user xabari → General ga ko‘chirilmoqda.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.message_id
        )
        return

    # /start uchun oddiy javob
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("✅ Bot ishga tushgan.")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
