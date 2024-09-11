#!/usr/bin/env python3

# Новая реализация библиотеки для отрисовки простого
# интерфейса для работы с таблицами

VERSION = '0.0.3-1'

class Table():

    @classmethod
    # Возвращает количество колонок таблицы
    def _cols(cls, arr): return max([len(row) for row in arr])

    @classmethod
    # Возвращает количество строк таблицы
    def _rows(cls, arr): return len(arr)

    @classmethod
    # Возвращает список ширин для каждой колонки
    def _get_item_widths(cls, arr):
        widths = []
        for col in range(Table._cols(arr)):
            widths.append(max([len(str(arr[r][col])) for r in range(Table._rows(arr))]))
        return widths

    @classmethod
    # Возвращает ширину пустого пространства между колонками
    def _get_sep_len(cls, arr, widths):
        from os import get_terminal_size
        tw = get_terminal_size()[0]
        sep_len = (tw - sum(widths)) // (len(widths) + 1)
        while sum(widths) + (Table._cols(arr) + 1) * sep_len > tw:
            sep_len -= 1
        return sep_len

    @classmethod
    # Возвращает таблицу в ровном виде
    # Или преобразует до нужного количества колонок
    def get_view(cls, arr, needed_cols=None):
        if not isinstance(arr, (list, tuple, str)):
            raise ValueError(f'Expected list-of-tuples or string (if you need a header), given {type(arr)}')

        if isinstance(arr, str):
            return [(arr,)]

        menu_lst = []

        if needed_cols is None:
            t = []
            for row in arr:
                while len(row) < Table._cols(arr):
                    row = row + ('',)
                menu_lst.append(row)
        else:
            # Получаем один список строк из списка кортежей
            items = []
            for row in arr:
                for item in row:
                    if len(str(item)) > 0:
                        items.append(item)

            while len(items) > 0:
                t = []
                for i in range(needed_cols):
                    try: t.append(items.pop(0))
                    except: t.append('')
                menu_lst.append(tuple(t))

        return menu_lst

    # Конструктор класса Table
    def __init__(self, arr, needed_cols=None):
        self.view = Table.get_view(arr, needed_cols)

    # Выводит таблицу с заданными разделителями
    def show(self, sep=' '):

        widths = Table._get_item_widths(self.view)
        sep_len = Table._get_sep_len(self.view, widths)

        for row in self.view:
            for c in range(len(row)):
                print('%s%-*s' % (sep * sep_len, widths[c], row[c]), end='')
            else:
                print('%s' % (sep * sep_len,))


class Screen():
    @classmethod
    # рисует линию шириной с экран заданным символом
    def line(cls, c='-'):
        from os import get_terminal_size
        print(c * get_terminal_size()[0])

    @classmethod
    # Очищает экран
    def clear(cls): print('\033[H\033[2J', end='')

    # Конструктр объекта Screen
    # Принимает именованные параметры, где 
    # header - заголовок
    # body - список с основными табличными данными
    # menu - список строк для меню
    # cols - целое число колонок меню
    def __init__(self, **kwargs):

        if (
                kwargs.get('header', False) and
                isinstance(kwargs['header'], str) and
                len(kwargs['header']) > 0
        ):
            self.__header = Table(kwargs['header'])
        else:
            self.__header = None


        if (
                kwargs.get('body', False) and
                isinstance(kwargs['body'], list)
        ):
            self.__body = [Table(i) for i in kwargs['body']]
        else:
            self.__body = None


        if (
            (
                kwargs.get('menu', False) and
                kwargs.get('cols', False)
            ) and
            (
                isinstance(kwargs['menu'], list) and
                isinstance(kwargs['cols'], int)
            )
        ):
            self.__menu = Table(kwargs['menu'], kwargs['cols'])
        else:
            self.__menu = None


    def display(self, c='-'):
        Screen.clear()
        if self.__header:
            Screen.line(c)
            self.__header.show()

        Screen.line(c)

        if self.__body:
            for i in self.__body:
                i.show()
                Screen.line(c)

        if self.__menu:
            self.__menu.show()
            Screen.line(c)

