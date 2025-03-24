import telega
import main

telega.start()

passw = telega.passw
log = telega.log

main.starting(log, passw)

main.key()

def sheld(info, weeks):

    schedule = dairy.week(info, weeks)
    weekr = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    for i in schedule['scheldule']:
        a = []
        a.append(i)
        for j in i:
            a.append(j)
        b.append(a)
    main_table(b, weekr, name_of="sheldule")