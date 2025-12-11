"""Ресурсные узлы"""
from fantasy_rts.core import RESOURCE_TYPES


class ResourceNode:
    """Узел ресурсов на карте"""

    def __init__(self, x, y, resource_type, amount):
        self.x = x
        self.y = y
        self.resource_type = resource_type
        self.amount = amount
        self.max_amount = amount

        # Визуальные параметры
        if resource_type == RESOURCE_TYPES['WOOD']:
            self.color = (0.2, 0.6, 0.1)
            self.size = 25
        else:  # GOLD
            self.color = (1, 0.8, 0)
            self.size = 20

    def gather(self, amount):
        """Собрать указанное количество ресурсов"""
        gather_amount = min(amount, self.amount)
        self.amount -= gather_amount
        return gather_amount

    def is_empty(self):
        """Проверка, истощены ли ресурсы"""
        return self.amount <= 0

    def get_percentage(self):
        """Получить процент оставшихся ресурсов"""
        if self.max_amount <= 0:
            return 0
        return self.amount / self.max_amount