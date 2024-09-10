import os
import oop_ui
import sqlite3
import signal

def winch_handler(signum, frame):
    raise StopIteration

signal.signal(signal.SIGWINCH, winch_handler)


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

current_period = (cur.execute("SELECT date()").fetchone())[0][:7]
data = get_period_data(cur, current_period)

class Screen():
    @classmethod
    def line(cls):
        from os import get_terminal_size
        print('-' * get_terminal_size()[0])

    @classmethod
    # Очищает экран
    def clear(cls): print('\033[H\033[2J', end='')

    # Конструктр объекта Screen
    def __init__(self, **kwargs):
        try:
            self.header = oop_ui.Table(kwargs['header'])
            self.body = oop_ui.Table(kwargs['body'])
            self.menu = oop_ui.Table(kwargs['menu'], kwargs['cols'])
        except:
            pass

    def display(self):
        Screen.clear()
        Screen.line()
        self.header.show()
        Screen.line()
        self.body.show()


while True:
    main = Screen(header=h,body=get_period_data(cur, current_period))
    main.display()
    try:
        a = input()
        if a == 'q':
            break
    except:
        continue

