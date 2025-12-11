"""Классы юнитов - с поддержкой строительства"""
from fantasy_rts.core import UNIT_STATS, UNIT_STATES, RESOURCE_TYPES
from fantasy_rts.entities.entity import Entity
import math

class Unit(Entity):
    """Базовый класс юнита с поддержкой строительства"""

    def __init__(self, x, y, unit_type="worker"):
        stats = UNIT_STATS[unit_type]
        super().__init__(x, y)

        self.unit_type = unit_type
        self.target_x = x
        self.target_y = y
        self.state = UNIT_STATES['IDLE']
        self.current_task = None

        # Характеристики из констант
        self.health = stats['health']
        self.max_health = stats['health']
        self.damage = stats['damage']
        self.armor = stats['armor']
        self.speed = stats['speed']
        self.size = stats['size']
        self.color = stats['color']

        # Для работяг
        if unit_type == 'worker':
            self.resource_capacity = stats['resource_capacity']
            self.gather_rate = stats['gather_rate']
            self.gather_time = stats['gather_time']
            self.carried_resources = {RESOURCE_TYPES['WOOD']: 0, RESOURCE_TYPES['GOLD']: 0}
            self.gather_target = None
            self.gather_timer = 0
            self.return_target = None
            self.build_target = None  # Что строит
            self.build_timer = 0.0

        # Для всех юнитов
        self.attack_target = None

    def move_towards_target(self, dt):
        """Движение к цели"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance > 2:
            move_distance = self.speed * dt * 60
            if distance > move_distance:
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance
                self.state = UNIT_STATES['MOVING']
            else:
                self.x = self.target_x
                self.y = self.target_y
                self.state = UNIT_STATES['IDLE']

    def update(self, dt, world):
        """Обновление состояния юнита"""
        if self.state == UNIT_STATES['GATHERING'] and self.gather_target:
            self.update_gathering(dt, world)
        elif self.state == UNIT_STATES['RETURNING'] and self.return_target:
            self.update_returning(dt, world)
        elif self.state == UNIT_STATES['BUILDING'] and self.build_target:
            self.update_building(dt, world)
        elif self.state == UNIT_STATES['MOVING']:
            self.move_towards_target(dt)
        elif self.state == UNIT_STATES['ATTACKING']:
            self.update_attacking(dt, world)

    def update_building(self, dt, world):
        """Обновление строительства"""
        if not self.build_target:
            self.state = UNIT_STATES['IDLE']
            return

        # Проверяем, достигли ли места строительства
        dx = self.build_target.x - self.x
        dy = self.build_target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 40:  # Достаточно близко для строительства
            self.build_timer += dt

            # Работаем над строительством
            if self.build_target.build_state == 'building':
                # Увеличиваем прогресс строительства
                build_speed = 1.0  # Базовая скорость строительства
                self.build_target.build_progress += dt * build_speed

                # Проверяем завершение
                if self.build_target.get_build_percentage() >= 1.0:
                    self.build_target.build_state = 'complete'
                    self.build_target.is_constructing = False
                    self.state = UNIT_STATES['IDLE']
                    self.build_target = None
        else:
            # Двигаемся к месту строительства
            self.target_x = self.build_target.x
            self.target_y = self.build_target.y
            self.move_towards_target(dt)

    def start_building(self, building):
        """Начать строительство здания"""
        self.build_target = building
        self.state = UNIT_STATES['BUILDING']
        self.target_x = building.x
        self.target_y = building.y
        self.build_timer = 0.0