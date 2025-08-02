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

@app.on_message(filters.all)
async def handler(client, message):
    # Forward qilingan media → Qiziqarli videolar
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward qilingan media topildi → qiziqarli videolar ga yuborilyapti.")
        await client.send_message(
            chat_id=GROUP_ID,
            text="",
            reply_to_message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            reply_to_message_id=None,
            thread_id=QIZIQARLI_TOPIC_ID  # send_message yoki copy_message uchun ishlovchi nom bu versiyada o'zgarishi mumkin
        )
        return

    # Noto‘g‘ri joyga yuborilgan user post → General ga
    if (
        message.from_user and
        message.chat.id == GROUP_ID and
        message.is_topic_message and
        (message.text or message.audio or message.video)
    ):
        topic_id = getattr(message, "message_thread_id", None)
        if topic_id == QIZIQARLI_TOPIC_ID:
            print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga ko'chirilyapti.")
            await client.copy_message(
                chat_id=GROUP_ID,
                from_chat_id=GROUP_ID,
                message_id=message.id,
                message_thread_id=None
            )
            return

    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishlayapti.")

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

