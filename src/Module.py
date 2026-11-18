import json
import os

import src.generate_sector
from src.utils import generate_id
from src.gen_sector import gen_sector
'''{
  "id": "testclimodule",
  "title": "test_cli_module",
  "version": "1.0.0",
  "compatibility": {
    "minimum": "12",
    "verified": "12"
  },
  "packs": [
    {
      "name": "scene",
      "label": "scene",
      "path": "packs/scene",
      "type": "Scene",
      "system": "dnd5e",
      "ownership": {
        "PLAYER": "OBSERVER",
        "ASSISTANT": "OWNER"
      }
    },
    {
      "name": "journals",
      "label": "journals",
      "path": "packs/journals",
      "type": "JournalEntry",
      "ownership": {
        "PLAYER": "OBSERVER",
        "ASSISTANT": "OWNER"
      },
      "system": "dnd5e"
    },
    {
      "name": "actors",
      "label": "actors",
      "path": "packs/actors",
      "type": "Actor",
      "ownership": {
        "PLAYER": "OBSERVER",
        "ASSISTANT": "OWNER"
      },
      "system": "dnd5e"
    },
    {
      "name": "playlist",
      "label": "playlist",
      "path": "packs/playlist",
      "type": "Playlist",
      "ownership": {
        "PLAYER": "OBSERVER",
        "ASSISTANT": "OWNER"
      },
      "system": "dnd5e"
    },
    {
      "name": "items",
      "label": "items",
      "path": "packs/items",
      "type": "Item",
      "ownership": {
        "PLAYER": "OBSERVER",
        "ASSISTANT": "OWNER"
      },
      "system": "dnd5e"
    }
  ]
}'''

class Module:
    def __init__(self, title):
        self.title = title
        self.id = title.replace('_', '')
        self.folder = f'output/{title}'.replace(' ', '-')
        self.folder_module_json = self.folder+'/module.json'
        self.scenes = []
        os.makedirs(self.folder)
        os.makedirs(self.folder+'/assets')
        os.makedirs(self.folder+'/packs')

        os.makedirs(self.folder+'/packs/scenes')
        os.makedirs(self.folder + '/packs/scenes/_source')

        os.makedirs(self.folder+'/packs/journals')
        os.makedirs(self.folder + '/packs/journals/_source')

        os.makedirs(self.folder+'/packs/actors')
        os.makedirs(self.folder + '/packs/actors/_source')

        os.makedirs(self.folder+'/packs/playlists')
        os.makedirs(self.folder + '/packs/playlists/_source')

        os.makedirs(self.folder+'/packs/items')
        os.makedirs(self.folder + '/packs/items/_source')


        js =  {
          "id": self.id,
          "title": self.title,
          "version": "1.0.0",
          "compatibility": {
            "minimum": "12",
            "verified": "13"
          },
        "packs": [
            {
              "name": "scenes",
              "label": "scenes",
              "path": "packs/scenes",
              "type": "Scene",
              "ownership": {
                "PLAYER": "OBSERVER",
                "ASSISTANT": "OWNER"
              },
              "system": "dnd5e"
            },
            {
                "name": "journals",
                "label": "journals",
                "path": "packs/journals",
                "type": "JournalEntry",
                "ownership": {
                    "PLAYER": "OBSERVER",
                    "ASSISTANT": "OWNER"
                },
                "system": "dnd5e"
            },
            {
                "name": "actors",
                "label": "actors",
                "path": "packs/actors",
                "type": "Actor",
                "ownership": {
                    "PLAYER": "OBSERVER",
                    "ASSISTANT": "OWNER"
                },
                "system": "dnd5e"
            },
            {
                "name": "playlists",
                "label": "playlists",
                "path": "packs/playlists",
                "type": "Playlist",
                "ownership": {
                    "PLAYER": "OBSERVER",
                    "ASSISTANT": "OWNER"
                },
                "system": "dnd5e"
            },
            {
                "name": "items",
                "label": "items",
                "path": "packs/items",
                "type": "Item",
                "ownership": {
                    "PLAYER": "OBSERVER",
                    "ASSISTANT": "OWNER"
                },
                "system": "dnd5e"
            }]
        }
        with open(self.folder_module_json, 'w', encoding='utf-8') as f:
          json.dump(js, f, ensure_ascii=False, indent=4)
        with open(self.folder+'/.gitattributes', 'w', encoding='utf-8') as f:
            f.write('packs/** binary')

    def add_scene(self,name="",height = 1000,width=1000, padding=0.25,
                  data = None):
        """Добавить сцену. Значит добавить json в папку scenes/_source"""
        if data.get('type_scene') is None: exit('Не задан тип сектора')
        if data.get('ruin_level') is None: exit('Не задан уровень разрушенности')
        if data.get('module_name') is None: exit('Не задано имя модуля')
        if data.get('padding') is None: exit('Не задан padding')

        id_scene = generate_id(16)
        padding_w = data['width'] * data['padding']
        padding_h = data['height'] * data['padding']

        points = [[padding_w, padding_h],
                  [padding_w + data['width'], padding_h],
                  [padding_w + data['width'], padding_h + data['height']],
                  [padding_w, data['height'] + padding_h]]

        js_sector = gen_sector(id_scene=id_scene,
                              points=points,
                              type_sector=data.get('type_scene'),
                              ruin_lvl=data.get('ruin_level'),
                              cell=data.get('cell'),
                              module_name=data.get('module_name'),
                               padding = 0.25
                              )

        with open('example_jsons/fvtt_Scene.json', 'r', encoding='utf-8') as f:
            scene = json.load(f)


        if name == "": title = id_scene
        else: title = name

        from src.generate_sector.house_001.main_gen import start_generate

        scene['name'] = title

        scene['_id'] = id_scene
        scene['_key'] = f'!scenes!{id_scene}'


        js = start_generate(data=data, key = id_scene)
        if data is not None:
            if data.get('width') is not None: scene['width'] = data['width']
            else: scene['width'] = width

            if data.get('height') is not None: scene['height'] = data['height']
            else: scene['height'] = height

            if data.get('padding') is not None: scene['padding'] = data['padding']
            else: scene['padding'] = padding



        '''data = {'width':1000, "height":1000,
            "type_scene": conf["map_settings"]["type_scenes"][0],
            "snow_lvl": 0, "biome": "forest", "ruin_level": 0,
            "overgrowth_level": 0, "abandonment_level": 0,
            'padding': conf["map_settings"]["padding"],
            "cell": conf["map_settings"]["cell_size_px"],
            "module_name": conf["module_settings"]["name_module"],}
            '''





        scene['walls'] = js['walls']
        scene['tiles'] = js['tiles']
        scene['flags'] = {
    "levels": {
      "sceneLevels": [
        [
          "-10",
          "-1",
          ""
        ],
        [
          "0",
          "9",
          ""
        ],
        [
          "10",
          "19",
          ""
        ]
      ]
    }
  }




        path = f'{self.folder}/packs/scenes/_source/{name}{id_scene}.json'
        js = {'path':path}
        self.scenes.append(js)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(scene, f, ensure_ascii=False, indent=4)
        return path



