import asyncio
import os
from pyrogram import Client, filters
from flask import Flask
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web = Flask(__name__)

# Bosh sahifaga oddiy javob
@web.route('/')
def home():
    return "Bot ishlayapti! 🚀"

# Foydalanuvchi yozgan xabarni boshqa topikga o'tkazish (notog'ri yozganda)
@app.on_message(filters.chat(GROUP_ID))
async def handle_user_texts(client, message):
    if message.is_topic_message and message.message_thread_id == QIZIQARLI_TOPIC_ID:
        # Agar foydalanuvchi o'zi xabar yuborgan bo‘lsa (media emas)
        if message.from_user and message.text:
            await client.send_message(GROUP_ID, message.text, message_thread_id=None)
            await message.delete()

# Forward qilingan media fayllarni ajratib olish va to'g'ri topikka yuborish
@app.on_message(filters.chat(GROUP_ID) & filters.forwarded)
async def forward_media_to_topic(client, message):
    if message.media:
        await message.copy(GROUP_ID, message_thread_id=QIZIQARLI_TOPIC_ID)
        await message.delete()

# Botni va Flaskni parallel ishga tushurish
async def start_all():
    await app.start()
    print("Bot ishga tushdi.")
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, web.run, "0.0.0.0", 10000)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(start_all())
