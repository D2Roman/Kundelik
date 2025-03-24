from dnevnikru import Dnevnik
from pprint import pprint


log = input("Your login >>> ")
passw = input("Your password >>> ")

log = "roman.dragun"
passw = "dragunroman08"


dairy = Dnevnik(login=log, password=passw)

homework = dairy.homework(days=7)

print(f"{'Предмет':<15} {'ДЗ':^30} {'Урок':^15}")
pprint(homework)
for i in homework['homework']:
    print(f"{i[0]:<15} {i[1]:^30} {i[2]:^15}")