from pyrogram import Client, filters
from flask import Flask
from threading import Thread
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.group)
async def handle_messages(client, message):
    # 1️⃣ Forward qilingan media — Qiziqarli videolar
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward qilingan media → Qiziqarli videolar")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    # 2️⃣ User noto'g'ri topikga yozsa → General ga
    if (
        message.from_user and
        message.chat.id == GROUP_ID and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)
    ):
        print("↩️ User noto'g'ri topikka yozdi → General ga")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None
        )
        return

    # 3️⃣ /start komandasi uchun
    if message.text and message.text.startswith("/start"):
        await message.reply("✅ Bot ishlayapti!")

# --- Flask server ---
flask_app = Flask(__name__)
@flask_app.route('/')
def index():
    return "Bot ishlayapti!"

def run():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    Thread(target=run).start()
    app.run()
