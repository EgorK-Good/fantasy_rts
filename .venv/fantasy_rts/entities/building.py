"""Классы зданий"""
from fantasy_rts.entities.entity import Entity
from fantasy_rts.core import BUILDING_STATS, BUILD_STATES

class Building(Entity):
    """Базовый класс здания"""

    def __init__(self, x, y, building_type):
        stats = BUILDING_STATS[building_type]
        super().__init__(x, y)

        self.building_type = building_type  # ТЕПЕРЬ ЕСТЬ ЭТОТ АТРИБУТ
        self.health = stats['health']
        self.max_health = stats['max_health']
        self.size = stats['size']
        self.color = stats['color']
        self.build_time = stats['build_time']
        self.build_progress = 0.0
        self.build_state = BUILD_STATES['COMPLETE']  # По умолчанию построено
        self.can_train = stats['can_train']
        self.population = stats['population']
        self.description = stats['description']

        # Для обратной совместимости
        self.selected = False

        # Для строительства
        self.builder = None  # Кто строит
        self.is_constructing = False

    def update(self, dt):
        """Обновление состояния здания"""
        if self.build_state == BUILD_STATES['BUILDING'] and self.builder:
            self.build_progress += dt
            if self.build_progress >= self.build_time:
                self.build_state = BUILD_STATES['COMPLETE']
                self.is_constructing = False

    def start_building(self, builder):
        """Начать строительство"""
        self.build_state = BUILD_STATES['BUILDING']
        self.builder = builder
        self.is_constructing = True
        self.build_progress = 0.0

    def can_build_here(self, world, x, y):
        """Проверить, можно ли построить здесь"""
        # Проверяем, не пересекается ли с другими зданиями
        for building in world.buildings:
            if building is not self:  # Не проверяем себя
                dx = building.x - x
                dy = building.y - y
                distance = (dx*dx + dy*dy)**0.5
                min_distance = (self.size + building.size) / 2
                if distance < min_distance:
                    return False

        # Проверяем, не слишком ли близко к краю карты
        if (x < self.size or x > world.map.width * world.map.tile_size - self.size or
            y < self.size or y > world.map.height * world.map.tile_size - self.size):
            return False

        return True

    def get_build_percentage(self):
        """Получить процент завершения строительства"""
        if self.build_time <= 0:
            return 1.0
        return min(self.build_progress / self.build_time, 1.0)

    # Метод для обратной совместимости
    def get_health_percent(self):
        """Получить процент здоровья (для обратной совместимости)"""
        if self.max_health <= 0:
            return 0
        return self.health / self.max_health


class Farm(Building):
    """Ферма - увеличивает лимит населения"""

    def __init__(self, x, y):
        super().__init__(x, y, 'farm')


class Barracks(Building):
    """Казармы - обучает воинов"""

    def __init__(self, x, y):
        super().__init__(x, y, 'barracks')
        self.training_queue = []  # Очередь обучения
        self.current_training = None
        self.training_progress = 0.0

    def update(self, dt):
        super().update(dt)

        # Обновление обучения
        if self.build_state == BUILD_STATES['COMPLETE']:
            if self.current_training:
                self.training_progress += dt
                from fantasy_rts.core import UNIT_STATS
                if self.current_training in UNIT_STATS:
                    build_time = UNIT_STATS[self.current_training]['build_time']
                    if self.training_progress >= build_time:
                        # Юнит готов
                        self.complete_training()
            elif self.training_queue:
                # Начинаем обучение следующего юнита
                self.start_next_training()

    def can_train_unit(self, unit_type, world):
        """Может ли обучить юнита"""
        if unit_type not in self.can_train:
            return False

        # Проверяем лимит населения
        current_population = len([u for u in world.units if hasattr(u, 'unit_type') and u.unit_type != 'worker'])
        max_population = world.get_max_population()
        if current_population >= max_population:
            return False

        return True

    def train_unit(self, unit_type, world):
        """Добавить юнита в очередь обучения"""
        if self.can_train_unit(unit_type, world):
            self.training_queue.append(unit_type)
            return True
        return False

    def start_next_training(self):
        """Начать обучение следующего юнита"""
        if self.training_queue:
            self.current_training = self.training_queue.pop(0)
            self.training_progress = 0.0

    def complete_training(self):
        """Завершить обучение юнита"""
        # Этот метод будет вызван из мира
        self.current_training = None
        self.training_progress = 0.0

    def get_training_percentage(self):
        """Получить процент завершения обучения"""
        if not self.current_training:
            return 0.0

        from fantasy_rts.core import UNIT_STATS
        if self.current_training in UNIT_STATS:
            build_time = UNIT_STATS[self.current_training]['build_time']
            return min(self.training_progress / build_time, 1.0)
        return 0.0