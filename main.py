from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client(
    "media_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.all)
async def handler(client, message):

    # 1️⃣ Forward qilingan media → "qiziqarli videolar" topikiga
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward qilingan media topildi → qiziqarli videolar ga yuborilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    # 2️⃣ User noto‘g‘ri joyga yozsa → general ga ko‘chirish
    if (
        message.from_user is not None and
        message.chat.id == GROUP_ID and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)
    ):
        print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga ko'chirilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None
        )
        return

    # 3️⃣ Test /start buyrug‘i
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishlayapti.")

app.run()
