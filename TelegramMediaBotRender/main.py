import json
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, TOPIC_ID

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

QUEUE_FILE = "queue.json"

def is_night_time():
    now = datetime.now().hour
    return not (7 <= now <= 23)

def save_to_queue(message):
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except:
        queue = []

    queue.append({
        "chat_id": message.chat_id,
        "message_id": message.id
    })

    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f)

@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    msg = event.message
    if msg.forward and (msg.photo or msg.video or msg.audio or msg.document) and not (msg.voice or msg.video_note):
        if is_night_time():
            save_to_queue(msg)
        else:
            await client.forward_messages(GROUP_ID, msg.id, msg.chat_id, thread_id=TOPIC_ID)

async def process_queue():
    await client.connect()
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except:
        queue = []

    for item in queue:
        try:
            await client.forward_messages(GROUP_ID, item["message_id"], item["chat_id"], thread_id=TOPIC_ID)
        except:
            pass

    # Clear queue
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

    print("✅ Forward qilingan kechagi media yuborildi.")

with client:
    client.loop.run_until_complete(process_queue())
    print("🚀 Bot ishga tushdi...")
    client.run_until_disconnected()
