from pyrogram import Client
import config  # api_id, api_hash, bot_token shu faylda

app = Client(
    name="media_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN  # MUHIM!
)

@app.on_message(filters.group)
async def route_messages(client: Client, message: Message):
    # 🔁 1. Forward qilingan media — "qiziqarli videolar" topikiga
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        print("📥 Forward qilingan media topildi → qiziqarli videolar ga yuborilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    # ✍️ 2. Guruh a'zosi noto'g'ri joyga yozsa (text/audio/video → qiziqarli videolar)
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
            message_thread_id=None  # General
        )
        return

app.run()
