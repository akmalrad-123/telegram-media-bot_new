from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import asyncio
import os

# 🔐 Config
API_ID = 22476589
API_HASH = "97cfc3f9313c7bf03cd69417631d4903"
SESSION_NAME = "media_bot"
GROUP_ID = -1002637326587
TOPIC_ID = 123  # 🔁 Replace with your actual topic ID after testing

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    msg = event.message

    # ✅ Faqat forwarded va media bo'lganlar
    if not msg.forward or not (msg.photo or msg.document or msg.video or msg.audio):
        return

    # ❌ Voice yoki VideoNote bo'lsa chiq
    if msg.voice or msg.video_note:
        return

    try:
        await client.send_message(
            entity=GROUP_ID,
            message=msg.message or "",
            file=msg.media,
            reply_to=TOPIC_ID
        )
        print("✅ Forward qilingan media yuborildi.")
    except Exception as e:
        print("❌ Xato:", e)

async def main():
    print("🚀 Bot ishga tushdi...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
