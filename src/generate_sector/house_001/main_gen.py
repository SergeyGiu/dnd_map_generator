import random
from doctest import debug
from typing import Protocol

from add_wall import add_wall, add_door, add_window
from src.utils import Color

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
    biome = data.get('biome')
    sector = data['sector']
    key = sector.id_scene
    cell = sector.cell
    points = sector.points
    module_name = sector.module_name
    direct = sector.direct
    print(f"{Color.YELLOW}Входные данные house_001:")
    print(f"--->Класс сектор:", sector)
    print(f"--->id сцены:", key)
    print(f'--->Имя модуля:', module_name)
    print(f'--->Размер ячейки:', cell)
    print(f"--->Границы сектора:", points, Color.WHITE)
    #print("--->Направление сектора", direct)
    walls = []  # Массив стен, окон, дверей в итоговом формате
    light = []  # Массив источников света
    tiles = []  # Массив тайлов

    doors_raw = [] # Массив дверей в сыром виде
    windows_raw = []
    start_point = src.generate_sector.house_001.utils.create_start_point(
                                    direct=direct,points=points,cell = cell)

    boarders = src.generate_sector.house_001.utils.extend_square(
                            start_point,polygon=points, cell=cell)
    x1,y1,x2,y2 = boarders[0],boarders[1],boarders[2],boarders[3]

    # Сырой массив стен
    walls_raw = [[(x1, y1), (x2, y1)],
                [(x2, y1), (x2, y2)],
                [(x1, y2),(x2, y2)],
                [(x1, y1), (x1, y2)]]

    if direct == 'up':
        print(f'{Color.CYAN}Режем верхнюю стену, чтобы получить дверь')
        ar_wall, ar_door = src.utils.cut_hole_in_wall(wall = walls_raw.pop(0),cell = cell)
        ar_wall2, ar_windows = src.utils.cut_hole_in_wall(wall = walls_raw,cell = cell)
    elif direct == 'right':
        print(f'{Color.CYAN}Режем правую стену, чтобы получить дверь')
        ar_wall, ar_door = src.utils.cut_hole_in_wall(wall=walls_raw.pop(1),cell=cell)
        ar_wall2, ar_windows = src.utils.cut_hole_in_wall(wall = walls_raw,cell = cell)
    elif direct == 'down':
        print(f'{Color.CYAN}Режем нижнюю стену, чтобы получить дверь')
        ar_wall, ar_door = src.utils.cut_hole_in_wall(wall=walls_raw.pop(2),cell=cell)
        ar_wall2, ar_windows = src.utils.cut_hole_in_wall(wall = walls_raw,cell = cell)
    else:
        print(f'{Color.CYAN}Режем левую стену, чтобы получить дверь')
        ar_wall, ar_door = src.utils.cut_hole_in_wall(wall=walls_raw.pop(3),cell=cell)
        ar_wall2, ar_windows = src.utils.cut_hole_in_wall(wall = walls_raw,cell = cell)

    walls_raw = ar_wall
    walls_raw.extend(ar_wall2)

    windows_raw.extend(ar_windows)
    doors_raw.extend(ar_door)

    # Переводим в нужный формат стены и добавляем к ним тайлы
    for i in range(len(walls_raw)):
        js_wall, js_tile = add_wall(wall = walls_raw[i], id_scene = key, elevation=0,
                      module_name = module_name, type_texture='wood')

        tiles.append(js_tile)
        walls.append(js_wall)

    for i in range(len(doors_raw)):
        js_wall, js_tile = add_door(wall = doors_raw[i], id_scene=key,
                      module_name = module_name,
                      type_texture='wood',
                      type_door='single',
                      elevation = 0,
                      cell=cell)

        '''door_img = open_image('images/texture_wood/wood_door_001.png')
        door_img = resize_image(door_img, cell, cell)
        path_tile = f'output/{module_name}/assets/wood_door_001_{gen_tile}.png'
        path_tile_ = f'modules/{module_name}/assets/wood_door_001_{gen_tile}.png'
        save_image(door_img, path_tile)
        left_top = [doors_raw[i][0][0], doors_raw[i][0][1]-cell//2]

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
        }'''
        tiles.append(js_tile)
        walls.append(js_wall)

    for i in range(len(windows_raw)):
        js = add_window(wall = windows_raw[i], id_scene=key, elevation = 0)

        gen_tile = generate_id(16)
        door_img = open_image('images/texture_glass/glass_001.png')
        door_img = resize_image(door_img, cell, cell)
        path_tile = f'output/{module_name}/assets/glass_001_{gen_tile}.png'
        path_tile_ = f'modules/{module_name}/assets/glass_001_{gen_tile}.png'
        save_image(door_img, path_tile)
        left_top = [windows_raw[i][0][0], windows_raw[i][0][1]-cell//2]

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
            "sort": 9,
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
    x1,y1,x2,y2 = square_contur(polygon)

    # Рандомим будет ли погреб
    type_cellar = 'simple_cellar'
    if random.randint(1, 100) > 0:
        print(f"{Color.MAGENTA}Строительство подвала")
        luke = {"x": random.randrange(x1, x2, cell),
                "y": random.randrange(y1, y2, cell),
                'key': key,
                'module_name': module_name,
                'elevation': 0,
                'cell': cell,
                }
        print(f'--->Расположение люка {luke["x"]}:{luke["y"]}')
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
            if dict_cellar.get('direct_outer_luke') == 'up': rotate = 0
            elif dict_cellar.get('direct_outer_luke') == 'down': rotate = 180
            elif dict_cellar.get('direct_outer_luke') == 'left': rotate = 270
            elif dict_cellar.get('direct_outer_luke') == 'right': rotate = 90
            else:
                exit('Неизвестный наклон')

            luke_tile = src.add_tile.luke_and_stairs(luke_outer, type_stairs='diagonal_wood', rotate=rotate, type_luke='double_door')
            tiles.extend(luke_tile)
        for i in range(len(walls_cellar)):
            js_wall, js_tile = add_wall(wall=walls_cellar[i], id_scene = key, elevation=-10,
                     module_name=module_name,type_texture='wood')

            tiles.append(js_tile)
            walls.append(js_wall)
            walls_cellar_dict.append(js_wall)

        # Добавить тайл пола в подвале
        # Рассчитать внешний полигон
        polygon = build_outer_polygon(walls_cellar_dict)


        left_top = get_top_left_point(polygon)
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

        print(Color.WHITE)

    save_image(img_floor_1, out_floor1_path)


    # Делаем почву.

    #  По сути будет текстура земли. Из неё делаются выерзки.


    out = {"walls": walls, 'tiles': tiles}
    return out

def square_contur(walls):
    """Определяет крайние точки"""
    x_buf = []
    y_buf = []
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
        print("--->Границы погреба:", f'{board[0]}:{board[1]}')
        if ar_flags:
            print('--->Подвал подошёл к границе:', ar_flags)
            print("--->Второй выход находится в", second_exit)
        else:
            print("--->Подвал не имеет дверей наружу")

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