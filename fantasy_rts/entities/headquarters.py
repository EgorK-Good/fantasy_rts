"""Главное здание"""
from fantasy_rts.entities.building import Building
from fantasy_rts.core import UNIT_STATS

class Headquarters(Building):
    """Главное здание игрока - наследуется от Building"""

    def __init__(self, x, y):
        # Используем конструктор родительского класса Building
        super().__init__(x, y, 'headquarters')

        # Переопределяем некоторые атрибуты для обратной совместимости
        self.resources = {
            'wood': 200,
            'gold': 200
        }

        # Статистика
        self.units_trained = 0

    def deliver_resources(self, resources_dict):
        """Принять ресурсы от юнитов"""
        for resource_type, amount in resources_dict.items():
            if resource_type in self.resources:
                self.resources[resource_type] += amount

    def can_train_unit(self, unit_type):
        """Проверить, можно ли обучить юнита"""
        if unit_type not in UNIT_STATS:
            return False

        # Проверяем, может ли штаб обучать этот тип юнитов
        if unit_type not in self.can_train:
            return False

        cost = UNIT_STATS[unit_type].get('cost', {})
        for resource_type, amount in cost.items():
            if self.resources.get(resource_type, 0) < amount:
                return False
        return True

    def train_unit(self, unit_type):
        """Обучить юнита"""
        if not self.can_train_unit(unit_type):
            return False

        cost = UNIT_STATS[unit_type].get('cost', {})
        for resource_type, amount in cost.items():
            self.resources[resource_type] -= amount

        self.units_trained += 1
        return True

    def can_build(self, building_type):
        """Проверить, можно ли построить здание"""
        from fantasy_rts.core import BUILDING_STATS

        if building_type not in BUILDING_STATS:
            return False

        cost = BUILDING_STATS[building_type]['cost']
        for resource_type, amount in cost.items():
            if self.resources.get(resource_type, 0) < amount:
                return False
        return True

    def pay_for_building(self, building_type):
        """Оплатить строительство здания"""
        from fantasy_rts.core import BUILDING_STATS

        if building_type not in BUILDING_STATS:
            return False

        cost = BUILDING_STATS[building_type]['cost']
        for resource_type, amount in cost.items():
            if self.resources.get(resource_type, 0) < amount:
                return False

        for resource_type, amount in cost.items():
            self.resources[resource_type] -= amount

        return True