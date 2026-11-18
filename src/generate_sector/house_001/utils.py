import random

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
    min_y = find_bottommost_point(polygon=points, cell=cell)
    max_y = find_topmost_point(polygon=points, cell=cell)
    print("Поиск стартовой точки...")
    print("---> Минимальное расстояние до края:", offset)
    print("---> Массив стен", walls)
    print("-----> Координаты центра", center)
    print("-----> Самая левая точка", min_x)
    print("-----> Самая правая точка", max_x)
    print("-----> Самая верхняя точка", min_y)
    print("-----> Самая нижняя точка", max_y)
    print("---> Направление сектора:", direct)

    if direct == "up":
        print("---->Значит сдвигаем дом в нижнюю часть")
        while True:
            x = random.randrange(min_x[0], max_x[0], cell)
            y = random.randrange(min_y[1],center[1], cell)

    elif direct == "down":
        print("---->Значит сдвигаем дом в верхнюю часть")
    elif direct == "left":
        print("---->Значит сдвигаем дом в правую часть")
    elif direct == "right":
        print("---->Значит сдвигаем дом в левую часть")
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


def extend_square(point1,point2,point3,point4, cell, padding_w, padding_h, height,width):
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


