import json
import random
import string

def read_conf():
    with open('conf/language.json', 'r', encoding='utf-8') as f:
        return json.load(f)
def write_conf(local_config):
    with open('conf/language.json', 'w', encoding='utf-8') as f:
        json.dump(local_config, f, ensure_ascii=False, indent=4)


def generate_id(length: int = 8) -> str:
    alphabet = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(alphabet) for _ in range(length))