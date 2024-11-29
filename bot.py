import telebot
import os

bot_token = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)
image_path = 'images/Photo.jpg'
chat_id = None
current_user = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, 'Бот запущен')

def send_image():
    if chat_id and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                bot.send_photo(chat_id, f, caption=f"Фото злостного нарушителя")
        except Exception as e:
            print(f'Ошибка при отправке фото: {e}')