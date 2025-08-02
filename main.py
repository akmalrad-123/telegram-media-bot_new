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

# Bu handler barcha xabarlarni kuzatadi
@app.on_message(filters.all)
async def handler(client, message):
    # 1) Agar bu forwarded media bo‘lsa → Qiziqarli videolarga ko‘chirish
    if message.forward_date and (message.video or message.audio or message.photo or message.document or message.text):
        print("📥 Forward qilingan media yoki ssilka topildi → qiziqarli videolar ga yuborilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.id,
            forum_topic_id=QIZIQARLI_TOPIC_ID
        )
        return

    # 2) Agar bu foydalanuvchi o‘zi yozgan text/video/audio bo‘lsa va noto‘g‘ri Qiziqarli topicda yozgan bo‘lsa → General ga o‘tkazish
    if (
        message.from_user is not None and
        message.chat.id == GROUP_ID and
        message.forum_topic_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)
    ):
        print("↩️ Noto'g'ri topikka yozilgan user xabari → General ga ko'chirilyapti.")
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id
            # General ga o‘tadi → forum_topic_id bermasak bo‘ldi
        )
        return

    # 3) Test komanda
    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishlayapti.")

# --- Flask server ---
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
