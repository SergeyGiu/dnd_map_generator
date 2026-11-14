import random

def add_carpet(x,y, size=50):
    """Универсальная функция, расположить тайл ковёр
    x,y - координаты левой верхней точки тайла ковра
    size - размер ковра"""

    path_to_image = ""

    return 1

def add_stairs_up():
    """Создаёт лестницу, на которую если наступить, то передвинешься +10 фт."""
    return 1

def add_luke():
    """Универсальная функция, добавляет в дом тайл люк с триггером,
     открывающийся и закрывающийся, а если натупить, тогда опустишься вниз
     Размер 5х5 фт."""
    return 1
def add_cellar(x,y,
               home_border,
               cell=50, debug=True):
    """Генерирует погреб, а именно всю структуру, и тайлы и стены.
    Строится примерно как и комната. От центра начинает расширяться.
    Если вышел за границу дома, то должен быть люк на улицу сразу
    hard_border - квадрат за который выходить нельзя"""
    print(home_border)
    ar_wall_local = []
    ar_doors_local = []
    size_x = random.randint(3,7)
    size_y = random.randint(3,7)

    board = [[x,y],[x+cell, y+cell]]
    flag_up = False
    flag_down = False
    flag_left = False
    flag_right = False
    for i in range(size_x):
        if random.randint(0,1) == 0:
            # Расширение налево
            if board[0][0] - cell > home_border[0]:
                if board[0][1] - cell == home_border[1]:
                    flag_left = True
                board[0][0] -= cell
        else:
            # Расширение направо
            if board[1][0] + cell <= home_border[2]:
                if board[1][0] + cell == home_border[2]:
                    flag_right = True
                board[1][0] += cell

    # Расширение по вертикали
    for i in range(size_y):
        if random.randint(0, 1) == 0:
            # Расширение вверх
            if board[0][1] - cell >= home_border[1]:
                if board[0][1] - cell == home_border[1]:
                    flag_up = True
                board[0][1] -= cell
        else:
            # Расширение вниз
            if board[1][1] + cell <= home_border[3]:
                if board[1][1] + cell == home_border[3]:
                    flag_down = True
                board[1][1] += cell


    ar_flags = []
    if flag_up: ar_flags.append('up')
    if flag_down: ar_flags.append('down')
    if flag_left: ar_flags.append('left')
    if flag_right: ar_flags.append('right')
    if ar_flags:
        second_exit = random.choice(ar_flags)
    else: second_exit = ''
    if debug:
        print('Координаты люка:', f"{x}:{y}")
        print("Границы погреба:", f'{board[0]}:{board[1]}')
        print("Размер дома", f'{home_border}')

        if ar_flags:
            print('Подвал подошёл к границе:', ar_flags)
            print("Второй выход находится в", second_exit)
        else:
            print("Подвал не имеет дверей наружу")


    if second_exit != "":
        # Надо найти нужную стену чтобы её разрубить и раширить для ступенек
        if second_exit == 'down':
            wall_exit = [[board[0][0],board[1][1]], [board[1][0],board[1][1]]]
            door_x = random.randrange(wall_exit[0][0] + cell, wall_exit[1][0]-cell*2)
            door_y = wall_exit[0][1]

            ar_doors_local.append([[door_x,door_y],[door_x+cell,door_y]])

            ar_wall_local.append([[wall_exit[0][0], door_y],[door_x,door_y]])
            ar_wall_local.append([[door_x, door_y],[wall_exit[1][0],door_y]])

            ar_wall_local.append([[door_x, door_y],[door_x,door_y+cell*2]])
            ar_wall_local.append([[door_x+cell, door_y],[door_x+cell,door_y+cell*2]])
            ar_wall_local.append([[door_x, door_y+cell*2],[door_x+cell,door_y+cell*2]])

            ar_wall_local.append([[board[0][0], board[0][1]],[board[1][0],board[0][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]],[board[0][0],board[1][1]]])
            ar_wall_local.append([[board[1][0],board[0][1]],[board[1][0],board[1][1]]])
        elif second_exit == 'up':
            wall_exit = [[board[0][0],board[0][1]], [board[1][0],board[0][1]]]
            door_x = random.randrange(wall_exit[0][0] + cell, wall_exit[1][0] - cell * 2)
            door_y = wall_exit[0][1]

            ar_doors_local.append([[door_x, door_y], [door_x + cell, door_y]])

            ar_wall_local.append([[wall_exit[0][0], door_y], [door_x, door_y]])
            ar_wall_local.append([[door_x, door_y], [wall_exit[1][0], door_y]])

            ar_wall_local.append([[door_x, door_y], [door_x, door_y + cell * 2]])
            ar_wall_local.append([[door_x + cell, door_y], [door_x + cell, door_y + cell * 2]])
            ar_wall_local.append([[door_x, door_y + cell * 2], [door_x + cell, door_y + cell * 2]])

            ar_wall_local.append([[board[0][0], board[1][1]],[board[1][0],board[1][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]], [board[0][0], board[1][1]]])
            ar_wall_local.append([[board[1][0], board[0][1]], [board[1][0], board[1][1]]])

        elif second_exit == 'left':
            wall_exit = [[board[0][0],board[0][1]], [board[0][0],board[1][1]]]
            door_x = wall_exit[0][0]
            door_y = random.randrange(wall_exit[0][1] + cell, wall_exit[1][1] - cell * 2)

            ar_doors_local.append([[door_x, door_y], [door_x, door_y+cell]])

            ar_wall_local.append([[wall_exit[0][0], wall_exit[0][1]], [door_x, door_y]])
            ar_wall_local.append([[door_x, door_y+ cell], [wall_exit[1][0], wall_exit[1][1]]])

            ar_wall_local.append([[door_x, door_y], [door_x-cell*2, door_y]])
            ar_wall_local.append([[door_x-cell*2, door_y], [door_x-cell*2, door_y + cell]])
            ar_wall_local.append([[door_x, door_y+cell], [door_x-cell*2, door_y + cell]])

            ar_wall_local.append([[board[0][0], board[0][1]],[board[1][0],board[0][1]]])
            ar_wall_local.append([[board[0][0], board[1][1]],[board[1][0],board[1][1]]])
            ar_wall_local.append([[board[1][0], board[0][1]], [board[1][0], board[1][1]]])


        elif second_exit == 'right':
            wall_exit = [[board[1][0],board[0][1]], [board[1][0],board[1][1]]]
            door_x = wall_exit[0][0]
            door_y = random.randrange(wall_exit[0][1] + cell, wall_exit[1][1] - cell * 2)

            ar_doors_local.append([[door_x, door_y], [door_x, door_y + cell]])

            ar_wall_local.append([[wall_exit[0][0], wall_exit[0][1]], [door_x, door_y]])
            ar_wall_local.append([[door_x, door_y + cell], [wall_exit[1][0], wall_exit[1][1]]])

            ar_wall_local.append([[door_x, door_y], [door_x + cell * 2, door_y]])
            ar_wall_local.append([[door_x + cell * 2, door_y], [door_x + cell * 2, door_y + cell]])
            ar_wall_local.append([[door_x, door_y + cell], [door_x + cell * 2, door_y + cell]])

            ar_wall_local.append([[board[0][0], board[0][1]], [board[1][0], board[0][1]]])
            ar_wall_local.append([[board[0][0], board[1][1]], [board[1][0], board[1][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]], [board[0][0], board[1][1]]])
        else:
            exit("Неизвестное направление")


input_walls = [
    [(0,0),(600,0)],
    [(600,0),(600,500)],
    [(0,0),(0,500)],

    [(0,500),(250,500)],
    [(300,500),(600,500)],
    [(250,500),(300,500)],
]

# Должна быть кровть(1-4)
# стол - обеденный или рабочий
# печь
# Комод и шкаф
# люк в погреб
# выхода вешалка
#  корзины ящики
# Коврик у кровати или входа
# лавки
# икона
# инструмены всякие, прялка и веретено


# Печь находится слева или справа от двери в углу.
# Напротив печи в другом углу иконы


# Первое, функция должна определить где дверь и подсчитать найти две смежные к ней стены
# Если длины обоих стен приемлимы(>x) тогда рандомим с какой стороны. Стена H
# Отмечаем четыре угла A,B,C,D
# Угол А это печь.
# Угол С это икона
# Угол
# На этой стене Н в углу стоит печь, рядом с ней место для готовки(или сразу место для обеда)
#  Возможно стоит огородить занавеской или лёгкой перегородкой (рандомно)


#  такс. Нужно какие размеры будет иметь печь. Думаю стоит ввести два вида. Угловая и прямая.
# Прямая занимает 2х1, угловая три клетки буквой г.


def add_furniture(walls: list,cell: int):
    """Функция добавляет фурнитуру в комнату"""
    # Строим матрицу клеток
    x_buf = []
    y_buf = []
    for i in range(len(walls)):
        x_buf.append(walls[i][0][0])
        x_buf.append(walls[i][1][0])
        y_buf.append(walls[i][0][1])
        y_buf.append(walls[i][1][1])
    x_min, x_max = min(x_buf), max(x_buf)
    y_min, y_max = min(y_buf), max(y_buf)

    cnt_x = (x_max - x_min) // cell
    cnt_y = (y_max - y_min) // cell
    print(cnt_x, cnt_y)
    # Заглушка, сейчас я знаю что это дверь
    door = walls[-1]

    # Рандомим, будет ли ковёр
    if random.randint(1,100) > 60:
        tile = add_carpet(x=0,y=0,size=50)

    # Рандомим будет ли погреб
    if random.randint(1,100) > 1:
        add_luke()
        add_cellar(450,300,
           home_border=[walls[0][0][0],walls[0][0][1],walls[0-2][1][0],walls[-2][1][1]], cell=50)

add_furniture(input_walls, cell=50)