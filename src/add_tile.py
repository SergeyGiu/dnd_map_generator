import src.image_utils as image_utils
from src.utils import generate_id, tile_add_action


def luke_and_stairs(data, type_luke = "base", type_stairs = "stick",rotate = 0):
    # Функция создаёт тайл люк, а под ним на уровень ниже тайл лестница
    # и невидимый тайл для триггера

    module_name = data['module_name']
    key = data['key']
    cell = data['cell']
    elevation = data['elevation']
    x = data['x']
    y = data['y']

    tiles = []
    # Рисуем лестницу снизу

    id_tile_stairs = generate_id(16) # id тайла лестница

    id_tile_luke = generate_id(16) # id тайла люк
    id_tile_luke_close = generate_id(16) # id варианта изображения люка
    id_tile_luke_open = generate_id(16) # id варианта изображения люка

    # Информация о лестнице
    out_stair_path = f'output/{module_name}/assets/stairs_001_{key}_{id_tile_stairs}.png'
    module_stair_path = f'modules/{module_name}/assets/stairs_001_{key}_{id_tile_stairs}.png'
    if type_stairs == "stick":
        img_stair = image_utils.open_image('images/stairs/stairs_001.png')
    elif type_stairs == "diagonal_wood":
        img_stair = image_utils.open_image('images/stairs/stairs_diagonal_wood_001.png')
    else:
        exit('Неизвестный тип лестницы')

    image_utils.save_image(img_stair,out_stair_path)

    # Информация о люке закрытом
    out_luke_close_path = f'output/{module_name}/assets/luke_close_{key}_{id_tile_luke}.png'
    module_luke_close_path = f'modules/{module_name}/assets/luke_close_{key}_{id_tile_luke}.png'
    if type_luke == "base":
        img_luke_close = image_utils.open_image('images/interior/luke_001_close.png')
    elif type_luke == "double_door":
        img_luke_close = image_utils.open_image('images/interior/luke_double_001_close.png')
    else: exit('Неизвестное направление')
    image_utils.save_image(img_luke_close, out_luke_close_path)

    # Информация о лшюке открытом
    out_luke_open_path = f'output/{module_name}/assets/luke_open_{key}_{id_tile_luke}.png'
    module_luke_open_path = f'modules/{module_name}/assets/luke_open_{key}_{id_tile_luke}.png'
    if type_luke == "base":
        img_luke_open = image_utils.open_image( 'images/interior/luke_001_open.png')
    elif type_luke == "double_door": \
            img_luke_open = image_utils.open_image('images/interior/luke_double_001_open.png')
    else: exit('Неизвестное направление')
    image_utils.save_image(img_luke_open, out_luke_open_path)

    tag_luke = generate_id(16)

    js_stair = {
            "texture": {
                "src": module_stair_path,
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
            "x": x,
            "y": y,
            "width": cell,
            "height": cell,
            "elevation": elevation-10,
            "sort": 9,
            "occlusion": {
                "mode": 0,
                "alpha": 0
            },
            "_id": id_tile_stairs,
            "rotation": rotate,
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
            "flags": {
                "betterroofs": {
                    "brMode": False
                },
                "levels": {
                    "rangeTop": elevation-1,
                    "allWallBlockSight": False,
                    "showIfAbove": False,
                    "showAboveRange": None,
                    "noCollision": False,
                    "noFogHide": False,
                    "isBasement": False
                },
                "monks-active-tiles": {
                    "name": "",
                    "active": True,
                    "record": False,
                    "restriction": "all",
                    "controlled": "all",
                    "trigger": [
                        "enter",
                        "rightclick"
                    ],
                    "allowpaused": False,
                    "usealpha": False,
                    "pointer": False,
                    "vision": True,
                    "pertoken": False,
                    "minrequired": 0,
                    "cooldown": None,
                    "chance": 100,
                    "fileindex": 1,
                    "actions": [

                    ],
                    "files": [],
                    "variables": {
                        "открыто": 0
                    }
                }
            },
            "_key": f"!scenes.tiles!{key}.{id_tile_stairs}"
        }
    tile_add_action(tile = js_stair, action = 'method', params= {"goto": "Проверка_закрытости", 'method': "enter"})
    tile_add_action(tile=js_stair, action='checkvariable',params={'tag': tag_luke, "var": "открыто", 'value': "1"})
    tile_add_action(tile=js_stair, action='elevation', params={'elevation': elevation})

    tiles.append(js_stair)

    js_luke = {
          "texture": {
            "src": module_luke_close_path,
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
          "x": x,
          "y": y,
          "width": 50,
          "height": 50,
          "elevation": elevation,
          "sort": 3,
          "occlusion": {
            "mode": 0,
            "alpha": 0
          },
          "_id": id_tile_luke,
          "rotation": rotate,
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
          "flags": {
            "betterroofs": {
              "brMode": False
            },
            "levels": {
              "rangeTop": 9,
              "allWallBlockSight": False,
              "showIfAbove": False,
              "showAboveRange": None,
              "noCollision": False,
              "noFogHide": False,
              "isBasement": False
            },
            "monks-active-tiles": {
              "name": "",
              "active": True,
              "record": False,
              "restriction": "all",
              "controlled": "all",
              "trigger": [
                "enter",
                "rightclick"
              ],
              "allowpaused": False,
              "usealpha": False,
              "pointer": False,
              "vision": True,
              "pertoken": False,
              "minrequired": 0,
              "cooldown": None,
              "chance": 100,
              "fileindex": 1,
              "actions": [
              ],
              "files": [
                {
                  "id": id_tile_luke_close,
                  "name": module_luke_close_path,
                  "selected": True
                },
                {
                  "id": id_tile_luke_open,
                  "name": module_luke_open_path,
                  "selected": False
                }
              ],
              "variables": {
                "открыто": 0
              }
            },
            "tagger": {
                  "tags": [
                      tag_luke,
                  ]
              }
          },
          "_key": f"!scenes.tiles!{key}.{id_tile_luke}"
        }

    tile_add_action(tile=js_luke, action='method',params={"goto": "Проверка_закрытости", 'method': "enter"})
    tile_add_action(tile=js_luke, action='checkvariable',params={"var": "открыто", 'value': "1"})
    tile_add_action(tile=js_luke, action='elevation',params={'elevation': elevation-10})
    tile_add_action(tile=js_luke, action='enter',params={'name': "Проверка_закрытости"})
    tile_add_action(tile=js_luke, action='checkvariable',params={"var": "открыто", 'value': "1", 'goto': "открыть"})
    tile_add_action(tile=js_luke, action='playertype',params={"gm": "закрыть",'player': "выход"})
    tile_add_action(tile=js_luke, action='enter',params={'name': "открыть"})
    tile_add_action(tile=js_luke, action='playertype',params={"gm": "точно_открыть",'player': "выход"})
    tile_add_action(tile=js_luke, action='enter',params={'name': "точно_открыть"})
    tile_add_action(tile=js_luke, action='tileimage',params={"select": "2"})
    tile_add_action(tile=js_luke, action='setvariable',params={"value": "1", 'var': "открыто"})
    tile_add_action(tile=js_luke, action='text',params={"text": "открыть"})
    tile_add_action(tile=js_luke, action='enter',params={'name': "закрыть"})
    tile_add_action(tile=js_luke, action='setvariable',params={"value": "0", 'var': "открыто"})
    tile_add_action(tile=js_luke, action='tileimage',params={"select": "1"})
    tile_add_action(tile=js_luke, action='text',params={"text": "закрыть"})
    tile_add_action(tile=js_luke, action='enter',params={'name': "выход"})


    tiles.append(js_luke)
    return tiles


def door():
    """добавить тайл дверь"""
