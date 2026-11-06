import json
import os
import generate_menu, settings_menu

def read_conf():
    with open('conf/language.json', 'r', encoding='utf-8') as f:
        return json.load(f)
def write_conf(local_config):
    with open('conf/language.json', 'w', encoding='utf-8') as f:
        json.dump(local_config, f, ensure_ascii=False, indent=4)

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


