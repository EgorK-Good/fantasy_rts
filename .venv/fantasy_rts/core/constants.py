"""Константы игры"""

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Размеры тайлов
TILE_SIZE = 40
MAP_WIDTH = 20
MAP_HEIGHT = 15

# Типы ресурсов
RESOURCE_TYPES = {
    'WOOD': 'wood',
    'GOLD': 'gold'
}

# Типы юнитов
UNIT_TYPES = {
    'WORKER': 'worker',
    'INFANTRY': 'infantry',
    'ARCHER': 'archer',
    'COMMANDER': 'commander'
}

# Типы зданий
BUILDING_TYPES = {
    'HEADQUARTERS': 'headquarters',
    'FARM': 'farm',
    'BARRACKS': 'barracks'
}

# Состояния юнитов
UNIT_STATES = {
    'IDLE': 'idle',
    'MOVING': 'moving',
    'GATHERING': 'gathering',
    'RETURNING': 'returning',
    'ATTACKING': 'attacking',
    'BUILDING': 'building'
}

# Цвета для отладки
DEBUG_COLORS = {
    'GRASS': (0.3, 0.7, 0.3),
    'GRASS2': (0.2, 0.6, 0.2),
    'DIRT': (0.6, 0.5, 0.3),
    'SELECTION': (0.5, 0.5, 1, 0.3),
    'SELECTION_BORDER': (0, 0.5, 1, 0.8),
    'HEALTH_GOOD': (0, 1, 0),
    'HEALTH_MEDIUM': (1, 1, 0),
    'HEALTH_LOW': (1, 0, 0)
}

# Характеристики юнитов (базовые)
UNIT_STATS = {
    'worker': {
        'health': 100,
        'damage': 5,
        'armor': 0,
        'speed': 12,
        'size': 18,
        'color': (0.2, 0.7, 0.2),
        'resource_capacity': 100,
        'gather_rate': 10,  # единиц в секунду
        'gather_time': 2.0,  # секунд на сбор
        'cost': {'wood': 50, 'gold': 0},
        'build_time': 10.0,  # Время строительства в секундах
        'can_build': True,   # Может строить здания
        'train_location': 'headquarters'  # Где обучается
    },
    'infantry': {
        'health': 150,
        'damage': 15,
        'armor': 10,
        'speed': 10,
        'size': 22,
        'color': (0.3, 0.3, 0.8),
        'cost': {'wood': 100, 'gold': 50},
        'build_time': 15.0,
        'can_build': False,
        'train_location': 'barracks'  # Требуется казарма
    },
    'archer': {
        'health': 80,
        'damage': 20,
        'armor': 0,
        'speed': 8,
        'size': 20,
        'color': (0.8, 0.5, 0.2),
        'cost': {'wood': 80, 'gold': 100},
        'build_time': 12.0,
        'can_build': False,
        'train_location': 'barracks'  # Требуется казарма
    },
    'commander': {
        'health': 200,
        'damage': 25,
        'armor': 16,
        'speed': 8,
        'size': 24,
        'color': (0.9, 0.1, 0.1),  # Красный
        'cost': {'wood': 200, 'gold': 200},
        'build_time': 30.0,
        'can_build': False,
        'train_location': 'barracks',  # Требуется казарма
        'heal_aura': True  # Может лечить вокруг себя
    }
}

# Характеристики зданий
BUILDING_STATS = {
    'headquarters': {
        'health': 1000,
        'max_health': 1000,
        'size': 60,
        'color': (0.7, 0.3, 0.3),
        'cost': {'wood': 0, 'gold': 0},  # Стартовое
        'build_time': 0,
        'can_train': ['worker'],
        'population': 5,  # +5 к максимальному населению
        'description': 'Главное здание'
    },
    'farm': {
        'health': 500,
        'max_health': 500,
        'size': 40,
        'color': (0.3, 0.7, 0.3),  # Зеленый
        'cost': {'wood': 150, 'gold': 50},
        'build_time': 20.0,
        'can_train': [],
        'population': 5,  # +5 к максимальному населению
        'description': 'Увеличивает лимит войск'
    },
    'barracks': {
        'health': 600,
        'max_health': 600,
        'size': 50,
        'color': (0.3, 0.3, 0.7),  # Синий
        'cost': {'wood': 200, 'gold': 100},
        'build_time': 25.0,
        'can_train': ['infantry', 'archer', 'commander'],
        'population': 0,
        'description': 'Обучает воинов'
    }
}

# Стоимость зданий (дублирование для обратной совместимости)
BUILDING_COSTS = {
    'headquarters': {'wood': 0, 'gold': 0},  # Стартовое
    'farm': {'wood': 150, 'gold': 50},
    'barracks': {'wood': 200, 'gold': 100}
}

# Лимит населения (сколько войск можно иметь)
BASE_POPULATION = 10
POPULATION_PER_FARM = 5

# Состояния строительства
BUILD_STATES = {
    'PLANNING': 'planning',  # Выбор места
    'BUILDING': 'building',  # В процессе строительства
    'COMPLETE': 'complete'   # Построено
}

# Цвета для UI
UI_COLORS = {
    'BACKGROUND': (0.1, 0.1, 0.2, 0.9),  # Темно-синий полупрозрачный
    'PANEL_BG': (0.15, 0.15, 0.25, 0.95),
    'TEXT': (1, 1, 1, 1),  # Белый
    'BUTTON_NORMAL': (0.2, 0.5, 0.8, 1),  # Синий
    'BUTTON_HOVER': (0.3, 0.6, 0.9, 1),
    'BUTTON_PRESSED': (0.1, 0.4, 0.7, 1),
    'BUTTON_GREEN': (0.2, 0.8, 0.3, 1),
    'BUTTON_RED': (0.9, 0.2, 0.2, 1),
    'BUTTON_YELLOW': (0.9, 0.8, 0.2, 1),
    'BUTTON_BLUE': (0.2, 0.6, 0.8, 1),
    'BUTTON_PURPLE': (0.5, 0.2, 0.8, 1),
    'RESOURCE_WOOD': (0.7, 0.5, 0.2, 1),  # Коричневый для дерева
    'RESOURCE_GOLD': (1, 0.8, 0, 1),  # Золотой для золота
    'HEALTH_BAR': (0, 1, 0, 1),
    'SELECTION': (0.2, 0.6, 1, 0.3),
}

# Стили кнопок
BUTTON_STYLE = {
    'font_size': 16,
    'bold': True,
    'border_radius': 10,
    'padding': (10, 5),
}

# Режимы игры
GAME_MODES = {
    'NORMAL': 'normal',
    'BUILDING': 'building',
    'RECRUITING': 'recruiting'
}

# Цвета зданий в режиме планирования
BUILDING_PLAN_COLORS = {
    'VALID': (0.3, 0.7, 0.3, 0.5),    # Зеленый - можно строить
    'INVALID': (0.9, 0.2, 0.2, 0.5),  # Красный - нельзя строить
    'PLANNING': (0.5, 0.5, 0.8, 0.3)  # Синий - режим планирования
}