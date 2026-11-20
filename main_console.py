import json
import os

import src.generate_menu as generate_menu
import src.settings_menu as settings_menu

from src.utils import *
os.environ['TERM'] = 'dumb'
if __name__ == '__main__':
    my_os = init_os()
    conf = read_default_conf()
    list_pack = check_texture_pack()
    conf['os'] = my_os
    conf['map_settings']['texture_packs'] = list_pack
    conf['map_settings']['current_texture_pack'] = 'base'
    write_conf(conf)

    while True:
        clear_console()
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


# Нужно исправить баг со стенами и их тайлами, чтобы не перезаписывалось

# Нужно сделать для лестницы запрет, если люк сверху закрыт, для избегания
#   вылазывания из подвала при закрытом люке

# Вырезать в полу дырку для люка

# Нарисовать такой же люк на улицу