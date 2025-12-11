"""Базовый класс для всех игровых сущностей"""


class Entity:
    """Базовый класс всех игровых объектов"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.selected = False
        self.health = 100
        self.max_health = 100
        self.size = 20
        self.color = (1, 1, 1)

    def update(self, dt):
        """Обновление состояния сущности"""
        pass

    def draw(self, canvas):
        """Отрисовка сущности"""
        pass

    def is_point_inside(self, x, y):
        """Проверка, находится ли точка внутри сущности"""
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance < self.size

    def get_health_percent(self):
        """Получение процента здоровья"""
        if self.max_health <= 0:
            return 0
        return self.health / self.max_health