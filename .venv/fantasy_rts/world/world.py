"""Игровой мир"""
from world.map import GameMap
from core.constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, BASE_POPULATION, POPULATION_PER_FARM, BUILDING_STATS
import random

class World:
    """Мир игры с поддержкой зданий и населения"""

    def __init__(self):
        self.map = GameMap(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)
        self.units = []
        self.buildings = []
        self.resource_nodes = []
        self.headquarters = None
        self.planned_building = None

    def add_unit(self, unit):
        """Добавить юнита в мир"""
        self.units.append(unit)

    def add_building(self, building):
        """Добавить здание в мир"""
        self.buildings.append(building)
        if building.building_type == 'headquarters':
            self.headquarters = building

    def add_resource_node(self, resource):
        """Добавить ресурсный узел"""
        self.resource_nodes.append(resource)

    def get_max_population(self):
        """Получить максимальное количество населения"""
        max_pop = BASE_POPULATION
        for building in self.buildings:
            if (hasattr(building, 'building_type') and
                building.building_type == 'farm' and
                building.build_state == 'complete'):
                max_pop += POPULATION_PER_FARM
        return max_pop

    def get_current_population(self):
        """Получить текущее количество населения (без работяг)"""
        return len([u for u in self.units if hasattr(u, 'unit_type') and u.unit_type != 'worker'])

    def can_train_unit(self, unit_type):
        """Можно ли обучить юнита (проверка лимита)"""
        if unit_type == 'worker':
            return True
        current_pop = self.get_current_population()
        max_pop = self.get_max_population()
        return current_pop < max_pop

    def start_building_placement(self, building_type):
        """Начать размещение нового здания"""
        if building_type not in BUILDING_STATS:
            return None

        # Проверяем хватает ли ресурсов
        cost = BUILDING_STATS[building_type]['cost']
        if (self.headquarters and
            (self.headquarters.resources.get('wood', 0) < cost.get('wood', 0) or
             self.headquarters.resources.get('gold', 0) < cost.get('gold', 0))):
            return None

        # Создаем здание в режиме планирования
        from entities.building import Farm, Barracks

        if building_type == 'farm':
            self.planned_building = Farm(0, 0)
        elif building_type == 'barracks':
            self.planned_building = Barracks(0, 0)

        if self.planned_building:
            self.planned_building.build_state = 'planning'
            return self.planned_building

        return None

    def place_building(self, x, y, builder):
        """Разместить здание на карте"""
        if not self.planned_building:
            return False

        # Проверяем, можно ли построить здесь
        if not self.planned_building.can_build_here(self, x, y):
            return False

        # Оплачиваем строительство
        if self.headquarters and not self.headquarters.pay_for_building(self.planned_building.building_type):
            return False

        # Устанавливаем позицию и начинаем строительство
        self.planned_building.x = x
        self.planned_building.y = y
        self.planned_building.start_building(builder)

        # Добавляем в список зданий
        self.buildings.append(self.planned_building)

        # Сбрасываем planned_building
        self.planned_building = None
        return True

    def cancel_building_placement(self):
        """Отменить размещение здания"""
        self.planned_building = None

    def update(self, dt):
        """Обновить состояние мира"""
        # Обновляем юнитов
        for unit in self.units:
            if hasattr(unit, 'update'):
                unit.update(dt, self)

        # Обновляем здания
        for building in self.buildings:
            if hasattr(building, 'update'):
                building.update(dt)

        # Обновляем тренировку в казармах
        for building in self.buildings:
            if hasattr(building, 'training_queue'):
                building.update(dt)

                # Проверяем готовность юнитов
                if (hasattr(building, 'current_training') and
                    building.current_training and
                    building.get_training_percentage() >= 1.0):

                    # Создаем обученного юнита
                    from entities.unit import Unit

                    new_unit = Unit(
                        x=building.x + random.randint(-30, 30),
                        y=building.y + random.randint(-30, 30),
                        unit_type=building.current_training
                    )
                    self.add_unit(new_unit)

                    # Завершаем обучение
                    building.complete_training()

        # Удаляем истощенные ресурсы
        self.resource_nodes = [r for r in self.resource_nodes if not r.is_empty()]

    def generate_resources(self):
        """Генерация ресурсов на карте"""
        # Деревья по краям
        for i in range(25):
            x = random.randint(0, 2) * TILE_SIZE + random.randint(5, 35)
            y = random.randint(0, MAP_HEIGHT-1) * TILE_SIZE + random.randint(5, 35)
            from entities.resource import ResourceNode
            from core.constants import RESOURCE_TYPES
            self.add_resource_node(
                ResourceNode(x, y, RESOURCE_TYPES['WOOD'], random.randint(100, 300))
            )

        for i in range(25):
            x = random.randint(MAP_WIDTH-3, MAP_WIDTH-1) * TILE_SIZE + random.randint(5, 35)
            y = random.randint(0, MAP_HEIGHT-1) * TILE_SIZE + random.randint(5, 35)
            from entities.resource import ResourceNode
            from core.constants import RESOURCE_TYPES
            self.add_resource_node(
                ResourceNode(x, y, RESOURCE_TYPES['WOOD'], random.randint(100, 300))
            )

        # Золотые шахты
        if self.headquarters:
            for i in range(3):
                x = self.headquarters.x + random.randint(-100, 100)
                y = self.headquarters.y + random.randint(-100, 100)
                if 0 <= x < MAP_WIDTH * TILE_SIZE and 0 <= y < MAP_HEIGHT * TILE_SIZE:
                    from entities.resource import ResourceNode
                    from core.constants import RESOURCE_TYPES
                    self.add_resource_node(
                        ResourceNode(x, y, RESOURCE_TYPES['GOLD'], random.randint(200, 500))
                    )