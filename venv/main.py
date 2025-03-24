from dnevnikru import Dnevnik
from pprint import pprint
from prettytable import PrettyTable

##log = input("Your login >>> ")
#passw = input("Your password >>> ")

log = "roman.dragun"
passw = "dragunroman08"
run = True

dairy = Dnevnik(login=log, password=passw)

def mark(period):
    marks = dairy.marks()
    th = ['№', 'Предметы', 'Отметки', 'Опоздания', 'Всего Пропусков', 'По болезни', 'СОР 1', 'СОР 2', 
          'СОР 3', 'СОР 4', 'СОЧ', 'СОР + ФО%', 'СОЧ%', 'Сумма', 'Итог']
    td = marks
    columns = len(th)
    table = PrettyTable(th)
    td_data = td[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]
    print(table)


def view_home(day):
    homework = dairy.homework(days=day)

    print(f"{'Предмет':<15} {'ДЗ':^30} {'Урок':^15}")
    for i in homework['homework']:
        print(f"{i[2]:<15} {i[0]:^15} {i[1]:^60}")

while run == True:
    ans = int(input(" 1: Homework \n 2: Marks \n Write your answer >>>"))
    if ans == 1:
        view_home(int(input("Day >>> ")))
    elif ans == 2:
        mark(int(input('write the period of marks >>> ')))

