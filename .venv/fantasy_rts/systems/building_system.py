"""Система строительства зданий"""
from core.constants import BUILDING_STATS

class BuildingSystem:
    """Система управления строительством"""

    def __init__(self, world):
        self.world = world
        self.building_mode = None
        self.selected_builder = None

    def start_building_mode(self, building_type):
        """Войти в режим строительства"""
        if building_type in ['farm', 'barracks']:
            self.building_mode = building_type
            return True
        return False

    def exit_building_mode(self):
        """Выйти из режима строительства"""
        self.building_mode = None
        self.world.cancel_building_placement()
        self.selected_builder = None

    def select_builder(self, unit):
        """Выбрать строителя"""
        if unit.unit_type == 'worker':
            self.selected_builder = unit
            return True
        return False

    def place_building(self, x, y):
        """Разместить здание в указанных координатах"""
        if not self.building_mode or not self.selected_builder:
            return False

        # Начинаем размещение здания
        planned = self.world.start_building_placement(self.building_mode)
        if not planned:
            return False

        # Пытаемся разместить
        if self.world.place_building(x, y, self.selected_builder):
            # Даем строителю задание
            self.selected_builder.build_target = planned
            self.selected_builder.state = 'building'
            self.selected_builder.target_x = x
            self.selected_builder.target_y = y

            # Выходим из режима строительства
            self.exit_building_mode()
            return True

        return False

    def can_afford_building(self, building_type):
        """Проверить, хватает ли ресурсов на здание"""
        if building_type not in BUILDING_STATS:
            return False

        cost = BUILDING_STATS[building_type]['cost']
        if self.world.headquarters:
            return (self.world.headquarters.resources.get('wood', 0) >= cost.get('wood', 0) and
                    self.world.headquarters.resources.get('gold', 0) >= cost.get('gold', 0))
        return False

    def get_building_cost(self, building_type):
        """Получить стоимость здания"""
        if building_type in BUILDING_STATS:
            return BUILDING_STATS[building_type]['cost']
        return {}