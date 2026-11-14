import random

def create_start_point(direct_local,padding_w, padding_h, cell, width, height):
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