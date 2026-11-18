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
                  data = None, global_light = True):
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

        cell = data['cell']
        js_sector = gen_sector(id_scene=id_scene,
                              points=points,
                              type_sector=data.get('type_scene'),
                              ruin_lvl=data.get('ruin_level'),
                              cell=cell,
                              module_name=data['module_name'],
                               padding = 0.25
                              )
        # Создать шаблон сцены
        if name == "": name = id_scene


        walls = js_sector['walls']
        tiles = js_sector['tiles']

        scene = {
          "name": name,
          "navigation": False,
          "navOrder": 0,
          "navName": "",
          "background": {
            "src": None,
            "anchorX": 0,
            "anchorY": 0,
            "offsetX": 0,
            "offsetY": 0,
            "fit": "fill",
            "scaleX": 1,
            "scaleY": 1,
            "rotation": 0,
            "tint": "#ffffff",
            "alphaThreshold": 0
          },
          "foreground": None,
          "foregroundElevation": 20,
          "thumb": None,
          "width": width,
          "height": height,
          "padding": padding,
          "initial": {
            "x": None,
            "y": None,
            "scale": 0.5
          },
          "backgroundColor": "#999999",
          "grid": {
            "type": 1,
            "size": cell,
            "style": "solidLines",
            "thickness": 1,
            "color": "#000000",
            "alpha": 0.2,
            "distance": 5,
            "units": "ft"
          },
          "tokenVision": True,
          "fog": {
            "exploration": False,
            "overlay": None,
            "colors": {
              "explored": None,
              "unexplored": None
            }
          },
          "environment": {
            "darknessLevel": 0,
            "darknessLock": False,
            "globalLight": {
              "enabled": global_light,
              "alpha": 0.5,
              "bright": False,
              "color": None,
              "coloration": 1,
              "luminosity": 0,
              "saturation": 0,
              "contrast": 0,
              "shadows": 0,
              "darkness": {
                "min": 0,
                "max": 1
              }
            },
            "cycle": True,
            "base": {
              "hue": 0,
              "intensity": 0,
              "luminosity": 0,
              "saturation": 0,
              "shadows": 0
            },
            "dark": {
              "hue": 0.7138888888888889,
              "intensity": 0,
              "luminosity": -0.25,
              "saturation": 0,
              "shadows": 0
            }
          },
          "drawings": [],
          "tokens": [],
          "lights": [],
          "notes": [],
          "sounds": [],
          "regions": [],
          "templates": [],
          "tiles": tiles,
          "walls": walls,
          "playlist": None,
          "playlistSound": None,
          "journal": None,
          "journalEntryPage": None,
          "weather": "",
          "folder": None,
          "ownership": {
            "default": 0,
            "gwA7Bkmj54EdZvsA": 3
          },
          "flags": {},
          "_stats": {
            "compendiumSource": None,
            "duplicateSource": None,
            "coreVersion": "12.331",
            "systemId": "dnd5e",
            "systemVersion": "4.4.2",
            "createdTime": 1793968374286,
            "modifiedTime": 1793968430130,
            "lastModifiedBy": "gwA7Bkmj54EdZvsA"
          },
          "_id": id_scene,
          "active": False,
          "sort": 100000,
          "_key": f"!scenes!{id_scene}",
          "levels": []
        }


        '''# Взять образец сцены
        with open('example_jsons/fvtt_Scene.json', 'r', encoding='utf-8') as f:
            scene = json.load(f)'''


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



