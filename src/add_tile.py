from Tools.demo.spreadsheet import cellname

import src.image_utils as image_utils
from src.utils import generate_id

def luke(data):
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
    id_tile = generate_id(16)
    data['path'] = f'output/{module_name}/assets/stairs_001_{key}_{id_tile}.png'
    data['path_'] = f'modules/{module_name}/assets/stairs_001_{key}_{id_tile}.png'
    data['input_image'] = 'images/stairs/stairs_001.png'
    img = image_utils.open_image(data['input_image'])
    image_utils.save_image(img,data['path'])
    id_trigger = generate_id(16)
    js_tile =  {
        "texture": {
            "src": data['path_'],
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
        "sort": 3,
        "occlusion": {
            "mode": 0,
            "alpha": 0
        },
        "_id": id_tile,
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
                "rangeTop": -1,
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
                    "enter"
                ],
                "allowpaused": False,
                "usealpha": False,
                "pointer": False,
                "vision": True,
                "pertoken": False,
                "minrequired": 0,
                "cooldown": None,
                "chance": 100,
                "fileindex": -1,
                "actions": [
                    {
                        "action": "elevation",
                        "data": {
                            "entity": {
                                "id": "token",
                                "name": "Триггерный токен"
                            },
                            "value": elevation
                        },
                        "id": id_trigger
                    }
                ],
                "files": []
            }
        },
        "_key": f"!scenes.tiles!{key}.{id_tile}"
    }
    tiles.append(js_tile)

    ########################################################################
    id_tile = generate_id(16)
    # Рисуем люк
    id_trigger = generate_id(16)

    data['path'] = f'output/{module_name}/assets/luke_{key}_{id_tile}.png'
    data['path_open'] = f'output/{module_name}/assets/luke_open_{key}_{id_tile}.png'

    data['path_'] = f'modules/{module_name}/assets/luke_{key}_{id_tile}.png'
    data['path_open_'] = f'modules/{module_name}/assets/luke_open_{key}_{id_tile}.png'

    data['input_image'] = 'images/interior/luke_001.png'
    data['input_image_open'] = 'images/interior/luke_001_open.png'

    img = image_utils.open_image(data['input_image'])
    img2 = image_utils.open_image(data['input_image_open'])

    id_close = generate_id(16)
    id_open = generate_id(16)

    image_utils.save_image(img, data['path'])
    image_utils.save_image(img2, data['path_open'])

    actions = []
    for i in range(20):
        actions.append(generate_id(16))

    js_new = {
          "texture": {
            "src": data['path_'],
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
          "_id": id_tile,
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
                  "id": actions[0]
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
                  "id": actions[1]
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
                  "id": actions[2]
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "Проверка_закрытости",
                    "stop": True
                  },
                  "id": actions[3]
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
                  "id": actions[4]
                },
                {
                  "action": "playertype",
                  "data": {
                    "gm": "закрыть",
                    "player": "выход"
                  },
                  "id": actions[5]
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "открыть",
                    "stop": True
                  },
                  "id": actions[6]
                },
                {
                  "action": "playertype",
                  "data": {
                    "gm": "точно_открыть",
                    "player": "выход"
                  },
                  "id": actions[7]
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "точно_открыть",
                    "stop": True
                  },
                  "id": actions[8]
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
                  "id": actions[9]
                },
                {
                  "action": "setvariable",
                  "data": {
                    "entity": "",
                    "name": "открыто",
                    "value": "1"
                  },
                  "id": actions[10]
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
                  "id": actions[11]
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "закрыть",
                    "stop": True
                  },
                  "id": actions[12]
                },
                {
                  "action": "setvariable",
                  "data": {
                    "entity": "",
                    "name": "открыто",
                    "value": "0"
                  },
                  "id": actions[13]
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
                  "id": actions[14]
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
                  "id": actions[15]
                },
                {
                  "action": "anchor",
                  "data": {
                    "tag": "выход",
                    "stop": True
                  },
                  "id": actions[16]
                }
              ],
              "files": [
                {
                  "id": id_close,
                  "name":data['path_'],
                  "selected": True
                },
                {
                  "id": id_open,
                  "name": data['path_open_'],
                  "selected": False
                }
              ],
              "variables": {
                "открыто": 0
              }
            }
          },
          "_key": f"!scenes.tiles!{key}.{id_tile}"
        }

    tiles.append(js_new)
    return tiles
