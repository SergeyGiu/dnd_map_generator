import random
from typing import Union, Callable, Any

import src.Sector
import importlib


def gen_sector(id_scene,cell, points, type_sector,module_name,padding, ruin_lvl=0) -> \
Union[Callable, Any]:
    """Начало и конец серии генераций
    id_scene - id сцены
    points - координаты вершин сектора. За них постройка не выйдет ни на пиксель
    type_sector - Тип сектора (Например простой дом)
    """
    # direct - направление главного выхода в сектор

    directs = ['up', 'down', 'left', 'right']
    direct = random.choice(directs)


    sector = src.Sector.Sector( id_scene=id_scene,
                     points=points,
                     type_sector = type_sector,
                     ruin_lvl = ruin_lvl,
                     cell = cell,
                     module_name = module_name,
                     direct = direct)

    # 1. Формируем полный путь к модулю
    module_path = f"src.generate_sector.{type_sector}.main_gen"
    # 3. Получаем функцию из импортированного модуля
    data = {
        "sector": sector,
        "padding": padding
    }
    # 2. Динамически импортируем модуль
    try:
        module = importlib.import_module(module_path)


        start_generate = getattr(module, 'start_generate')

        # 4. Вызываем функцию
        if callable(start_generate):
            info_sector = start_generate(data = data)
            return info_sector
        else:
            print("Функция start_generate не найдена или не является вызываемой")

    except ModuleNotFoundError:
        print(f"Модуль {module_path} не найден. Проверьте наличие файла generate_sector.py в папке {type_sector}")
    except AttributeError:
        print(f"В модуле {module_path} нет функции start_generate")

    js_sector = sector.js
    return js_sector