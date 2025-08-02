from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import threading
import datetime
import config

app = Flask(__name__)
bot = Client(
    "bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Message queue for night caching
cached_messages = []

# Flask web route
@app.route("/")
def index():
    return "Bot is running."

# Bot handler
@bot.on_message(filters.chat(config.GROUP_ID))
async def handle_messages(client, message: Message):
    now = datetime.datetime.now().time()
    is_night = now < datetime.time(7, 0)

    if message.chat.type != "supergroup" or message.message_thread_id is None:
        return

    # Forwarded content from other sources
    if message.forward_from or message.forward_sender_name:
        if message.media:
            await message.copy(config.GROUP_ID, message_thread_id=config.QIZIQARLI_TOPIC_ID)
        elif message.text and ("http" in message.text or "youtu" in message.text or "t.me" in message.text):
            await message.copy(config.GROUP_ID, message_thread_id=config.QIZIQARLI_TOPIC_ID)

    # User sent message to Qiziqarli topic directly
    elif message.message_thread_id == config.QIZIQARLI_TOPIC_ID:
        if is_night:
            cached_messages.append(message)
        else:
            await message.copy(config.GROUP_ID, message_thread_id=0)

# Run Flask in background thread
def run_flask():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run()
