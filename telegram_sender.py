from telegram import Bot
from config import BOT_TOKEN, CHANNEL_ID

bot = Bot(token=BOT_TOKEN)

def send_signal(message, chart_file):
    with open(chart_file, 'rb') as f:
        bot.send_photo(chat_id=CHANNEL_ID, photo=f, caption=message)
