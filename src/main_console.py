import json
import os
import generate_menu, settings_menu
from read_write import read_conf,write_conf

if __name__ == '__main__':
    while True:
        os.system('cls')  # Windows

        conf = read_conf()
        lang = conf['lang']
        print(conf[lang]['menu_main_lb'])
        print(f'0-{conf[lang]["exit"]}')
        print(f'1-{conf[lang]["settings"]}')
        print(f'2-{conf[lang]["generate"]}')
        num = input()

        if num == '0':
            break
        elif num == '1':
            settings_menu.menu()
        elif num == '2':
            generate_menu.menu()


