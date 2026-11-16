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


def tile_add_action(tile, action, params=None, indx=None):
    """Добавляет действие (триггер) к тайлу.

    Args:
        tile: Тайл, к которому добавляется действие.
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
                "value": "Значение переменной", "tag": "Тэг другого тайла(не обязательно, если тайл текущий)"}
            elevation - В VTT(Высота). В param добавьте {"elevation": "Нужная высота"}\n
            enter - В VTT(Вход). В param добавьте {"name": "Имя входа"}\n
            playertype - В VTT(Перенаправление в зависимости от от типа игрока).
                В param добавьте {"gm": "куда направить гм-а", "player": "куда направить игрока"}\n
            tileimage - В VTT(Переключение изображения тайла). В param добавьте
                {"tag": "сущность"(не обязательно, если текущий тайл),"select": "Номер изображения", }\n
            text - В VTT(Всплывающий текст). В param добавьте {"text": "текст"}
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
        new_action = {
          "action": "checkvariable",
          "data": {
            "entity": {
              "id": f"tagger:{params['tag']}",
              "match": "all",
              "scene": "_active",
              "name": f"<i class=\"fas fa-tag fa-sm\"></i> {params['tag']}"
            },
            "type": "all",
            "name": params["var"],
            "value": str(params["value"]),
            "fail": params.get('goto', "")
          },
          "id": generate_id(16)
        }
    elif action == "setvariable":
        if params['tag'] is None:
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
        if params['tag'] is None:
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
