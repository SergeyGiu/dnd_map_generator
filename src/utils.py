import json
import os
import random
import string
import math


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def init_os():
    """определить операционную систему"""
    import platform

    # Получить краткое имя системы (Windows, Linux, Darwin, ...)
    os_name = platform.system()

    if os_name == "Windows":
        return "Windows"
    elif os_name == "Linux":
        return "Linux"
    elif os_name == "Darwin":
        return "macOS"
    else:
        print(f"Неизвестная система: {os_name}")

def clear_console():
    conf = read_conf()
    my_os = conf.get("os")
    if my_os == "Windows":
        os.system("cls")
    elif my_os == "Linux":
        os.system("clear")
    elif my_os == "MacOS":
        os.system("clear")
    else:
        exit("Неизвестная ОС")


def read_conf():
    try:
        with open('conf/language.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        pass

def write_conf(local_config):
    with open('conf/language.json', 'w', encoding='utf-8') as f:
        json.dump(local_config, f, ensure_ascii=False, indent=4)


def generate_id(length: int = 8) -> str:
    alphabet = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(alphabet) for _ in range(length))

def distance_2d(x1, y1, x2, y2):
    """
    Вычисляет евклидово расстояние между двумя точками на плоскости.

    Args:
        x1, y1: координаты первой точки
        x2, y2: координаты второй точки

    Returns:
        int: расстояние между точками
    """
    return int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))


def tile_add_action(tile, action, params=None, indx=None):
    """Добавляет действие (триггер) к тайлу.

    Args:
        tile: Тайл, к которому добавляется действие.\n
        action: Варианты действия\n
            method - В VTT(Перенаправление на основе метода). В param добавьте
            {"goto": "Куда направить", "method": "Какой метод(enter,... )"}.\n
            checkvariable - В VTT(проверка переменной).
                В param добавьте {
                "tag": "Нужный тэг",
                "var": "Название переменной",
                "goto": "Переход ко входу при провале"(необязательно),
                "value": "Значение"}\n
            setvariable - В VTT(Выставление переменной). В param добавьте {"var": "Имя переменной",
                "value": "Значение переменной", "tag": "Тэг другого тайла(не обязательно, если тайл текущий)"}\n
            elevation - В VTT(Высота). В param добавьте {"elevation": "Нужная высота"}\n
            enter - В VTT(Вход). В param добавьте {"name": "Имя входа"}\n
            playertype - В VTT(Перенаправление в зависимости от от типа игрока).
                В param добавьте {"gm": "куда направить гм-а", "player": "куда направить игрока"}\n
            tileimage - В VTT(Переключение изображения тайла). В param добавьте
                {"tag": "сущность"(не обязательно, если текущий тайл),"select": "Номер изображения", }\n
            text - В VTT(Всплывающий текст). В param добавьте {"text": "текст"}\n
        params: Необязательные параметры действия.
    """

    if params is None:
        params = {}

    flags = tile["flags"]["monks-active-tiles"]
    actions_list = flags.setdefault("actions", [])
    if action == "method":
        new_action = {
                        "action": "method",
                        "data": {
                            "method": params['method'],
                            "goto": params["goto"]
                        },
                        "id": generate_id(16)
                    }
    elif action == "checkvariable":
        if params.get("tag") is None:
            entity = ''
        else:
            entity = {
                  "id": f"tagger:{params['tag']}",
                  "match": "all",
                  "scene": "_active",
                  "name": f"<i class=\"fas fa-tag fa-sm\"></i> {params['tag']}"
                }
        new_action = {
          "action": "checkvariable",
          "data": {
            "entity": entity,
            "type": "all",
            "name": params["var"],
            "value": str(params["value"]),
            "fail": params.get('goto', "")
          },
          "id": generate_id(16)
        }
    elif action == "setvariable":
        if params.get('tag') is None:
            entity = ""
        else:
            entity = {
                "id": f"tagger:{params['tag']}",
                "match": "all",
                "scene": "_active",
                "name": f"<i class=\"fas fa-tag fa-sm\"></i> {params['tag']}"
            }
        new_action = {
                  "action": "setvariable",
                  "data": {
                    "entity": entity,
                    "name": params["var"],
                    "value": params['value'],
                  },
                  "id": generate_id(16)
                }
    elif action == "elevation":
        new_action = {
            "action": "elevation",
            "data": {
                "entity": {
                  "id": "token",
                  "name": "Триггерный токен"
                },
                "value": str(params['elevation'])
              },
            "id": generate_id(16)
          }
    elif action == "enter":
        new_action = {
                  "action": "anchor",
                  "data": {
                    "tag": params['name'],
                    "stop": True
                  },
                  "id": generate_id(16)
                }
    elif action == 'playertype':
        new_action = {
                  "action": "playertype",
                  "data": {
                    "gm": params['gm'],
                    "player": params['player'],
                  },
                  "id": generate_id(16)
                }
    elif action == 'tileimage':
        if params.get('tag') is None:
            entity = {
                      "id": "tile",
                      "name": "Этот тайл"
                    }
        else:
            entity = {
                  "id": f"tagger:{params['tag']}",
                  "match": "all",
                  "scene": "_active",
                  "name": f"<i class=\"fas fa-tag fa-sm\"></i> {params['tag']}"
                    }
        new_action = {
                  "action": "tileimage",
                  "data": {
                    "entity": entity,
                    "select": str(params['select']),
                    "transition": "none",
                    "speed": 1,
                    "loop": 1
                  },
                  "id": generate_id(16)
                }
    elif action == "text":
        new_action = {
                  "action": "scrollingtext",
                  "data": {
                    "text": params.get('text', ""),
                    "entity": {
                      "id": "tile",
                      "name": "Этот тайл"
                    },
                    "for": "trigger",
                    "duration": 5,
                    "anchor": "0",
                    "direction": "2"
                  },
                  "id": generate_id(16)
                }
    else:
        exit("Неизвестный метод триггера")

    if indx is None:
        actions_list.append(new_action)
    else:
        actions_list.insert(indx,new_action)
    tile["flags"]["monks-active-tiles"]['actions'] = actions_list
    return tile


import math

def point_segment_distance(px, py, ax, ay, bx, by):
    """Расстояние от точки (px,py) до отрезка (ax,ay)-(bx,by)."""
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        # Отрезок вырожден в точку
        return math.hypot(px - ax, py - ay)

    # Параметр проекции точки на прямую (0..1 — внутри отрезка)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))  # прижимаем к отрезку

    cx = ax + t * dx
    cy = ay + t * dy
    return math.hypot(px - cx, py - cy)


def min_distance_to_walls(walls, point):
    """
    walls: список стен, каждая стена = [[x1,y1],[x2,y2]]
    point: [x, y]
    Возвращает (min_dist, index_of_wall)
    """
    px, py = point
    best_d = float('inf')
    best_i = -1
    for i, (a, b) in enumerate(walls):
        (ax, ay), (bx, by) = a, b
        d = point_segment_distance(px, py, ax, ay, bx, by)
        if d < best_d:
            best_d = d
            best_i = i
    return int(best_d), best_i


import math

def segment_hits_any_wall(walls, segment, eps=1e-12):
    """
    Проверяет, пересекает ли отрезок segment хотя бы одну стену из walls.

    walls:   список стен, каждая стена = [[x1,y1],[x2,y2]]
    segment: [[x1,y1],[x2,y2]] — проверяемый отрезок
    eps:     допуск для сравнения float

    Возвращает (True/False, index_of_wall или None).
    Касание и коллинеарное наложение считаются пересечением.
    """
    (ax, ay), (bx, by) = segment

    def orient(px, py, qx, qy, rx, ry):
        val = (qx - px) * (ry - py) - (qy - py) * (rx - px)
        if abs(val) < eps:
            return 0
        return 1 if val > 0 else -1

    def on_segment(px, py, qx, qy, rx, ry):
        return (min(px, qx) - eps <= rx <= max(px, qx) + eps and
                min(py, qy) - eps <= ry <= max(py, qy) + eps)

    for i, (c, d) in enumerate(walls):
        (cx, cy), (dx, dy) = c, d

        o1 = orient(ax, ay, bx, by, cx, cy)
        o2 = orient(ax, ay, bx, by, dx, dy)
        o3 = orient(cx, cy, dx, dy, ax, ay)
        o4 = orient(cx, cy, dx, dy, bx, by)

        # Общий случай: концы отрезков по разные стороны
        if o1 != o2 and o3 != o4:
            return True, i

        # Особые случаи: коллинеарность + точка на отрезке
        if o1 == 0 and on_segment(ax, ay, bx, by, cx, cy):
            return True, i
        if o2 == 0 and on_segment(ax, ay, bx, by, dx, dy):
            return True, i
        if o3 == 0 and on_segment(cx, cy, dx, dy, ax, ay):
            return True, i
        if o4 == 0 and on_segment(cx, cy, dx, dy, bx, by):
            return True, i

    return False, None


import math

def min_distance_point_to_polygon(point, polygon):
    """
    Минимальное расстояние от точки до стенок полигона.

    point:    [x, y]
    vertices: [[x1,y1], [x2,y2], ..., [xn,yn]] — вершины полигона по порядку
              (последняя вершина автоматически соединяется с первой)

    Возвращает (min_dist, index_of_edge), где edge i — отрезок
    vertices[i] -> vertices[(i+1) % n].
    """
    vertices = polygon
    px, py = point
    n = len(vertices)

    if n == 0:
        raise ValueError("Полигон не содержит вершин")
    if n == 1:
        ax, ay = vertices[0]
        return math.hypot(px - ax, py - ay), 0

    best_d = float('inf')
    best_i = -1

    for i in range(n):
        ax, ay = vertices[i]
        bx, by = vertices[(i + 1) % n]

        dx = bx - ax
        dy = by - ay

        if dx == 0 and dy == 0:
            d = math.hypot(px - ax, py - ay)
        else:
            # Проекция точки на прямую, прижатая к отрезку
            t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
            if t < 0.0:
                t = 0.0
            elif t > 1.0:
                t = 1.0
            cx = ax + t * dx
            cy = ay + t * dy
            d = math.hypot(px - cx, py - cy)

        if d < best_d:
            best_d = d
            best_i = i

    return int(best_d), best_i


import math
import random

def cut_hole_in_wall(wall, cell, cnt=1, l=None, width=None, offset=None):
    """Делает дыры в отрезке wall шириной width.
        А где именно, рандомно с шагом cell,
        минимальный отступ от края offset.
        Кол-во дыр cnt. Если cnt, то рандомно выбирается где с шагом cell,
         если не задан l, тначе на расстоянии l от первой точки.
        Если дыр больше одной, то стараться на равно расстоянии друг от друга, но не забывать про шаг cell
        На выходе два массива
        """
    if width is None: width = cell
    if offset is None: offset = cell

    # --- Поддержка как одной стены, так и списка стен ---
    is_many = (len(wall) > 0 and isinstance(wall[0][0], (list, tuple)))

    if is_many:
        print(f'{Color.CYAN}---->Режем {len(wall)} стен(ы) '
              f'(cell={cell}, cnt={cnt}, width={width}, offset={offset}, l={l}){Color.WHITE}')
        all_solid = []
        all_holes = []
        for i, w in enumerate(wall):
            print(f'{Color.CYAN}---->Стена #{i}: {w}{Color.WHITE}')
            solid, holes = cut_hole_in_wall(
                wall=w, cell=cell, cnt=cnt, l=l, width=width, offset=offset)
            all_solid.extend(solid)
            all_holes.extend(holes)
        print(f'{Color.CYAN}---->Итого по всем стенам: '
              f'сплошных кусков={len(all_solid)}, дыр={len(all_holes)}{Color.WHITE}')
        return all_solid, all_holes

    # --- Дальше обработка одной стены ---
    (x1, y1), (x2, y2) = wall

    print(f'{Color.CYAN}---->Режем стену {wall} '
          f'(cell={cell}, cnt={cnt}, width={width}, offset={offset}, l={l}){Color.WHITE}')

    # Длина стены и единичный вектор вдоль неё
    wall_len = math.hypot(x2 - x1, y2 - y1)
    if wall_len == 0:
        print(f'{Color.RED}---->Стена вырождена в точку, резать нечего{Color.WHITE}')
        return [wall], []

    ux = (x2 - x1) / wall_len
    uy = (y2 - y1) / wall_len

    # Допустимый диапазон начала дыры вдоль стены (отступ от краёв)
    pos_min = offset
    pos_max = wall_len - offset - width
    if pos_max < pos_min:
        print(f'{Color.RED}---->Стена слишком короткая: '
              f'длина={int(wall_len)}, нужно минимум {int(2 * offset + width)}. '
              f'Оставляем стену целой{Color.WHITE}')
        return [wall], []

    # Шаг сетки: позиции кратны cell, начиная от offset
    def snap(v):
        """Прижать позицию к сетке с шагом cell в пределах [pos_min, pos_max]."""
        k = round((v - pos_min) / cell)
        return min(pos_max, max(pos_min, pos_min + k * cell))

    positions = []

    if cnt == 1:
        if l is not None:
            p = snap(l)
            print(f'{Color.CYAN}---->Одна дыра на заданном l={int(l)} -> позиция {int(p)}{Color.WHITE}')
        else:
            k_max = int((pos_max - pos_min) // cell)
            k = random.randint(0, k_max)
            p = snap(pos_min + k * cell)
            print(f'{Color.CYAN}---->Одна дыра, случайный шаг k={k} -> позиция {int(p)}{Color.WHITE}')
        positions = [p]
    else:
        # Стараемся распределить равномерно, но с шагом cell
        if l is not None:
            p0 = snap(l)
            step = (pos_max - p0) / (cnt - 1) if cnt > 1 else 0
            positions = [snap(p0 + i * step) for i in range(cnt)]
            print(f'{Color.CYAN}---->cnt={cnt}, первая дыра от l={int(l)} -> {int(p0)}, '
                  f'шаг={int(step)}{Color.WHITE}')
        else:
            step = (pos_max - pos_min) / (cnt - 1) if cnt > 1 else 0
            positions = [snap(pos_min + i * step) for i in range(cnt)]
            print(f'{Color.CYAN}---->cnt={cnt}, равномерно по всей длине, '
                  f'шаг={int(step)}{Color.WHITE}')

    # Убираем дубликаты и сортируем (после snap позиции могут совпасть)
    before = len(positions)
    positions = sorted(set(positions))
    if len(positions) < before:
        print(f'{Color.RED}---->После прижатия к сетке часть дыр совпала: '
              f'{before} -> {len(positions)}{Color.WHITE}')
    if len(positions) > cnt:
        positions = positions[:cnt]

    # Строим сегменты: сплошные куски стены и дыры
    solid = []
    holes = []

    def point_at(dist):
        return [int(round(x1 + ux * dist)), int(round(y1 + uy * dist))]

    def fmt(p):
        return f'({p[0]}:{p[1]})'

    cursor = 0.0
    for p in positions:
        hole_start = p
        hole_end = p + width
        if hole_start > cursor:
            solid.append([point_at(cursor), point_at(hole_start)])
            print(f'{Color.GREEN}---->Сплошной кусок: '
                  f'{fmt(solid[-1][0])} -> {fmt(solid[-1][1])}{Color.WHITE}')
        holes.append([point_at(hole_start), point_at(hole_end)])
        print(f'{Color.YELLOW}---->Дыра: '
              f'{fmt(holes[-1][0])} -> {fmt(holes[-1][1])} '
              f'(от {int(hole_start)} до {int(hole_end)}){Color.WHITE}')
        cursor = hole_end

    if cursor < wall_len:
        solid.append([point_at(cursor), point_at(wall_len)])
        print(f'{Color.GREEN}---->Сплошной кусок: '
              f'{fmt(solid[-1][0])} -> {fmt(solid[-1][1])}{Color.WHITE}')

    print(f'{Color.CYAN}---->Итого: сплошных кусков={len(solid)}, дыр={len(holes)}{Color.WHITE}')

    return solid, holes