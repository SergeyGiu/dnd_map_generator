import datetime
import json
import os
import shutil
from read_write import read_conf
from Module import Module

def delete_tmp_module(folder= "output/module_tmp"):
    if os.path.exists(folder):
        shutil.rmtree(folder)  # удаляем со всем содержимым
    return folder

def menu():
    os.system('cls')  # Windows
    conf = read_conf()
    title = f"{conf['module_settings']['name_module']}".replace(' ', '-')
    folder = f'output/{title}'
    if os.path.exists(folder):
        shutil.rmtree(folder)  # удаляем со всем содержимым
    module = Module(title=title)

    while True:
        os.system('cls')  # Windows


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
            module.add_scene()

        elif num == '2':
            pass
        elif num == '3':
            pack_packs()
            break


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
