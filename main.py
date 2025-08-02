 import asyncio
import threading
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# 🔁 Configdan import
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, GENERAL_TOPIC_ID, QIZIQARLI_TOPIC_ID

# Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Flask web server
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running (Render Flask workaround)"

# Ish vaqti: 07:00–00:00
def is_active_hours():
    now = datetime.now().time()
    return now.hour >= 7 or now.hour == 0

# ✉️ Qiziqarli videolarga text yozilsa — Generalga forward qilinadi
@app.on_message(
    filters.chat(GROUP_ID) &
    filters.text &
    filters.topic(QIZIQARLI_TOPIC_ID) &
    ~filters.forwarded
)
async def handle_text_in_video_topic(client: Client, message: Message):
    if is_active_hours():
        await message.forward(chat_id=GROUP_ID, message_thread_id=GENERAL_TOPIC_ID)

# 🎥 Forward qilingan media va linklar — Qiziqarli videolarga yuboriladi
@app.on_message(
    filters.chat(GROUP_ID) &
    filters.forwarded &
    (filters.video | filters.audio | filters.photo | filters.document | filters.text)
)
async def handle_forwarded_media(client: Client, message: Message):
    if is_active_hours():
        if message.message_thread_id != QIZIQARLI_TOPIC_ID:
            await message.forward(chat_id=GROUP_ID, message_thread_id=QIZIQARLI_TOPIC_ID)

# Botni ishga tushirish
def run_bot():
    app.run()

# Flask web server (Render uchun)
def run_web():
    web_app.run(host="0.0.0.0", port=10000)

# Ikkala threadni parallel boshlaymiz
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    threading.Thread(target=run_web).start()

