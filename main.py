from pyrogram import Client, filters
import threading
from config import API_ID, API_HASH, BOT_TOKEN, GROUP_ID, QIZIQARLI_TOPIC_ID

app = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "Bot is running"

@app.on_message(filters.all)
async def handler(client, message):
    if message.forward_date and (message.video or message.audio or message.photo or message.document):
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=QIZIQARLI_TOPIC_ID
        )
        return

    if (message.from_user is not None and
        message.chat.id == GROUP_ID and
        message.message_thread_id == QIZIQARLI_TOPIC_ID and
        (message.text or message.audio or message.video)):
        await client.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=GROUP_ID,
            message_id=message.id,
            message_thread_id=None
        )
        return

    if message.text and message.text.lower().startswith("/start"):
        await message.reply("Salom! Bot ishga tushdi.")

def run_web():
    web_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
