"""Карта и тайлы"""
from core.constants import DEBUG_COLORS


class Tile:
    """Один тайл карты"""

    def __init__(self, x, y, tile_type):
        self.x = x
        self.y = y
        self.tile_type = tile_type

        # Определяем цвет по типу
        if tile_type == "grass":
            self.color = DEBUG_COLORS['GRASS']
        elif tile_type == "dirt":
            self.color = DEBUG_COLORS['DIRT']
        else:  # grass2
            self.color = DEBUG_COLORS['GRASS2']


class GameMap:
    """Игровая карта"""

    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []
        self.generate_map()

    def generate_map(self):
        """Генерация базовой карты"""
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Простая генерация
                if (x + y) % 3 == 0:
                    tile_type = "grass"
                elif (x + y) % 5 == 0:
                    tile_type = "dirt"
                else:
                    tile_type = "grass2"

                row.append(Tile(x, y, tile_type))
            self.tiles.append(row)

    def world_to_tile(self, world_x, world_y):
        """Преобразование мировых координат в координаты тайла"""
        tile_x = int(world_x // self.tile_size)
        tile_y = int(world_y // self.tile_size)
        return tile_x, tile_y

    def tile_to_world(self, tile_x, tile_y):
        """Преобразование координат тайла в мировые"""
        world_x = tile_x * self.tile_size + self.tile_size / 2
        world_y = tile_y * self.tile_size + self.tile_size / 2
        return world_x, world_y

    def is_valid_position(self, x, y):
        """Проверка, находится ли позиция в пределах карты"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_walkable(self, x, y):
        """Проверка, можно ли пройти по тайлу (заглушка)"""
        if not self.is_valid_position(x, y):
            return False
        # Пока все тайлы проходимы
        return True