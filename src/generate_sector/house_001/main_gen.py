import random
from doctest import debug

import src.image_utils
from src.utils import generate_id, distance_2d
from PIL import Image
from src.image_utils import *
from .utils import *
import src.add_tile
import src.generate_sector.house_001.utils
from src.Sector import Sector
# Эта функция отвечает за постройку однокомнатного
#   дома с уличным туалетом и подвалом. Возвращает один js
#   необходимыми тайлами, стенами, освещением и тд.
# ВНИМАНИЕ
# Тут не строится сама земля, только то что на самой земле.
# Например огород на земле внутри сектора тут делается, но
# сама земля делается не тут.
#
# ВАЖНО!!!
# Глобальные настройки сцены тут не должны учавствовать.
# Мы должны быть локально отделены




def start_generate(data):
    """Основная функция для генерации сцены.
    На вход принимает словарь с параметрами.
    На выходе словарь, содержащий информацию об
    стенах, лампах, путях до картинок и тд\n
    data должен содержать\n
        """
    # Проверка входных данных


    def cut_door(walls_local, direct_local):
        """Вырезает в стене проём для двери
        walls_local - сырой массив стен"""
        walls_up = walls_local[0]
        walls_right = walls_local[1]
        walls_down = walls_local[2]
        walls_left = walls_local[3]


        doors_raw_local = []
        if direct_local == 'up':
            top_left_x = random.randrange(walls_up[0][0] + cell,walls_up[1][0] - cell * 2, cell)
            top_left_y = walls_up[0][1]

            walls_local.append([(walls_up[0][0], walls_up[0][1]),
                                    (top_left_x, top_left_y)])
            walls_local.append([(top_left_x+cell, top_left_y),
                                    (walls_up[1][0], walls_up[1][1])])

            doors_raw_local.append([(top_left_x, top_left_y), (top_left_x+cell, top_left_y)])
            walls_local.pop(0)
        elif direct_local == 'right':
            top_left_x = walls_right[0][0]
            top_left_y =  random.randrange(walls_right[0][1] + cell,walls_right[1][1] - cell * 2, cell)
            walls_local.append([(walls_right[0][0], walls_right[0][1]),
                                (top_left_x, top_left_y)])
            walls_local.append([(top_left_x, top_left_y+cell),
                                (walls_right[1][0], walls_right[1][1])])
            doors_raw_local.append([(top_left_x, top_left_y), (top_left_x, top_left_y+cell)])
            print('Координаты двери:',doors_raw_local[-1])
            print('Координаты стен вокруг двери')
            print('    ', walls_local[-2])
            print('    ', walls_local[-1])

            walls_local.pop(1)
        elif direct_local == 'down':
            top_left_x = random.randrange(walls_down[0][0] + cell,walls_down[1][0] - cell * 2, cell)
            top_left_y = walls_down[0][1]

            walls_local.append([(walls_down[0][0], walls_down[0][1]),
                                (top_left_x, top_left_y)])
            walls_local.append([(top_left_x + cell, top_left_y),
                                (walls_down[1][0], walls_down[1][1])])

            doors_raw_local.append(
                [(top_left_x, top_left_y), (top_left_x + cell, top_left_y)])
            walls_local.pop(2)

        return walls_local,doors_raw_local

    # Присваиваем данные

    type_scene = data.get('type_scene')
    biome = data.get('biome')
    module_name = data.get('module_name')
    sector = data['sector']
    key = sector.id_scene
    cell = sector.cell
    points = sector.points
    direct = sector.direct
    print("Входные данные house_001:")
    print("--->Класс сектор", sector)
    print("--->id сцены:", key)
    print('--->Размер ячейки', cell)
    print("--->Границы сектора", points)
    print("--->Направление сектора", direct)

    walls = []  # Массив стен, окон, дверей в итоговом формате
    light = []  # Массив источников света
    tiles = []  # Массив тайлов

    doors_raw = [] # Массив дверей в сыром виде

    src.generate_sector.house_001.utils.create_start_point(direct=direct,points=points,
                                                           cell = cell)


    width = data['width']
    height = data['height']
    padding = data['padding']

    padding_h = int(height * padding)
    padding_w = int(width * padding)





    # Метод наращивания помещения. Строим центр, а затем расширяем дом в одном из направлений x раз
    # Дом должен стоять в противоположном направлении от direct.
    # То есть при up - дом в нижней части карты.

    # Центр отсчёта дома
    point_x1,point_y1,point_x2,point_y2  = create_start_point3(direct_local=direct,
                                                               padding_w=padding_w,
                                                               padding_h=padding_h,
                                                               cell=cell,
                                                               width=width,
                                                               height=height)
    print('Центр отсчёта здания:', point_x1, point_y1)

    # Расширяем исходную точку в рандомных направлениях, чтобы получить здание
    point_x1, point_y1, point_x2, point_y2 = extend_square(point_x1, point_y1, point_x2, point_y2,
                                                           cell, padding_w, padding_h,
                                                           height, width)

    # Добавляем люк

    # Сырой массив стен
    walls_raw = [[(point_x1, point_y1), (point_x2, point_y1)],
                [(point_x2, point_y1), (point_x2, point_y2)],
                [(point_x1, point_y2),(point_x2, point_y2)],
                [(point_x1, point_y1), (point_x1, point_y2)]]

    # В одной из стен создать дыру для двери в зависимости от direct
    walls_raw,doors_ = cut_door(walls_raw, direct_local=direct)
    doors_raw.extend(doors_)


    # Делаем окна (пропущено)

    # Объявим базовый уровень


    print('Массив сырых стен:', walls_raw)
    # Переводим в нужный формат стены и добавляем к ним тайлы
    for i in range(len(walls_raw)):
        gen_id = generate_id(16)
        js = {
            "light": 20,
            "sight": 20,
            "sound": 20,
            "move": 20,
            "c": [
            walls_raw[i][0][0],
            walls_raw[i][0][1],
            walls_raw[i][1][0],
            walls_raw[i][1][1]
                ],
            "_id": gen_id ,
            "dir": 0,
            "door": 0,
            "ds": 0,
            "threshold": {
            "light": None,
            "sight": None,
            "sound": None,
            "attenuation": False
                },
            "flags": {
                "wall-height": {
                    "bottom": 0,
                    "top": 9}
            },
            "_key": f"!scenes.walls!{key}.{gen_id}"
        }
        wall = [walls_raw[i][0][0], walls_raw[i][0][1], walls_raw[i][1][0], walls_raw[i][1][1]]
        data_tile = {"input_image": 'images/texture_wood/wood_001.png',
                     'wall': wall, 'key': key,
                     'path': f'output/{module_name}/assets/wood_002_{i}.png',
                     'path_': f'modules/{module_name}/assets/wood_002_{i}.png',
                     "range_top": 9,
                     'elevation':0
                     }

        tile = src.image_utils.gen_tile_wall(data_tile)
        tiles.append(tile)
        walls.append(js)

    for i in range(len(doors_raw)):
        gen_id = generate_id(16)
        js = {
            "light": 20,
            "sight": 20,
            "sound": 20,
            "move": 20,
            "c": [
            doors_raw[i][0][0],
            doors_raw[i][0][1],
            doors_raw[i][1][0],
            doors_raw[i][1][1]
                ],
            "_id": gen_id ,
            "dir": 0,
            "door": 1,
            "ds": 0,
            "threshold": {
            "light": None,
            "sight": None,
            "sound": None,
            "attenuation": False
                },
            "flags": { "wall-height": {
                    "bottom": 0,
                    "top": 9}
            },
            "_key": f"!scenes.walls!{key}.{gen_id}"
        }

        door_img = src.image_utils.open_image('images/texture_wood/wood_door_001.png')
        door_img = src.image_utils.resize_image(door_img, cell, cell)
        path_tile = f'output/{module_name}/assets/wood_door_001.png'
        path_tile_ = f'modules/{module_name}/assets/wood_door_001.png'
        save_image(door_img, path_tile)
        left_top = [doors_raw[i][0][0], doors_raw[i][0][1]-cell//2]

        gen_tile = generate_id(16)
        js_tile = {
            "texture": {
                "src": path_tile_,
                "anchorX": 0.5,
                "anchorY": 0.5,
                "offsetX": 0,
                "offsetY": 0,
                "fit": "fill",
                "scaleX": 1,
                "scaleY": 1,
                "rotation": 0,
                "tint": "#ffffff",
                "alphaThreshold": 0.75
            },
            "x": left_top[0],
            "y": left_top[1],
            "width": cell,
            "height": cell,
            "elevation": 0,
            "sort": 8,
            "occlusion": {
                "mode": 0,
                "alpha": 0
            },
            "_id": gen_tile,
            "rotation": 0,
            "alpha": 1,
            "hidden": False,
            "locked": False,
            "restrictions": {
                "light": False,
                "weather": False
            },
            "video": {
                "loop": True,
                "autoplay": True,
                "volume": 0
            },
            "flags": {},
            "_key": f"!scenes.tiles!{key}.{gen_tile}"
        }
        tiles.append(js_tile)
        walls.append(js)


    # Добавить тайл пола
    # Рассчитать внешний полигон
    polygon = build_outer_polygon(walls)
    print('polygon', polygon)
    left_top = get_top_left_point(polygon)

    img_floor_1 = tile_image_to_polygon('images/texture_wood/wood_001.png',points=polygon)
    # Создать конечную картинку
    info = get_image_info(img_floor_1)

    img_floor_1 = darken_near_walls(
        img_floor_1,
        walls=walls,  # глобальные координаты — как есть!
        left_top=left_top,  # глобальная позиция картинки
        distance=cell*0.4,
        max_darkening=0.6,
        falloff="smooth",
        wall_offset=5,  # половина толщины стены
        scene_padding=20,  # запас, чтобы стены за краем дали тень
    )



    gen_tile = generate_id(16)
    out_floor1_path = f'output/{module_name}/assets/floor1_{gen_tile}.png'
    module_floor1_path = f'modules/{module_name}/assets/floor1_{gen_tile}.png'


    js_tile = {
          "texture": {
            "src": module_floor1_path,
            "anchorX": 0.5,
            "anchorY": 0.5,
            "offsetX": 0,
            "offsetY": 0,
            "fit": "fill",
            "scaleX": 1,
            "scaleY": 1,
            "rotation": 0,
            "tint": "#ffffff",
            "alphaThreshold": 0.75
          },
          "x": left_top[0],
          "y": left_top[1],
          "width": info['width'],
          "height": info['height'],
          "elevation": 0,
          "sort": 1,
          "occlusion": {
            "mode": 0,
            "alpha": 0
          },
          "_id": gen_tile ,
          "rotation": 0,
          "alpha": 1,
          "hidden": False,
          "locked": False,
          "restrictions": {
            "light": False,
            "weather": False
          },
          "video": {
            "loop": True,
            "autoplay": True,
            "volume": 0
          },
          "flags": {"betterroofs":
                {
              "brMode": False
                },
              "levels": {
                  "rangeTop": 9,
                  "allWallBlockSight": False}
          },
          "_key": f"!scenes.tiles!{key}.{gen_tile}"
        }
    tiles.append(js_tile)

    # Делаем погреб
    print('Делаем погреб')
    x1,y1,x2,y2 = square_contur(polygon)
    print('Контур дома',  x1,y1,x2,y2)

    # Рандомим будет ли погреб
    if random.randint(1, 100) > 0:
        luke = {"x": random.randrange(point_x1, point_x2, cell),
                "y": random.randrange(point_y1, point_y2, cell),
                'key': key,
                'module_name': module_name,
                'elevation': 0,
                'cell': cell,
                }
        print('Люк расположен:', luke['x'], luke['y'])
        polygon2 = [[luke['x'],luke['y']],
                    [luke['x']+cell, luke['y']],
                    [luke['x']+cell, luke['y']+cell],
                    [luke['x'], luke['y'] + cell]
                    ]
        img_floor_1 = cut_hole(img_floor_1, polygon1=polygon,
                polygon2=polygon2, offset=-5)

        luke_tile = src.add_tile.luke_and_stairs(luke)
        tiles.extend(luke_tile)

        dict_cellar = add_cellar(luke['x'], luke['y'],home_border=[x1, y1, x2, y2], cell=cell,doors= doors_raw)
        walls_cellar = dict_cellar['ar_walls']

        walls_cellar_dict = []
        if dict_cellar.get('coord_outer_luke') is not None:
            luke_outer = {"x": dict_cellar.get('coord_outer_luke')[0],
                    "y": dict_cellar.get('coord_outer_luke')[1],
                    'key': key,
                    'module_name': module_name,
                    'elevation': 0,
                    'cell': cell,
                    }
            print("dict_cellar.get('direct_outer_luke')", dict_cellar.get('direct_outer_luke'))
            if dict_cellar.get('direct_outer_luke') == 'up': rotate = 0
            elif dict_cellar.get('direct_outer_luke') == 'down': rotate = 180
            elif dict_cellar.get('direct_outer_luke') == 'left': rotate = 270
            elif dict_cellar.get('direct_outer_luke') == 'right': rotate = 90
            else:
                exit('Неизвестный наклон')

            print('rotate',rotate)
            luke_tile = src.add_tile.luke_and_stairs(luke_outer, type_stairs='diagonal_wood', rotate=rotate, type_luke='double_door')
            print('Тайлы люка')
            print(*luke_tile, sep='\n')
            tiles.extend(luke_tile)
        for i in range(len(walls_cellar)):

            gen_id = generate_id(16)
            js = {
                "light": 20,
                "sight": 20,
                "sound": 20,
                "move": 20,
                "c": [
                walls_cellar[i][0][0],
                walls_cellar[i][0][1],
                walls_cellar[i][1][0],
                walls_cellar[i][1][1]
                    ],
                "_id": gen_id ,
                "dir": 0,
                "door": 0,
                "ds": 0,
                "threshold": {
                "light": None,
                "sight": None,
                "sound": None,
                "attenuation": False
                    },
                "flags": {
                    "wall-height": {
                        "bottom": -10,
                        "top": -1}
                },
                "_key": f"!scenes.walls!{key}.{gen_id}"
            }
            wall = [walls_cellar[i][0][0], walls_cellar[i][0][1], walls_cellar[i][1][0], walls_cellar[i][1][1]]
            data_tile = {"input_image": 'images/texture_wood/wood_001.png',
                         'wall': wall, 'key': key,
                         'path': f'output/{module_name}/assets/wood_002_{gen_id}_{i}.png',
                         'path_': f'modules/{module_name}/assets/wood_002_{gen_id}_{i}.png',
                         'range_top': -1,
                         "elevation": -10,
                         }
            tile = src.image_utils.gen_tile_wall(data_tile)
            tiles.append(tile)
            walls.append(js)
            walls_cellar_dict.append(js)

        # Добавить тайл пола в подвале
        # Рассчитать внешний полигон
        polygon = build_outer_polygon(walls_cellar_dict)


        left_top = get_top_left_point(polygon)
        if debug:
            print("Дебажим определение тайла и полигона")
            print('Стены подвала', walls_cellar_dict)
            print('внешний контур подвала', polygon)
            print('left_top', left_top)
        img = tile_image_to_polygon('images/texture_stone/stone_001.png',points=polygon)
        # Создать конечную картинку
        info = get_image_info(img)

        img = darken_near_walls(
            img,
            walls=walls,  # глобальные координаты — как есть!
            left_top=left_top,  # глобальная позиция картинки
            distance=cell * 0.4,
            max_darkening=0.6,
            falloff="smooth",
            wall_offset=5,  # половина толщины стены
            scene_padding=20,  # запас, чтобы стены за краем дали тень
        )
        gen_tile = generate_id(16)
        path_tile = f'output/{module_name}/assets/stone_001_{key}_{gen_tile}.png'
        path_tile_ = f'modules/{module_name}/assets/stone_001_{key}_{gen_tile}.png'
        save_image(img, path_tile)
        js_tile = {
            "texture": {
                "src": path_tile_,
                "anchorX": 0.5,
                "anchorY": 0.5,
                "offsetX": 0,
                "offsetY": 0,
                "fit": "fill",
                "scaleX": 1,
                "scaleY": 1,
                "rotation": 0,
                "tint": "#ffffff",
                "alphaThreshold": 0.75
            },
            "x": left_top[0],
            "y": left_top[1],
            "width": info['width'],
            "height": info['height'],
            "elevation": -10,
            "sort": 0,
            "occlusion": {
                "mode": 0,
                "alpha": 0
            },
            "_id": gen_tile,
            "rotation": 0,
            "alpha": 1,
            "hidden": False,
            "locked": False,
            "restrictions": {
                "light": False,
                "weather": False
            },
            "video": {
                "loop": True,
                "autoplay": True,
                "volume": 0
            },
            "flags": {"betterroofs":
                {
                    "brMode": False
                },
                "levels": {
                    "rangeTop": -1,
                    "allWallBlockSight": False}
            },
            "_key": f"!scenes.tiles!{key}.{gen_tile}"
        }
        tiles.append(js_tile)

    save_image(img_floor_1, out_floor1_path)


    # Делаем почву.

    #  По сути будет текстура земли. Из неё делаются выерзки.


    out = {"walls": walls, 'tiles': tiles}
    return out

def square_contur(walls):
    """Определяет крайние точки"""
    x_buf = []
    y_buf = []
    print(walls)
    for i in range(len(walls)):
        x_buf.append(walls[i][0])
        y_buf.append(walls[i][1])
    x_min, x_max = min(x_buf), max(x_buf)
    y_min, y_max = min(y_buf), max(y_buf)
    return x_min,y_min,x_max,y_max

def add_cellar(x,y,
               home_border,
               cell=50, debug=True,
               doors = None):
    """Генерирует погреб, а именно всю структуру, и тайлы и стены.
    Строится примерно как и комната. От центра начинает расширяться.
    Если вышел за границу дома, то должен быть люк на улицу сразу
    hard_border - квадрат за который выходить нельзя"""

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
            if board[0][0] - cell >= home_border[0]:
                if board[0][1] - cell == home_border[1]:
                    flag_left = True
                board[0][0] -= cell
            else:
                flag_left = True
                if flag_right is False:
                    board[1][0] += cell
        else:
            # Расширение направо
            if board[1][0] + cell <= home_border[2]:
                if board[1][0] + cell == home_border[2]:
                    flag_right = True
                board[1][0] += cell
            else:
                flag_right = True
                if flag_left is False:
                    board[0][0] -= cell

    # Расширение по вертикали
    for i in range(size_y):
        if random.randint(0, 1) == 0:
            # Расширение вверх
            if board[0][1] - cell >= home_border[1]:
                if board[0][1] - cell == home_border[1]:
                    flag_up = True
                board[0][1] -= cell
            else:
                flag_up = True
                if flag_down is False:
                    board[1][1] += cell
        else:
            # Расширение вниз
            if board[1][1] + cell <= home_border[3]:
                if board[1][1] + cell == home_border[3]:
                    flag_down = True
                board[1][1] += cell
            else:
                flag_down = True
                if flag_up is False:
                    board[0][1] -= cell

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
        print("Двери в доме", doors)
        if ar_flags:
            print('Подвал подошёл к границе:', ar_flags)
            print("Второй выход находится в", second_exit)
        else:
            print("Подвал не имеет дверей наружу")

    coord_outer_luke = []
    dol = None
    if second_exit != "":
        dol = second_exit
        # Надо найти нужную стену чтобы её разрубить и раширить для ступенек
        if second_exit == 'down':
            wall_exit = [[board[0][0],board[1][1]], [board[1][0],board[1][1]]]
            door_y = wall_exit[0][1]
            while True:
                if wall_exit[0][0] + cell == wall_exit[1][0] - cell * 2:
                    door_x = wall_exit[1][0] - cell * 2
                    break
                else:
                    door_x = random.randrange(wall_exit[0][0] + cell, wall_exit[1][0]-cell*2,cell)
                    for i in range(len(doors)):
                        if door_x == doors[i][0] and door_y == doors[i][1]:
                            # Есть совпадения, заново генерим
                            break
                    else:
                        # Всё норм, совпадений нет, выходи
                        break

            coord_outer_luke = [door_x, door_y]


            ar_doors_local.append([[door_x,door_y],[door_x+cell,door_y]])

            ar_wall_local.append([[wall_exit[0][0], door_y],[door_x,door_y]])
            ar_wall_local.append([[door_x+ cell, door_y],[wall_exit[1][0],door_y]])

            ar_wall_local.append([[door_x, door_y],[door_x,door_y+cell]])
            ar_wall_local.append([[door_x+cell, door_y],[door_x+cell,door_y+cell]])
            ar_wall_local.append([[door_x, door_y+cell],[door_x+cell,door_y+cell]])

            ar_wall_local.append([[board[0][0], board[0][1]],[board[1][0],board[0][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]],[board[0][0],board[1][1]]])
            ar_wall_local.append([[board[1][0],board[0][1]],[board[1][0],board[1][1]]])
        elif second_exit == 'up':
            wall_exit = [[board[0][0],board[0][1]], [board[1][0],board[0][1]]]
            print('wall_exit', wall_exit)
            door_y = wall_exit[0][1]

            while True:
                if wall_exit[0][0] + cell == wall_exit[1][0] - cell * 2:
                    door_x = wall_exit[1][0] - cell * 2
                    break
                else:
                    door_x = random.randrange(wall_exit[0][0] + cell, wall_exit[1][0]-cell*2,cell)
                    for i in range(len(doors)):
                        if door_x == doors[i][0] and door_y == doors[i][1]:
                            # Есть совпадения, заново генерим
                            break
                    else:
                        # Всё норм, совпадений нет, выходи
                        break
            coord_outer_luke = [door_x, door_y-cell]
            ar_doors_local.append([[door_x, door_y], [door_x + cell, door_y]])

            ar_wall_local.append([[wall_exit[0][0], door_y], [door_x, door_y]])
            ar_wall_local.append([[door_x+cell, door_y], [wall_exit[1][0], door_y]])

            ar_wall_local.append([[door_x, door_y], [door_x, door_y - cell]])
            ar_wall_local.append([[door_x + cell, door_y], [door_x + cell, door_y - cell]])
            ar_wall_local.append([[door_x, door_y - cell ], [door_x + cell, door_y - cell]])

            ar_wall_local.append([[board[0][0], board[1][1]],[board[1][0],board[1][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]], [board[0][0], board[1][1]]])
            ar_wall_local.append([[board[1][0], board[0][1]], [board[1][0], board[1][1]]])
        elif second_exit == 'left':
            wall_exit = [[board[0][0],board[0][1]], [board[0][0],board[1][1]]]
            print('wall_exit', wall_exit)
            door_x = wall_exit[0][0]
            while True:
                if wall_exit[0][1] + cell == wall_exit[1][1] - cell * 2:
                    door_y = wall_exit[1][1] - cell * 2
                    break
                else:
                    door_y = random.randrange(wall_exit[0][1] + cell,wall_exit[1][1] - cell * 2,cell)
                    for i in range(len(doors)):
                        if door_x == doors[i][0] and door_y == doors[i][1]:
                            # Есть совпадения, заново генерим
                            break
                    else:
                        # Всё норм, совпадений нет, выходи
                        break
            coord_outer_luke = [door_x-cell, door_y]
            ar_doors_local.append([[door_x, door_y], [door_x, door_y+cell]])

            ar_wall_local.append([[wall_exit[0][0], wall_exit[0][1]], [door_x, door_y]])
            ar_wall_local.append([[door_x, door_y+ cell], [wall_exit[1][0], wall_exit[1][1]]])

            ar_wall_local.append([[door_x, door_y], [door_x-cell, door_y]])
            ar_wall_local.append([[door_x-cell, door_y], [door_x-cell, door_y + cell]])
            ar_wall_local.append([[door_x, door_y+cell], [door_x-cell, door_y + cell]])

            ar_wall_local.append([[board[0][0], board[0][1]],[board[1][0],board[0][1]]])
            ar_wall_local.append([[board[0][0], board[1][1]],[board[1][0],board[1][1]]])
            ar_wall_local.append([[board[1][0], board[0][1]], [board[1][0], board[1][1]]])
        elif second_exit == 'right':
            wall_exit = [[board[1][0],board[0][1]], [board[1][0],board[1][1]]]
            print('wall_exit', wall_exit)

            door_x = wall_exit[0][0]
            while True:
                if wall_exit[0][1] + cell == wall_exit[1][1] - cell * 2:
                    door_y = wall_exit[1][1] - cell * 2
                    break
                else:
                    door_y = random.randrange(wall_exit[0][1] + cell,wall_exit[1][1] - cell * 2,cell)
                    for i in range(len(doors)):
                        if door_x == doors[i][0] and door_y == doors[i][1]:
                            # Есть совпадения, заново генерим
                            break
                    else:
                        # Всё норм, совпадений нет, выходи
                        break
            coord_outer_luke = [door_x, door_y]
            ar_doors_local.append([[door_x, door_y], [door_x, door_y + cell]])

            ar_wall_local.append([[wall_exit[0][0], wall_exit[0][1]], [door_x, door_y]])
            ar_wall_local.append([[door_x, door_y + cell], [wall_exit[1][0], wall_exit[1][1]]])

            ar_wall_local.append([[door_x, door_y], [door_x + cell , door_y]])
            ar_wall_local.append([[door_x + cell , door_y], [door_x + cell , door_y + cell]])
            ar_wall_local.append([[door_x, door_y + cell], [door_x + cell , door_y + cell]])

            ar_wall_local.append([[board[0][0], board[0][1]], [board[1][0], board[0][1]]])
            ar_wall_local.append([[board[0][0], board[1][1]], [board[1][0], board[1][1]]])
            ar_wall_local.append([[board[0][0], board[0][1]], [board[0][0], board[1][1]]])
        else:
            exit("Неизвестное направление")

    return {"ar_walls":ar_wall_local, 'ar_doors':ar_doors_local, 'coord_outer_luke': coord_outer_luke,
            'direct_outer_luke': dol}