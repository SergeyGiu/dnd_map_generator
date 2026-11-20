import math

import src.utils
from image_utils import gen_tile_wall, resize_image, open_image, save_image
from utils import generate_id

texture_pack = 'base'

def add_wall(wall, id_scene, elevation, module_name, top = None,
             path_to_texture = None, type_texture = None):
    """Получает на входе координаты отрезка, на выходе полный json"""
    if path_to_texture is not None:
        pass
        # Задана конкретная текстура
        texture_input = path_to_texture
    else:
        # Конкретная не задана, значит смотрим на тип текстуры
        if type_texture is None:
            exit("Не заданы настройки для тайла стены add_wall->(type_texture)")

    if top is None:
        top_elevation = elevation+9
    else:
        top_elevation = top
    gen = generate_id(16)

    js_wall = {
        "light": 20,
        "sight": 20,
        "sound": 20,
        "move": 20,
        "c": [
            wall[0][0],
            wall[0][1],
            wall[1][0],
            wall[1][1]
        ],
        "_id": gen,
        "dir": 0,
        "door": 0,
        "ds": 0,
        "threshold": {
            "light": None,
            "sight": None,
            "sound": None,
            "attenuation": False
        },
        "flags": {
            "wall-height": {
                "bottom": elevation,
                "top": top_elevation}
        },
        "_key": f"!scenes.walls!{id_scene}.{gen}"
    }

    # теперь генерируем тайл для стены
    wall = [wall[0][0], wall[0][1], wall[1][0], wall[1][1]]
    data_tile = {'wall': wall,
                 'key': id_scene,
                 'elevation': elevation,
                 "type_texture": type_texture,
                 "module_name": module_name
                 }
    tile = gen_tile_wall(data_tile)

    return js_wall, tile

def add_door(wall, id_scene, elevation, module_name,
             cell,
             type_door ="single", top = None,
             path_to_texture = None, type_texture = None):
    """Получает на входе координаты отрезка, на выходе полный json"""
    if path_to_texture is not None:
        pass
        # Задана конкретная текстура
        texture_input = path_to_texture
    else:
        # Конкретная не задана, значит смотрим на тип текстуры
        if type_texture is None:
            exit("Не заданы настройки для тайла стены add_wall->add_door(type_texture)")
        else:
            textures = src.utils.choice_texture(
                path=f'images/{texture_pack}/doors/{type_door}/{type_texture}')
            for i in range(len(textures)):
                if "close" in textures[i]:
                    indx = i
                if "open" in textures[i]:
                    indx_open = i
            texture_close_input = textures[indx]
            file_name_close = texture_close_input.split('/')[-1]

            texture_open_input = textures[indx_open]
            file_name_open = texture_open_input.split('/')[-1]

            gen_ile_close = generate_id(16)
            gen_tile_open = generate_id(16)

            path_close_output = f'output/{module_name}/assets/{file_name_close}_{gen_ile_close}.png'
            path_close_module = f'modules/{module_name}/assets/{file_name_close}_{gen_ile_close}.png'

            path_open_output = f'output/{module_name}/assets/{file_name_open}_{gen_tile_open}.png'
            path_open_module = f'modules/{module_name}/assets/{file_name_open}_{gen_tile_open}.png'



    if top is None:
        top_elevation = elevation + 9
    else:
        top_elevation = top
    gen = generate_id(16)
    js_wall = {
        "light": 20,
        "sight": 20,
        "sound": 20,
        "move": 20,
        "c": [
            wall[0][0],
            wall[0][1],
            wall[1][0],
            wall[1][1]
        ],
        "_id": gen,
        "dir": 0,
        "door": 1,
        "ds": 0,
        "threshold": {
            "light": None,
            "sight": None,
            "sound": None,
            "attenuation": False
        },
        "flags": {"wall-height": {
            "bottom": elevation,
            "top": top_elevation}
        },
        "_key": f"!scenes.walls!{id_scene}.{gen}"
    }

    ##################
    gen_tile = generate_id(16)

    ang_cos = src.utils.cos_angle(x1 = wall[0][0], y1=wall[0][1], x2 =wall[1][0], y2=wall[1][1])
    ang_sin = src.utils.sin_angle(x1 = wall[0][0], y1=wall[0][1], x2 =wall[1][0], y2=wall[1][1])

    x = wall[0][0] - cell * ang_sin
    y = wall[0][1] - cell//2*ang_cos

    door_img = open_image(texture_close_input)
    door_img = resize_image(door_img, cell, cell)
    save_image(door_img, path_close_output)

    js_tile = {
        "texture": {
            "src": path_close_module,
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
        "_key": f"!scenes.tiles!{id_scene}.{gen_tile}"
    }

    return js_wall, js_tile

def add_window(wall, id_scene, elevation, top = None,
               path_to_texture = None, type_texture = None):
    """Получает на входе координаты отрезка, на выходе полный json"""
    if top is None:
        top_elevation = elevation + 9
    else:
        top_elevation = top
    gen = generate_id(16)

    js = {
        "light": 30,
        "sight": 30,
        "sound": 20,
        "move": 20,
        "threshold": {
            "light": 10,
            "sight": 10,
            "attenuation": True,
            "sound": None
        },
        "c": [
            wall[0][0],
            wall[0][1],
            wall[1][0],
            wall[1][1]
        ],
        "_id": gen,
        "dir": 0,
        "door": 0,
        "ds": 0,
        "flags": {
            "wall-height": {
                "bottom": elevation,
                "top": top_elevation
            }
        },
        "_key": f"!scenes.walls!{id_scene}.{gen}"
    }

    return js