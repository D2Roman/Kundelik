from dnevnikru import Dnevnik
from pprint import pprint

dairy = Dnevnik(login="roman.dragun", password="dragunroman08")

marks = dairy.marks()
for i in marks:
    for j in range(15):
        if i[j] == '':
            i[j] = '-'
#pprint(marks)
print(f"{'#':<3} {'Предметы':<20} {'Отметки':^15} {'Опоздания':^10} {'Всего пропусков':^10} {'По болезни':^10} {'СОР 1':^8} {'СОР 2':^8} {'СОР 3':^8} {'СОР 4':^8} {'СОЧ':^8} {'СОР + ФО%':^5} {'СОЧ%':^5} {'Сумма':^5} {'Итог':^4}")

for i in marks:
    print(f"{i[0]:<3} {i[1]:<20} {i[2]:^15} {i[3]:^10} {i[4]:^10} {i[5]:^10} {i[6]:^8} {i[7]:^8} {i[8]:^8} {i[9]:^8} {i[10]:^8} {i[11]:^5} {i[12]:^5} {i[13]:^5} {i[14]:^4}")