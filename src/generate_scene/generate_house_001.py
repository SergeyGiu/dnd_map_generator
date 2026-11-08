


def start_generate(data):
    """Основная функция для генерации сцены.
    На вход принимает словарь с параметрами.
    На выходе словарь, содержащий информацию об
    стенах, лампах, путях до картинок и тд"""
    if data.get('width') is None: exit(f"Не хватает параметра width")
    else: width = data.get('width')
    if data.get('height') is None: exit(f"Не хватает параметра height")
    else: height = data.get('height')
    if data.get('padding') is None: exit(f"Не хватает параметра padding")
    else: padding = data.get('padding')
    if data.get('type_scene') is None: exit(f"Не хватает параметра type_scene")
    else: type_scene = data.get('type_scene')
    if data.get('snow_lvl') is None: snow_lvl = 0
    else: snow_lvl = int(data.get('snow_lvl'))
    if data.get('biome') is None: exit(f"Не хватает параметра type_scene")
    else: biome = data.get('biome')
    # direct - направление главного выхода с сектора
    if data.get('direct') is None: direct = 0
    else: direct = int(data.get('direct'))


    walls = []
    light = []
    tiles = []



