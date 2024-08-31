from oop_ui import Header, Table, Menu, Screen

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

# Можно создать отдельные заголовок, тело или меню
# Или использовать объект Screen
h1 = Header(h)
b1 = Table(body)
m1 = Menu (menu, 3)
m2 = Menu (menu, 2, False)
s1 = Screen(h, body, menu, 3)

s1.print()

Screen.line()
h1.print()
Screen.line()
b1.print()
Screen.line()
m1.print()
Screen.line()

