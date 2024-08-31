#!/usr/bin/env python3

# Новая реализация библиотеки для отрисовки простого
# интерфейса для работы с таблицами

VERSION = '0.0.2-9'

class Table():

    @classmethod
    def cols(cls, arr):
        '''Возвращает количество колонок таблицы'''
        return max([len(row) for row in arr])

    @classmethod
    def rows(cls, arr):
        '''Возвращает количество строк таблицы '''
        return len(arr)

    @classmethod
    def get_view(cls, arr):
        '''Возвращает таблицу в ровном виде'''
        if type(arr) not in (list, tuple):
            raise ValueError(f'Expected list-of-tuples, given {type(arr)}')
        t = []
        for row in arr:
            while len(row) < Table.cols(arr):
                row = row + ('',)
            t.append(row)
        return t

    @classmethod
    def get_item_widths(cls, arr):
        '''Возвращает список ширин для каждой колонки'''
        widths = []
        for col in range(Table.cols(arr)):
            widths.append(max([len(str(arr[r][col])) for r in range(Table.rows(arr))]))

        return widths

    @classmethod
    def get_sep_len(cls, arr, widths):
        '''Возвращает ширину пустого пространства между колонками'''
        tw = os.get_terminal_size()[0]
        sep_len = (tw - sum(widths)) // (len(widths) + 1)
        while sum(widths) + (Table.cols(arr) + 1) * sep_len > tw:
            sep_len -= 1
        return sep_len

    def print(self, sep=' '):
        '''Выводит таблицу с заданными разделителями'''
        for row in self.view:
            for c in range(len(row)):
                print('%s%-*s' % (sep * self.sep_len, self.widths[c], row[c]), end='')
            else:
                print('%s' % (sep * self.sep_len,))

    def __init__(self, arr):
        '''Конструктор класса Table'''
        self.view = Table.get_view(arr)
        self.widths = Table.get_item_widths(self.view)
        self.sep_len = Table.get_sep_len(self.view, self.widths)



class Header(Table):
    @classmethod
    def get_view(cls, header_str):
        return [(header_str,)]

    def __init__(self, header_str):
        '''Конструктор класса Header'''
        self.view = Header.get_view(header_str)
        self.widths = Table.get_item_widths(self.view)
        self.sep_len = Table.get_sep_len(self.view, self.widths)

class Menu(Table):
    @classmethod
    def get_view(cls, arr, cols, sb=True):
        '''Возвращает таблицу сведенную до указанного количества колонок'''
        if cols == 0:
            raise ValueError("Cols must be bigger than 0")
        items = []
        menu_lst = []

        for row in arr:
            for item in row:
                if len(item) > 0:
                    if sb:
                        items.append(''.join(['[', item[0], ']', item[1:]]))
                    else:
                        items.append(item)


        while len(items) > 0:
            t = []
            for i in range(cols):
                try: t.append(items.pop(0))
                except: t.append('')
            menu_lst.append(tuple(t))

        return menu_lst

    def __init__(self, arr, cols, sb=True):
        '''Конструктор класса Menu'''
        self.view = Menu.get_view(arr, cols, sb)
        self.widths = Table.get_item_widths(self.view)
        self.sep_len = Table.get_sep_len(self.view, self.widths)

class Screen():
    @classmethod
    def line(cls):
        '''Печатает горизонтальную линию'''
        print('-' * os.get_terminal_size()[0])

    @classmethod
    def clear(cls):
        '''Очищает экран'''
        print('\033[H\033[2J', end='')

    def __init__(self, title, body, menu, menu_col, sb=True):
        '''Конструктр объекта Screen'''
        self.h = Header(title)
        self.b = Table(body)
        self.m = Menu(menu, menu_col, sb)


    def print(self):
        Screen.clear()
        Screen.line()
        self.h.print()
        Screen.line()

        self.b.print()
        Screen.line()
        self.m.print()
        Screen.line()
        

import os
import sqlite3

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

jtt_main = Screen(
    'Job-time-tracker', data, [('sdf', 'dfh'), ('',)], 2

)
jtt_main.print()
