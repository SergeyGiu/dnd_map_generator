import os
import shutil
from src.utils import read_conf, clear_console
from src.Module import Module

def delete_tmp_module(folder= "output/module_tmp"):
    if os.path.exists(folder):
        shutil.rmtree(folder)  # удаляем со всем содержимым
    return folder

def menu():
    clear_console()  # Windows
    conf = read_conf()
    title = f"{conf['module_settings']['name_module']}".replace(' ', '-')
    folder = f'output/{title}'
    if os.path.exists(folder):
        shutil.rmtree(folder)  # удаляем со всем содержимым
    module = Module(title=title)

    while True:
        clear_console()


        conf = read_conf()
        lang = conf['lang']
        print(f'{conf[lang]["generate"]}')
        print(f'0-{conf[lang]["back"]}')
        print(f'1-{conf[lang]["scene_add"]}')
        print(f'2-{conf[lang]["actor_add"]}')
        print(f'3-{conf[lang]["module_gen"]}')

        num = input()
        if num == '0' or num == '':
            break
        elif num == '1':
            menu_add_scene(module = module)

        elif num == '2':
            pass
        elif num == '3':
            pack_packs()
            break

def menu_add_scene(module):
    def change_size(data_local):
        while True:
            clear_console()
            conf = read_conf()
            lang = conf['lang']
            x = data_local['width']
            y = data_local['height']
            print(f'{conf[lang]["en_new_scene_size"]} ({x}x{y})')
            print(f'0-{conf[lang]["back"]}')

            num_local = input()
            x,y = num_local.replace('х', 'x').replace('X', 'x').split('x')
            if num_local == '0' or num_local == '':
                break
            try:
                return int(x), int(y)
            except:
                continue

    def change_type_scene(data_local):
        while True:
            clear_console()
            conf = read_conf()
            lang = conf['lang']
            print(f'{conf[lang]["en_new_type_scene"]} ({data_local["type_scene"]})')
            print(f'0-{conf[lang]["back"]}')

            ar_scenes = conf['map_settings']['type_scenes']
            for i in range(len(ar_scenes)):
                print(f'{i+1}-{ar_scenes[i]}')
            num_local = input()
            if num_local == '0' or num_local == '':
                break
            else:
                try:
                    num_local = int(num_local)
                    if num_local > len(ar_scenes) or num_local < 1:
                        continue
                    return ar_scenes[num_local-1]
                except:
                    continue

    conf = read_conf()
    data = {'width':1000, "height":1000,
            "type_scene": conf["map_settings"]["type_scenes"][0],
            "snow_lvl": 0, "biome": "forest", "ruin_level": 0,
            "overgrowth_level": 0, "abandonment_level": 0,
            'padding': conf["map_settings"]["padding"],
            "cell": conf["map_settings"]["cell_size_px"],
            "module_name": conf["module_settings"]["name_module"],}
    while True:
        clear_console()
        conf = read_conf()
        lang = conf['lang']
        print(f'{conf[lang]["settings_scene"]}')
        print(f'0-{conf[lang]["back"]}')
        print(f'1-{conf[lang]["scene_add"]}')
        print(f'2-{conf[lang]["scene_size"]} ({data["width"]}x{data["height"]})')
        print(f'3-{conf[lang]["type_scene"]} ({data["type_scene"]})')
        print(f'4-{conf[lang]["snow_lvl"]} ({data["snow_lvl"]} %)')
        print(f'5-{conf[lang]["biome"]} ({data["biome"]})')
        print(f'6-{conf[lang]["ruin_level"]} ({data["ruin_level"]})')
        print(f'7-{conf[lang]["overgrowth_level"]} ({data["overgrowth_level"]})')
        print(f'8-{conf[lang]["abandonment_level"]} ({data["abandonment_level"]})')




        num = input()

        if num == '0' or num == '':
            break
        elif num == '1':
            #1) Добавляем json чтобы могли его настраивать под нужды
            #js = start_generate(data=data)

            path = module.add_scene(data = data)

            break
        if num == '2':
            data['width'],data['height'] = change_size(data)
            continue
        elif num == '3':
            data['type_scene'] = change_type_scene(data)






def pack_packs():
    os.system('fvtt package pack "scenes" --type "Module" '
              '--inputDirectory "./output/module-auto-gen/packs/scenes/_source"'
              ' --outputDirectory "./output/module-auto-gen/packs"')
    os.system('fvtt package pack "actors" --type "Module" '
              '--inputDirectory "./output/module-auto-gen/packs/actors/_source"'
              ' --outputDirectory "./output/module-auto-gen/packs"')
    os.system('fvtt package pack "items" --type "Module" '
              '--inputDirectory "./output/module-auto-gen/packs/items/_source"'
              ' --outputDirectory "./output/module-auto-gen/packs"')
    os.system('fvtt package pack "journals" --type "Module" '
              '--inputDirectory "./output/module-auto-gen/packs/journals/_source"'
              ' --outputDirectory "./output/module-auto-gen/packs"')
    os.system('fvtt package pack "playlists" --type "Module" '
              '--inputDirectory "./output/module-auto-gen/packs/playlists/_source"'
              ' --outputDirectory "./output/module-auto-gen/packs"')
