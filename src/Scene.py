import json

from main_console import read_conf,write_conf

class Scene:
    """В этом классе будет храниться информация об одной сцене"""
    def __init__(self, width=None, height=None, padding=None):
        self.width = width
        self.height = height
        self.padding = padding
        js_scene = self.read_example_scene()
        if self.width is not None: js_scene.width = self.width
        if self.height is not None: js_scene.height = self.height
        if self.padding is not None: js_scene.padding = self.padding

        self.js_scene = js_scene

    def read_example_scene(self):
        with open('example_scene.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def export(self):
        return self.js_scene


def add_scene():
    """Создать сцену"""
    conf = read_conf()
    width = 1000
    height = 1000
    scene = Scene(width, # Ширина
                  height, # Высота
                  padding=conf['map_settings']['padding']) # Отступ
    js = scene.export()
