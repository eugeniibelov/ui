#!/usr/bin/env python3

# Новая реализация библиотеки для отрисовки простого
# интерфейса для работы с таблицами

from os import get_terminal_size

VERSION = '0.0.2-9

class Table():

    @staticmethod
    def line():
        '''Печатает горизонтальную линию'''
        print('-' * get_terminal_size()[0])

    @classmethod
    def cols(cls,arr):
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
        tw = get_terminal_size()[0]
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

    def print(self, sep=' '):
        '''Выводит таблицу с заданными разделителями'''
        Table.line()
        for row in self.view:
            for c in range(len(row)):
                print('%s%-*s' % (sep * self.sep_len, self.widths[c], row[c]), end='')
            else:
                print('%s' % (sep * self.sep_len,))
        Table.line()


Header('sgfdfgdfgfd').print()




class Menu(Table):
    @classmethod
    def get_view(cls, arr, cols):
        '''Возвращает таблицу сведенную до указанного количества колонок'''
        if cols == 0:
            raise ValueError("Cols must be bigger than 0")
        items = []
        menu_lst = []

        for row in arr:
            for item in row:
                if len(item) > 0:
                    items.append(''.join(['[', item[0], ']', item[1:]]))

        while len(items) > 0:
            t = []
            for i in range(cols):
                try: t.append(items.pop(0))
                except: t.append('')
            menu_lst.append(tuple(t))

        return menu_lst

    def __init__(self, arr, cols):
        '''Конструктор класса Menu'''
        self.view = Menu.get_view(arr, cols)
        self.widths = Table.get_item_widths(self.view)
        self.sep_len = Table.get_sep_len(self.view, self.widths)

