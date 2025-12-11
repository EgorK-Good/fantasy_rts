"""Виджет игры с поддержкой строительства"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse, Triangle
from kivy.clock import Clock
from core.constants import BUILDING_PLAN_COLORS

class GameWidget(Widget):
    """Виджет, отображающий игровой мир с поддержкой строительства"""

    def __init__(self, world, selection_system, hud, building_system, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.selection_system = selection_system
        self.hud = hud
        self.building_system = building_system
        self.last_touch_x = 0
        self.last_touch_y = 0

        # Запускаем игровой цикл
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        """Обновление и отрисовка"""
        self.world.update(dt)
        self.canvas.clear()
        self.draw()

    def draw(self):
        """Отрисовка игрового мира"""
        with self.canvas:
            # Темный фон
            Color(0.05, 0.05, 0.1, 1)
            Rectangle(pos=(0, 0), size=self.size)

            # Карта
            for y, row in enumerate(self.world.map.tiles):
                for x, tile in enumerate(row):
                    Color(*tile.color)
                    Rectangle(
                        pos=(x * self.world.map.tile_size, y * self.world.map.tile_size),
                        size=(self.world.map.tile_size, self.world.map.tile_size)
                    )

            # Ресурсы
            for resource in self.world.resource_nodes:
                if resource.resource_type == 'wood':
                    Color(0.2, 0.6, 0.1)
                    Rectangle(pos=(resource.x - 3, resource.y - 10), size=(6, 15))
                    Color(0.1, 0.8, 0.1)
                    Triangle(points=[
                        resource.x - resource.size, resource.y + 5,
                        resource.x + resource.size, resource.y + 5,
                        resource.x, resource.y + resource.size + 15
                    ])
                else:
                    Color(1, 0.8, 0)
                    Ellipse(
                        pos=(resource.x - resource.size/2, resource.y - resource.size/2),
                        size=(resource.size, resource.size)
                    )

            # Здания
            for building in self.world.buildings:
                Color(*building.color)
                Rectangle(
                    pos=(building.x - building.size/2, building.y - building.size/2),
                    size=(building.size, building.size)
                )

            # Здание в режиме планирования
            if self.world.planned_building:
                building = self.world.planned_building

                # Проверяем, можно ли построить здесь
                can_build = building.can_build_here(self.world, self.last_touch_x, self.last_touch_y)

                if can_build:
                    Color(*BUILDING_PLAN_COLORS['VALID'])
                else:
                    Color(*BUILDING_PLAN_COLORS['INVALID'])

                # Рисуем планируемое здание
                Rectangle(
                    pos=(self.last_touch_x - building.size/2, self.last_touch_y - building.size/2),
                    size=(building.size, building.size)
                )

            # Юниты
            for unit in self.world.units:
                Color(*unit.color)
                Ellipse(
                    pos=(unit.x - unit.size/2, unit.y - unit.size/2),
                    size=(unit.size, unit.size)
                )

                if unit.selected:
                    Color(1, 1, 0, 0.8)
                    Line(
                        circle=(unit.x, unit.y, unit.size/2 + 3),
                        width=1.5
                    )

            # Выделение
            selection_area = self.selection_system.get_selection_area()
            if selection_area:
                Color(0.5, 0.5, 1, 0.3)
                Rectangle(
                    pos=selection_area['pos'],
                    size=selection_area['size']
                )

                Color(0, 0.5, 1, 0.8)
                Line(
                    rectangle=(selection_area['pos'][0], selection_area['pos'][1],
                              selection_area['size'][0], selection_area['size'][1]),
                    width=1.5
                )

    def on_touch_down(self, touch):
        """Обработка нажатия"""
        # Пропускаем касания в нижних 150 пикселях (там HUD)
        if touch.y < 150:
            return False

        # Сохраняем позицию для режима строительства
        self.last_touch_x = touch.x
        self.last_touch_y = touch.y

        # Если в режиме строительства - пытаемся разместить здание
        if self.building_system.building_mode and self.building_system.selected_builder:
            if self.building_system.place_building(touch.x, touch.y):
                print(f"✓ Здание размещено в ({touch.x}, {touch.y})")
                return True
            else:
                print(f"✗ Нельзя построить здесь ({touch.x}, {touch.y})")
                return False

        # Обычное выделение
        self.selection_system.start_selection(touch.x, touch.y)
        return True

    def on_touch_move(self, touch):
        """Обработка движения"""
        # Обновляем позицию для режима строительства
        self.last_touch_x = touch.x
        self.last_touch_y = touch.y

        if self.selection_system.selecting:
            self.selection_system.update_selection(touch.x, touch.y)
            return True
        return False

    def on_touch_up(self, touch):
        """Обработка отпускания"""
        if self.selection_system.selecting:
            self.selection_system.finish_selection(touch.x, touch.y, self.world, self.hud)
            return True
        return False