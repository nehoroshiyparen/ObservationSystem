import telebot
import os
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)
chat_id = None
current_user = None

def send_image(image_path):
    if chat_id and os.path.exists(image_path):
        try:
            current_time = datetime.now()
            with open(image_path, 'rb') as f:
                    bot.send_photo(chat_id, f, caption=f"Фото злостного нарушителя")
        except Exception as e:
            print(f'Ошибка при отправке фото: {e}')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, 'Бот запущен')

def run_bot():
     bot.polling(non_stop=True)