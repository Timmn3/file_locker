import telebot

# Здесь используйте свой token, полученный от BotFather в Telegram
TOKEN = 'TOKEN_FROM_BOTFATHER'
CHAT_ID = '5635586329'  # id чата, куда будет отправляться сообщение

bot = telebot.TeleBot(TOKEN)

def send_password_to_telegram(password):
    try:
        # Отправка пароля
        bot.send_message(chat_id=CHAT_ID, text=f"Ваш шифровальный пароль: {password}")
    except Exception as e:
        print(f"Ошибка при отправке пароля: {e}")

def main():
    # Генерация пароля
    crypt_pass = 'crypt_pass'  # Замените на ваш пароль
    send_password_to_telegram(crypt_pass)

if __name__ == '__main__':
    main()