def check_input(data):
    if data.get('width') is None: exit(f"Не хватает параметра width")
    if data.get('height') is None: exit(f"Не хватает параметра height")
    if data.get('padding') is None: exit(f"Не хватает параметра padding")
    if data.get('type_scene') is None: exit(
        f"Не хватает параметра type_scene")
    if data.get('biome') is None: exit(f"Не хватает параметра type_scene")
    if data.get('cell') is None: exit(f"Не хватает параметра cell")
    if data.get('module_name') is None: exit(
        f"Не хватает параметра module_name")
    if data.get('snow_lvl') is None: exit(f"Не хватает параметра snow_lvl")