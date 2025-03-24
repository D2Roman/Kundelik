from dnevnikru import Dnevnik
from pprint import pprint
from prettytable import PrettyTable
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import telega

##log = input("Your login >>> ")
#passw = input("Your password >>> ")

run = True



def main_table(marks, columns, name_of):
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

    plt.savefig(name_of + ".png", bbox_inches='tight', pad_inches=0.1)
    telega.answer(name_of + ".png")

    

def tabl1(table):
    img = Image.new('RGB', (1400, 400), 'white')
    img.save('test.jpg')
    img = Image.open('test.jpg')
    font = ImageFont.truetype('consolas.ttf', size = 16)
    idraw = ImageDraw.Draw(img)
    idraw.multiline_text((50,50), str(table), font=font, fill='black')
    img.save('test.jpg')
    img = Image.open('test.jpg')
    img.show()


def mark(period):
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
    print(marks)
    main_table(marks, columns, name_of='marks')
    
def prtable(marks):
    th = ['№', 'Предметы', 'Отметки', 'Опоздания', 'Всего Пропусков', 'По болезни', 'СОР 1', 'СОР 2', 
          'СОР 3', 'СОР 4', 'СОЧ', 'СОР + ФО%', 'СОЧ%', 'Сумма', 'Итог']
    td = marks
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    table.add_rows(td_data)
    print(str(table))
    tabl1(table)
    


def view_home(day):
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
    main_table(td, th, name_of='homework')

def starting():
    global dairy
    dairy = Dnevnik(login=log, password=passw)
    ans = telega.mms(" 1: Homework \n 2: Marks \n 3: Quit programm \n Write your answer >>>")
    #ans = int(input(" 1: Homework \n 2: Marks \n 3: Quit programm \n Write your answer >>>"))
    if ans == 1:
        view_home(int(input("Day >>> ")))
    elif ans == 2:
        mark(int(input('write the period of marks >>> ')))
    elif ans == 3:
        run = False

