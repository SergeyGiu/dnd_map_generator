import json
import os
from src.utils import generate_id

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
        #scene2 = Scene()


        with open('example_jsons/fvtt_Scene.json', 'r', encoding='utf-8') as f:
            scene = json.load(f)

        gen = generate_id(16)
        if name == "": title = gen
        else: title = name

        from src.generate_scene.house_001.generate_main import start_generate


        scene['name'] = title

        scene['_id'] = gen
        scene['_key'] = f'!scenes!{gen}'

        js = start_generate(data=data, key = gen)
        if data is not None:
            if data.get('width') is not None: scene['width'] = data['width']
            else: scene['width'] = width

            if data.get('height') is not None: scene['height'] = data['height']
            else: scene['height'] = height

            if data.get('padding') is not None: scene['padding'] = data['padding']
            else: scene['padding'] = padding


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




        path = f'{self.folder}/packs/scenes/_source/{name}{gen}.json'
        js = {'path':path}
        self.scenes.append(js)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(scene, f, ensure_ascii=False, indent=4)
        return path



