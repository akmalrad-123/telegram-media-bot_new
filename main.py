import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

GENERAL_TOPIC_ID = 1  # Bu siz aytgan General topic ID

app = Client(
    "media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is alive!"

# Faqat user yozgan TEXT, AUDIO, VOICE, VIDEO msg larni Qiziqarli dan Generalga forward
@app.on_message(filters.chat(GROUP_ID) & filters.topic(QIZIQARLI_TOPIC_ID))
async def handle_user_text_in_qiziqarli(client, message: Message):
    if message.forward_from or message.forward_from_chat:
        return  # Forward qilingan media emas — ignore qilamiz
    if message.text or message.video or message.audio or message.voice:
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.id,
            message_thread_id=GENERAL_TOPIC_ID
        )

# Faqat tashqi forward qilingan media fayllarni General dan Qiziqarli ga forward
@app.on_message(filters.chat(GROUP_ID) & filters.topic(GENERAL_TOPIC_ID))
async def handle_forwarded_media_in_general(client, message: Message):
    if message.forward_from_chat or message.forward_from:
        if message.video or message.audio or message.voice or message.photo or message.document:
            await client.copy_message(
                chat_id=GROUP_ID,
                from_chat_id=message.chat.id,
                message_id=message.id,
                message_thread_id=QIZIQARLI_TOPIC_ID
            )

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

def run_bot():
    asyncio.run(main())

async def main():
    await app.start()
    print("🤖 Bot started.")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
