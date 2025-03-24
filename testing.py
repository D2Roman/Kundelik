import telebot
from telebot import types

bot = telebot.TeleBot('1599609982:AAHVolDftKg-H5wcdqnkHquvJZIigJeziXI')

chat = '2126407272'

bot.send_message(chat, text="Привет! Я тестовый бот! Предлогаю протеститовать моего собрата (@kundelik_2_0_bot), мало что изменилось, функций не добавилось, но визуально он совсем другой! Оцени его от 1 до 10 и напиши пожелания. Мой создатель думает что это финальная версия, т.к он немного з@еб@лся")
@bot.message_handler(func= lambda message: True)
def starting(message):
    print(message.text)
    a = ['Ты кто?', 'ты кто?', 'Ты кто', 'ты кто']
    if message.text in a:
        sti = 'CAACAgIAAxkBAAKbGWZJ3QoOMsydw0er1b2vFGYC8Mc2AALyDgACUOjoSZyNVkfynpKkNQQ'
        
    else:
        sti = 'CAACAgIAAxkBAAKbG2ZJ3qej5YwCTifWoMTkdcZauSvzAAIZFQACN_0gSGQkrv-VctPpNQQ'
    bot.send_sticker(chat, sti)

bot.polling(none_stop=True, interval=0)