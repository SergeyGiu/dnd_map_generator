import os

from main_console import read_conf, write_conf

def menu():
    while True:
        os.system('cls')  # Windows
        conf = read_conf()
        lang = conf['lang']

        print(conf[lang]['settings'])
        print(f'0-{conf[lang]["back"]}')
        print(f'1-{conf[lang]["language_choice"]} ({lang})')
        print(f'2-{conf[lang]["settings_output"]}')
        print(f'3-{conf[lang]["map_settings_lb"]}')
        num = input()

        if num == '0' or num == '':
            break
        elif num == '1':
            menu_choice_lang()
        elif num == '2':
            menu_settings_output()
        elif num == '3':
            menu_map_settings()

def menu_settings_output():
    while True:
        os.system('cls')
        conf = read_conf()
        lang = conf['lang']

        print(f'{conf[lang]["settings_output"]}')
        print(f'0-{conf[lang]["back"]}')
        print(f'1-{conf[lang]["name_module"]} ({conf["module_settings"]["name_module"]})')
        print(f'2-{conf[lang]["name_module_date"]} ({conf["module_settings"]["name_module_date"]})')

        num = input()
        if num == '0' or num == '':
            break
        elif num == '1':
            os.system('cls')
            print(f'{conf[lang]["name_module"]} ({conf["module_settings"]["name_module"]})')
            new_num = input(f'{conf[lang]["en_new_num"]} ')
            if new_num != "":
                conf['module_settings']['name_module'] = new_num
                write_conf(conf)
        elif num == '2':
            os.system('cls')
            print(f'{conf[lang]["name_module_date"]} '
                  f'({conf["module_settings"]["name_module_date"]})')
            print(f'0-{conf[lang]["back"]}')
            print(f'1-Yes')
            print(f'2-No')
            num = input()
            if num == '0' or num == '':
                break
            elif num == '1':
                conf['module_settings']['name_module_date'] = 'Yes'
                write_conf(conf)
            elif num == '2':
                conf['module_settings']['name_module_date'] = 'No'
                write_conf(conf)

def menu_choice_lang():
    while True:
        os.system('cls')  # Windows
        conf = read_conf()
        lang = conf['lang']
        lang_available = conf['lang_available']
        print(f'{conf[lang]["language_choice"]} ({lang})')
        print(f'0-{conf[lang]["back"]}')
        for i in range(len(lang_available)):
            print(f'{i+1}-{lang_available[i]}')
        new_num = input()
        if new_num == '0' or new_num == '':
            break
        else:
            try:
                new_num = int(new_num) - 1
                conf['lang'] = lang_available[new_num]
                write_conf(conf)
                break
            except:
                pass

def menu_map_settings():
    while True:
        os.system('cls')
        conf = read_conf()
        lang = conf['lang']
        print(f'0-{conf[lang]["back"]}')
        print(f'1-{conf[lang]["map"]["cell_size_px"]} '
              f'({conf["map_settings"]["cell_size_px"]})')
        print(f'2-{conf[lang]["map"]["padding"]} '
              f'({conf["map_settings"]["padding"]})')

        num = input()

        if num == '0' or num == '':
            break
        elif num == '1':
            os.system('cls')
            print(f'{conf[lang]["map"]["cell_size_px"]} '
                  f'({conf["map_settings"]["cell_size_px"]})')
            new_num = input(f'{conf[lang]["en_new_num"]} ')
            if new_num != "":
                try:
                    new_num = int(new_num)
                    conf['map_settings']['cell_size_px'] = new_num
                    write_conf(conf)
                except TypeError:
                    pass
        elif num == '2':
            os.system('cls')
            print(f'{conf[lang]["map"]["cell_size_px"]} '
                  f'({conf["map_settings"]["padding"]})')
            new_num = input(f'{conf[lang]["en_new_num"]} ')
            if new_num != "":
                try:
                    new_num = float(new_num)
                    if new_num > 1: new_num = 1.0
                    conf['map_settings']['padding'] = new_num
                    write_conf(conf)
                except TypeError:
                    pass