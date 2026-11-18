


class Sector:
    """Тут хранится информация об одном участке на карте"""
    def __init__(self,
                 points,
                 module_name: str,
                 id_scene: str,
                 type_sector: str,
                 ruin_lvl = 0,
                 cell = 50,
                 direct = 'up'
                 ):
        """arg:
            points: list - координаты краёв сектора
            id_scene - id
            module_name - Имя модуля
            type_sector - Тип сеткора(что в нём) Пример house_001
            ruin_lvl - Уровень разрушенности
            cell - размер ячейки
            """

        self.js = {"walls": [],
                   "tiles": []}
        self.id_scene = id_scene
        self.points = points
        self.cell = cell
        self.direct = direct