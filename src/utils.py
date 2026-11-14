import json
import random
import string
import math
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


