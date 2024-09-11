import os
import sqlite3
import signal
from oop_ui import *
def resize(signum, frame):
    raise StopIteration


signal.signal(signal.SIGWINCH, resize)

h = 'Текст заголовка'
body = [
        ('Данные', 'в', 'виде'), 
        ('списка', 'кортежей'), 
        ('со', 'строками'),
]
menu = [
        ('Список',), 
        ('элементов', 'меню'), 
        ('который', 'может', 'быть'), 
        ('разбит', 'на любое количество колонок')
]

MY_DB_DIR = os.path.join(os.environ['HOME'], '.my_db')
DB_NAME = os.path.join(MY_DB_DIR, 'jtt-data.db')

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
def get_period_data(cur, current_period):
    res = cur.execute("SELECT rowid, * FROM period_data WHERE date LIKE ? ORDER BY date", (current_period + '-%', )).fetchall()
    if res is None:
        return [(''),]
    else:
        return res

while True:
    main = Screen(
        header=h,
        body=[get_period_data(cur, '2024-08'),get_period_data(cur, '2024-09')], 
        menu=menu, cols =3
    )

    main.display('#')
    try:
        a = input()
        if a == 'q':
            break
    except StopIteration:
        continue
    except KeyboardInterrupt:
        os.system('clear')
        exit(-1)
