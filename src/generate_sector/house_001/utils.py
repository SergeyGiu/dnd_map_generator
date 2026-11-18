import random

import src.utils
from src.utils import Color
from PIL.Image import radial_gradient


def find_center_polygon(polygon: list, cell: float) -> tuple:
    """
    Вычисляет центр полигона (центроид) и округляет до сетки cell.
    """
    if not polygon:
        raise ValueError("Полигон пуст")

    x_coords = [p[0] for p in polygon]
    y_coords = [p[1] for p in polygon]

    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)

    return snap_to_grid(center_x, center_y, cell)


def find_leftmost_point(polygon: list, cell: float) -> tuple:
    """
    Возвращает координаты самой левой точки (минимальный X), округленные до сетки.
    """
    if not polygon:
        return (0, 0)

    # Находим точку с минимальным X
    leftmost = min(polygon, key=lambda p: p[0])
    # Округляем её координаты до сетки
    return snap_to_grid(leftmost[0], leftmost[1], cell)


def find_rightmost_point(polygon: list, cell: float) -> tuple:
    """
    Возвращает координаты самой правой точки (максимальный X), округленные до сетки.
    """
    if not polygon:
        return (0, 0)

    # Находим точку с максимальным X
    rightmost = max(polygon, key=lambda p: p[0])
    return snap_to_grid(rightmost[0], rightmost[1], cell)


def find_topmost_point(polygon: list, cell: float) -> tuple:
    """
    Возвращает координаты самой верхней точки.
    ВАЖНО: Зависит от системы координат.
    - Если Y=0 сверху (как в pygame, css): min(y)
    - Если Y=0 снизу (математика, gl): max(y)
    Предполагаем стандартную игровую/экранную: Y растет вниз.
    """
    if not polygon:
        return (0, 0)

    # Самая верхняя — та, у которой минимальный Y
    topmost = min(polygon, key=lambda p: p[1])
    return snap_to_grid(topmost[0], topmost[1], cell)


def find_bottommost_point(polygon: list, cell: float) -> tuple:
    """
    Возвращает координаты самой нижней точки.
    """
    if not polygon:
        return (0, 0)

    # Самая нижняя — та, у которой максимальный Y
    bottommost = max(polygon, key=lambda p: p[1])
    return snap_to_grid(bottommost[0], bottommost[1], cell)


def snap_to_grid(x: float, y: float, cell: float) -> tuple:
    """
    Вспомогательная функция: округляет координаты до ближайшей клетки.
    """
    if cell == 0:
        return (0, 0)
    snapped_x = round(x / cell) * cell
    snapped_y = round(y / cell) * cell
    return (snapped_x, snapped_y)

def create_start_point(direct, points, cell, offset=None):
    """Определяем стартовую точку отссчёта.
    Если направление вверх. Тогда дом стараемся чуть ниже
    Если справа вход, то левее и тд"""
    if offset is None: offset = cell*4
    walls = []
    for i in range(len(points)):
        walls.append([points[i-1], points[i]])
    center = find_center_polygon(polygon=points, cell = cell)
    min_x = find_leftmost_point(polygon=points, cell=cell)
    max_x = find_rightmost_point(polygon=points,cell = cell)
    max_y = find_bottommost_point(polygon=points, cell=cell)
    min_y = find_topmost_point(polygon=points, cell=cell)



    print(f"{Color.MAGENTA}Поиск стартовой точки...")
    print("---> Минимальное расстояние до края:", offset)
    print("---> Массив стен", walls)
    print(f"-----> Координаты центра", center)
    print("-----> Самая левая точка", min_x)
    print("-----> Самая правая точка", max_x)
    print("-----> Самая верхняя точка", min_y)
    print("-----> Самая нижняя точка", max_y)
    print(f"{Color.CYAN}---> Направление сектора:", direct)
    if direct == "up":
        print(f"---->Значит сдвигаем дом в нижнюю часть")
        y_board = center[1]
        cnt_error = 0
        while True:
            x = random.randrange(min_x[0], max_x[0], cell)
            y = random.randrange(y_board, max_y[1], cell)
            distance, indx_wall = src.utils.min_distance_to_walls(walls=walls, point=(x,y))
            if distance < offset:
                if y_board < min_y[1]:
                    cnt_error += 1
                    if cnt_error > 100:
                        print(f"{Color.RED}---->Не удалось найти точку свободную{Color.WHITE}")
                        return 0
                else:
                    y_board -= cell
                print(f'{Color.RED}Получили координату {x}:{y}. Минимальное расстояние={distance}. Расширяем зону center={x}:{y_board}{Color.WHITE}')

            else:
                res, indx_hits = src.utils.segment_hits_any_wall(
                    walls=walls,segment=[center,[x, y]])
                if res:
                    print(f'{Color.RED}Точка {x}:{y} прошла проверка дальности от стен, находится по другую сторону от края сектора{Color.WHITE}')
                    continue
                print(f'{Color.CYAN}Получили координату {x}:{y}. Минимальное расстояние={distance}{Color.WHITE}')
                return [x, y]
    elif direct == "down":
        print(f"---->Значит сдвигаем дом в верхнюю часть{Color.WHITE}")
        y_board = center[1]
        cnt_error = 0
        while True:
            x = random.randrange(min_x[0], max_x[0], cell)
            y = random.randrange(min_y[1], y_board, cell)
            distance, indx_wall = src.utils.min_distance_to_walls(
                walls=walls,point=(x,y))
            if distance < offset:
                if y_board > max_y[1]:
                    cnt_error += 1
                    if cnt_error > 100:
                        print(f"{Color.RED}---->Не удалось найти точку свободную{Color.WHITE}")
                        return 0
                else:
                    y_board += cell
                print(f'{Color.RED}Получили координату {x}:{y}. Минимальное расстояние={distance}. Расширяем зону center={x}:{y_board}{Color.WHITE}')

            else:
                res, indx_hits = src.utils.segment_hits_any_wall(
                    walls=walls, segment=[center, [x, y]])
                if res:
                    print(f'{Color.RED}Точка {x}:{y} прошла проверка дальности от стен, находится по другую сторону от края сектора{Color.WHITE}')
                    continue
                print(f'{Color.CYAN}Получили координату {x}:{y}. Минимальное расстояние={distance}{Color.WHITE}')
                return [x,y]
    elif direct == "left":
        print(f"---->Значит сдвигаем дом в правую часть{Color.WHITE}")
        x_board = center[0]
        cnt_error = 0
        while True:
            x = random.randrange(x_board, max_x[0], cell)
            y = random.randrange(min_y[1], max_y[1], cell)
            distance, indx_wall = src.utils.min_distance_to_walls(
                walls=walls,point=(x,y))
            if distance < offset:
                if x_board < min_x[0]:
                    cnt_error += 1
                    if cnt_error > 100:
                        print(f"{Color.RED}---->Не удалось найти точку свободную{Color.WHITE}")
                        return 0
                else:
                    x_board -= cell
                print(f'{Color.RED}Получили координату {x}:{y}. Минимальное расстояние={distance}. Расширяем зону center={x}:{x_board}{Color.WHITE}')

            else:
                res, indx_hits = src.utils.segment_hits_any_wall(
                    walls=walls, segment=[center, [x, y]])
                if res:
                    print(f'{Color.CYAN}Точка {x}:{y} прошла проверка дальности от стен, находится по другую сторону от края сектора{Color.WHITE}')
                    continue
                print(f'{Color.GREEN}Получили координату {x}:{y}. Минимальное расстояние={distance}{Color.WHITE}')
                return [x,y]
    elif direct == "right":
        print(f"---->Значит сдвигаем дом в левую часть{Color.WHITE}")
        x_board = center[0]
        cnt_error = 0
        while True:
            x = random.randrange(min_x[0], x_board, cell)
            y = random.randrange(min_y[1], max_y[1], cell)
            distance, indx_wall = src.utils.min_distance_to_walls(
                walls=walls,point=(x,y))
            if distance < offset:
                if x_board > max_x[0]:
                    cnt_error += 1
                    if cnt_error > 100:
                        print(f"{Color.RED}---->Не удалось найти точку свободную{Color.WHITE}")
                        return 0
                else:
                    x_board += cell
                print(f'{Color.RED}Получили координату {x}:{y}. Минимальное расстояние={distance}. Расширяем зону center={x}:{x_board}{Color.WHITE}')

            else:
                res, indx_hits = src.utils.segment_hits_any_wall(
                    walls=walls, segment=[center, [x, y]])
                if res:
                    print(f'{Color.RED}Точка {x}:{y} прошла проверка дальности от стен, находится по другую сторону от края сектора{Color.WHITE}')
                    continue
                print(f'{Color.CYAN}Получили координату {x}:{y}. Минимальное расстояние={distance}{Color.WHITE}')
                return [x,y]
    else:
        exit('Неизвестное направление')



def create_start_point3(direct_local, padding_w, padding_h, cell, width, height):
    # Определяем стартовую точку отсчёта
    if direct_local == "up":
        local_point_x1 = random.randrange(padding_w + cell,
                                          padding_w + width - cell * 2, cell)
        local_point_y1 = random.randrange(padding_h + height // 2,
                                          padding_h + height - cell * 2, cell)
    elif direct_local == "down":
        local_point_x1 = random.randrange(padding_w + cell,
                                          padding_w + width - cell * 2, cell)
        local_point_y1 = random.randrange(padding_h + cell,
                                          padding_h + height // 2, cell)
    elif direct_local == "left":
        local_point_x1 = random.randrange(padding_w + width // 2,
                                          padding_w + width - cell * 2, cell)
        local_point_y1 = random.randrange(padding_h + cell,
                                          padding_h + height - cell * 2, cell)
    elif direct_local == "right":
        local_point_x1 = random.randrange(padding_w + cell,
                                          padding_w + width // 2, cell)
        local_point_y1 = random.randrange(padding_h + cell,
                                          padding_h + height - cell * 2, cell)
    else:
        exit('Неизвестное направление')

    local_point_x2 = local_point_x1 + cell
    local_point_y2 = local_point_y1 + cell
    return local_point_x1, local_point_y1, local_point_x2, local_point_y2


def extend_square(start_point, polygon, cell, offset=None):
    """Расширитель здания, но не дальше ограничений polygon"""
    if offset is None: offset = cell * 4
    x1,y1 = start_point
    x2,y2 = x1+cell, y1+cell

    flag_up = False
    flag_down = False
    flag_left = False
    flag_right = False
    print(f'{Color.YELLOW}Расширяем точку для получения очертания дома')
    for _ in range(random.randint(4, 7)):
        dir = random.randint(0, 1) # Выбирается направление
        if dir == 0:  # Движение влево
            buf_point = [x1-cell, y1]
            distance, indx = src.utils.min_distance_point_to_polygon(
                point=buf_point, polygon=polygon) # Смотрим дистанцию точки
            if distance < offset or flag_left:
                flag_left = True # Сдвигаться левее больше нельзя
                if not flag_right: # А вправо можно?
                    x2 += cell
            else:
                '''print(f'{Color.YELLOW}Дистанция новой точки x1:y1'
                      f'{buf_point}={distance}{Color.WHITE}')'''
                x1 -= cell
        else:  # Движение вправо (dir == 1)
            buf_point = [x2 + cell, y2]
            distance, indx = src.utils.min_distance_point_to_polygon(
                point=buf_point, polygon=polygon)  # Смотрим дистанцию точки
            if distance < offset or flag_right:
                flag_right = True  # Сдвигаться правее больше нельзя
                if not flag_left:  # А влево можно?
                    x1 -= cell
            else:
                '''print(f'{Color.YELLOW}Дистанция новой точки x2:y2'
                      f'{buf_point}={distance}{Color.WHITE}')'''
                x2 += cell
    for _ in range(random.randint(4, 7)):
        dir = random.randint(0, 1) # Выбирается направление
        if dir == 0:  # Движение вверх
            buf_point = [x1, y1 - cell]
            distance, indx = src.utils.min_distance_point_to_polygon(
                point=buf_point, polygon=polygon)  # Смотрим дистанцию точки
            if distance < offset or flag_up:
                flag_up = True  # Сдвигаться выше больше нельзя
                if not flag_down:  # А вниз можно?
                    y2 += cell
            else:
                '''print(f'{Color.YELLOW}Дистанция новой точки x1:y1'
                      f'{buf_point}={distance}{Color.WHITE}')'''
                y1 -= cell
        else:  # Движение вниз (dir == 1)
            buf_point = [x2, y2 + cell]
            distance, indx = src.utils.min_distance_point_to_polygon(
                point=buf_point, polygon=polygon)  # Смотрим дистанцию точки
            if distance < offset or flag_down:
                flag_down = True  # Сдвигаться ниже больше нельзя
                if not flag_up:  # А вверх можно?
                    y1 -= cell
            else:
                '''print(f'{Color.YELLOW}Дистанция новой точки x2:y2'
                      f'{buf_point}={distance}{Color.WHITE}')'''
                y2 += cell
    print(f'--->Верхняя левая точка дома: {x1}:{y1}')
    print(f'--->Правая нижняя точка дома: {x2}:{y2}')
    print(f'----->Верхняя стена дома: {x1}:{y1} ; {x2}:{y1}')
    print(f'----->Правая стена дома: {x2}:{y1} ; {x2}:{y2}')
    print(f'----->Левая стена дома: {x1}:{y1} ; {x1}:{y2}')
    print(f'----->Нижняя стена дома: {x1}:{y2} ; {x2}:{y2}{Color.WHITE}')

    return [x1, y1, x2, y2]


def extend_square3(point1, point2, point3, point4, cell, padding_w, padding_h, height, width):
    """Расширитель здания"""
    # Сперва раздвигаем x раз влево вправо
    for ix in range(random.randint(4, 7)):
        dir = random.randint(0, 1)
        if dir == 0:  # Движение влево
            if point1 <= padding_w + cell * 2:
                point3 += cell  # Нельзя левее, значит правее
            else:
                point1 -= cell
        else:  # Движение вправо
            if point3 >= padding_w + width - cell * 2:
                point1 -= cell
            else:
                point3 += cell

    for iy in range(random.randint(4, 7)):
        dir = random.randint(0, 1)
        if dir == 0:  # Движение вверх
            if point2 <= padding_h + cell * 2:
                point4 += cell  # Нельзя выше, значит ниже
            else:
                point2 -= cell
        else:  # Движение вниз
            if point4 >= padding_h + height - cell * 2:
                point2 -= cell
            else:
                point4 += cell
    return point1, point2, point3, point4


