from dnevnikru import Dnevnik
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import table
import telebot
from telebot import types
import os
import time

matplotlib.use('agg')

bot = telebot.TeleBot('6668462912:AAEXd_oFVLo1jX-Dx1Wo_0MocduXmMiQlHM')

data_file = 'db.txt'
user_sessions = {}

#Класс авторизации
class UserSession:
    def __init__(self, user_id, log, passw):
        self.user_id = user_id
        self.log = log
        self.passw = passw

#Чтение с файла
def read_user_data(user_id):
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            for line in file:
                stored_user_id, log, passw = line.strip().split(',')
                if int(stored_user_id) == user_id:
                    return log, passw
    return None, None
#Запись учетных данных в файл
def write_user_data(user_id, log, passw):
    with open(data_file, 'a') as file:
        file.write(f"{user_id},{log},{passw}\n")

#Многопотоковая авторизация
def perform_action_with_auth(user_id, *args, **kwargs):
    if user_id in user_sessions:
        session = user_sessions[user_id]
        # Передаем данные авторизации в действие
        return session.log, session.passw
    else:
        return "Пожалуйста, авторизуйтесь сначала."

@bot.message_handler(commands=['start'])
def start1(message):
    bot.send_message(message.chat.id, text="Привет! Я тестовый бот Kundelik 2.0")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начнем🎆")
    markup.add(btn1)
    bot.send_message(message.from_user.id,'push button', reply_markup=markup)
    start(message)

# Обработчик авторизации
@bot.message_handler(commands=['auth'])
def auth(message):
    user_id = message.from_user.id
    try:
        _, log, passw = message.text.split()
        if user_id in user_sessions:
            bot.send_message(message.chat.id, "Вы уже авторизованы.")
        else:
            write_user_data(user_id, log, passw)
            user_sessions[user_id] = UserSession(user_id, log, passw)
            bot.send_message(message.chat.id, "Вы успешно авторизовались!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат: /auth логин пароль")


#Main method
@bot.message_handler(regexp='Начнем🎆')
def start(message):
    if message.text == 'Начнем🎆':
        user_id = message.from_user.id
        log, passw = read_user_data(user_id)
        if log and passw:
            user_sessions[user_id] = UserSession(user_id, log, passw)
            bot.send_message(message.chat.id, f"Вы уже авторизованы.")#\nЛогин: {log}\nПароль: {passw}
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton("marks💯")
            btn3 = types.KeyboardButton("homework📚")
            markup.add(btn2, btn3)
            bot.send_message(message.chat.id, text='Выбери действие', reply_markup=markup)                

        else:
            if user_id in user_sessions:
                session = user_sessions[user_id]
                bot.send_message(message.chat.id, f"Вы уже авторизованы.\nЛогин: {session.log}\nПароль: {session.passw}", reply_markup=markup)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn2 = types.KeyboardButton("marks💯")
                btn3 = types.KeyboardButton("homework📚")
                markup.add(btn2, btn3)
                bot.send_message(message.chat.id, text='Выбери действие', reply_markup=markup)
            else: 
                bot.send_message(message.chat.id, "Привет! Пожалуйста, авторизуйтесь с помощью команды /auth логин пароль")
    else: 
        starting(message)

#Marks
def mark(message, dairy):
    marks = dairy.marks()
    columns = ['№', 'Предметы', 'Отметки', 'Опоздания', 'Всего Пропусков', 'По болезни', 'СОР 1', 'СОР 2', 
          'СОР 3', 'СОР 4', 'СОЧ', 'СОР + ФО%', 'СОЧ%', 'Сумма', 'Итог']

    for i in marks:
        i[2] = str(i[2])
        new = ''
        for j in range(1, len(str(i[2]))):
            if i[2][j - 1] != '1' and i[2][j - 1] != '0' and i[2][j] != '0':
                new = new + str(i[2][j - 1]) + " "
            elif i[2][j - 1] == '1' and i[2][j] == '0':
                new = new + str(i[2][j - 1]) + str(i[2][j]) + " "
            elif i[2][j - 1] != '0': new = new + str(i[2][j - 1])
        i[2] = new
    main_table(message, marks, columns, name_of='marks')
#Homework
def view_home(message, day, dairy):
    homework = dairy.homework(days=day)
    b = []
    for i in homework['homework']:
        a = []
        a.append(i[2])
        a.append(i[0])
        a.append(i[1])
        b.append(a)
    th = ['Предмет', "ДЗ", "Урок"]
    td = b
    main_table(message, td, th, name_of='homework')

def meg(message):
    a = ['/marks', 'marks💯', 'hw', 'homework📚']
    return (message.text in a)

#Dnevnik
@bot.message_handler(func = meg)
def starting(message):
    user_id = message.from_user.id
    result = perform_action_with_auth(user_id)
    if len(result) == 2:
        log = result[0]
        passw = result[1]
        global dairy
        dairy = Dnevnik(login=log, password=passw)
        
        if message.text == '/marks' or message.text == 'marks💯':
            print('Answer on marks ...')
            mark(message, dairy)
            print(user_sessions)
        elif message.text == '/hw' or message.text == 'homework📚':
            print('Answer on homework ...')
            view_home(message, 2, dairy)
        else:
            helper(message)
    elif len(result) == 1:     
        bot.send_message(message.chat.id, result)
        auth(message)
#Draw Table
def main_table(message, marks, columns, name_of):
    data = marks
    df = pd.DataFrame(data, columns=columns)

    fig, ax = plt.subplots(figsize=(8, 3))  # Размеры рисунка
    ax.axis('tight')
    ax.axis('off')

    tbl = table(ax, df, loc='center', cellLoc='center', colWidths=[0.1]*len(df.columns))

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)

    for col_idx in range(len(columns)):
        col = tbl.auto_set_column_width(col_idx)
    path = "image\\"+ str(message.from_user.id) + name_of + ".png"
    plt.savefig(path, bbox_inches='tight', pad_inches=0.1)

    file = open(path, 'rb')
    bot.send_photo(message.from_user.id, file)
    
#Message in tgchat
def mms(message, mess):
    bot.send_message(message.from_user.id, mess)
    ans = message.text
    return ans



#Helper
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
        'text', 'location', 'contact', 'sticker'])
def helper(message):
    bot.send_message(message.chat.id, "send /start")


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Ошибка: {e}")
    time.sleep(15)

