from Tools.demo.spreadsheet import cellname

import src.image_utils as image_utils
from src.utils import generate_id, tile_add_action

def luke_and_stairs(data):
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

    entity_stair = {
        "id": f"Scene.{key}.Tile.{id_tile_stairs}",
        "name": f"Tile: {id_tile_stairs}"
    }

    # Информация о лестнице
    out_stair_path = f'output/{module_name}/assets/stairs_001_{key}_{id_tile_stairs}.png'
    module_stair_path = f'modules/{module_name}/assets/stairs_001_{key}_{id_tile_stairs}.png'
    img_stair = image_utils.open_image('images/stairs/stairs_001.png')
    image_utils.save_image(img_stair,out_stair_path)

    # Информация о люке закрытом
    out_luke_close_path = f'output/{module_name}/assets/luke_close_{key}_{id_tile_luke}.png'
    module_luke_close_path = f'modules/{module_name}/assets/luke_close_{key}_{id_tile_luke}.png'
    img_luke_close = image_utils.open_image('images/interior/luke_001_close.png')
    image_utils.save_image(img_luke_close, out_luke_close_path)

    # Информация о лшюке открытом
    out_luke_open_path = f'output/{module_name}/assets/luke_open_{key}_{id_tile_luke}.png'
    module_luke_open_path = f'modules/{module_name}/assets/luke_open_{key}_{id_tile_luke}.png'
    img_luke_open = image_utils.open_image( 'images/interior/luke_001_open.png')
    image_utils.save_image(img_luke_open, out_luke_open_path)

    tag_luke = generate_id(16)

    actions = []
    for i in range(40):
        actions.append(generate_id(16))
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
    #print(js_stair)
    tile_add_action(tile = js_stair, action = 'method', params= {"goto": "Проверка_закрытости", 'method': "enter"})
    tile_add_action(tile=js_stair, action='checkvariable',params={'tag': tag_luke, "var": "открыто", 'value': "1"})
    tile_add_action(tile=js_stair, action='elevation', params={'elevation': elevation})

    #print(js_stair)

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
                {
                  "action": "method",
                  "data": {
                    "method": "enter",
                    "goto": "Проверка_закрытости"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "checkvariable",
                  "data": {
                    "entity": "",
                    "type": "all",
                    "name": "открыто",
                    "value": "1",
                    "fail": ""
                  },
                  "id":generate_id(16)
                },
                {
                  "action": "elevation",
                  "data": {
                    "entity": {
                      "id": "token",
                      "name": "Триггерный токен"
                    },
                    "value": elevation-10
                  },
                  "id":generate_id(16)
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "Проверка_закрытости",
                    "stop": True
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "checkvariable",
                  "data": {
                    "entity": "",
                    "type": "all",
                    "name": "открыто",
                    "value": "1",
                    "fail": "открыть"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "playertype",
                  "data": {
                    "gm": "закрыть",
                    "player": "выход"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "открыть",
                    "stop": True
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "playertype",
                  "data": {
                    "gm": "точно_открыть",
                    "player": "выход"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "точно_открыть",
                    "stop": True
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "tileimage",
                  "data": {
                    "entity": {
                      "id": "tile",
                      "name": "Этот тайл"
                    },
                    "select": "2",
                    "transition": "none",
                    "speed": 1,
                    "loop": 1
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "setvariable",
                  "data": {
                    "entity": "",
                    "name": "открыто",
                    "value": "1"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "scrollingtext",
                  "data": {
                    "text": "Открыть",
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
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "закрыть",
                    "stop": True
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "setvariable",
                  "data": {
                    "entity": "",
                    "name": "открыто",
                    "value": "0"
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "tileimage",
                  "data": {
                    "entity": {
                      "id": "tile",
                      "name": "Этот тайл"
                    },
                    "select": "1",
                    "transition": "none",
                    "speed": 1,
                    "loop": 1
                  },
                  "id": generate_id(16)
                },
                {
                  "action": "scrollingtext",
                  "data": {
                    "text": "Закрыть",
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
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "выход",
                    "stop": True
                  },
                  "id": generate_id(16)
                }
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

    tiles.append(js_luke)
    return tiles
