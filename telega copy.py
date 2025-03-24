from dnevnikru import Dnevnik
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pandas.plotting import table
import telebot
import os

matplotlib.use('agg')

bot = telebot.TeleBot('6668462912:AAEXd_oFVLo1jX-Dx1Wo_0MocduXmMiQlHM')

data_file = 'db.txt'


class UserSession:
    def __init__(self, user_id, log, passw):
        self.user_id = user_id
        self.log = log
        self.passw = passw



def starting(message):
    user_id = message.from_user.id
    log, passw = perform_action(user_id)
    global dairy
    dairy = Dnevnik(login=log, password=passw)

def read_user_data(user_id):
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            for line in file:
                stored_user_id, log, passw = line.strip().split(',')
                if int(stored_user_id) == user_id:
                    return log, passw
    return None, None

def write_user_data(user_id, log, passw):
    with open(data_file, 'a') as file:
        file.write(f"{user_id},{log},{passw}\n")

def perform_action(user_id):
    log, passw = read_user_data(user_id)
    if log and passw:
        # Здесь выполняется действие с использованием логина и пароля
        return f"Данные для пользователя {user_id}:\nЛогин: {log}\nПароль: {passw}"
    else:
        return "Данные авторизации не найдены. Пожалуйста, авторизуйтесь сначала."




@bot.message_handler(commands=['start', 'marks', 'hw'])
def start(message):
    user_id = message.from_user.id
    log, passw = read_user_data(user_id)
    if log and passw:
        bot.send_message(message.chat.id, f"Вы уже авторизованы.\nЛогин: {log}\nПароль: {passw}")
        if message.text == '/marks':
            print('Answer on marks ...')
            mark(message)
        elif message.text == '/hw':
            print('Answer on homework ...')
            view_home(message, day=2)

    else:
        bot.send_message(message.chat.id, "Привет! Пожалуйста, авторизуйтесь с помощью команды /auth логин пароль")


def mark(message):
    marks = starting.dairy.marks()
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
    print(marks)
    main_table(message, marks, columns, name_of='marks')

def view_home(message, day):
    homework = starting.dairy.homework(days=day)
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

def starting(message):
    user_id = message.from_user.id
    log, passw = perform_action(user_id)
    bot.send_message(message.chat.id, log + " " + passw)
    global dairy
    dairy = Dnevnik(login=log, password=passw)
    bot.send_message(message.from_user.id, '1. /start - registration \n 2. /marks - marks for the term \n 3. /hw - homework')
    #ans = mms(" 1: Homework \n 2: Marks \n 3: Quit programm \n Write your answer >>>")
    #ans = int(input(" 1: Homework \n 2: Marks \n 3: Quit programm \n Write your answer >>>"))
    start(message)


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
    path = name_of + ".png"
    plt.savefig(path, bbox_inches='tight', pad_inches=0.1)

    file = open(path, 'rb')
    bot.send_photo(message.from_user.id, file)
    

def mms(message, mess):
    bot.send_message(message.from_user.id, mess)
    ans = message.text
    return ans

@bot.message_handler(commands=['auth'])
def auth(message):
    user_id = message.from_user.id
    try:
        _, log, passw = message.text.split()
        stored_log, stored_passw = read_user_data(user_id)
        if stored_log and stored_passw:
            bot.send_message(message.chat.id, "Вы уже авторизованы.")
        else:
            write_user_data(user_id, log, passw)
            bot.send_message(message.chat.id, "Вы успешно авторизовались!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, используйте формат: /auth логин пароль")


bot.polling(none_stop=True, interval=0)
