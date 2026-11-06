import json
import os
from read_write import generate_id

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

    def add_scene(self,name="",height = 1000,width=1000, padding=0.25):
        """Добавить сцену. Значит добавить json в папку scenes/_source"""
        with open('example_jsons/fvtt_Scene.json', 'r', encoding='utf-8') as f:
            scene = json.load(f)
        print(scene)
        gen = generate_id(16)
        if name == "": title = gen
        else: title = name

        scene['name'] = title
        scene['width'] = width
        scene['height'] = height
        scene['padding'] = padding
        scene['_id'] = gen
        scene['_key'] = f'!scenes!{gen}'

        with open(f'{self.folder}/packs/scenes/_source/{name}{gen}.json', 'w', encoding='utf-8') as f:
            json.dump(scene, f, ensure_ascii=False, indent=4)
