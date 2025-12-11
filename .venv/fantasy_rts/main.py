"""Главный файл игры с системой строительства"""
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock

from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from world.world import World
from entities.headquarters import Headquarters
from entities.unit import Unit
from systems.selection_system import SelectionSystem
from systems.building_system import BuildingSystem
from ui.game_widget import GameWidget
from ui.build_hud import BuildHUD

import traceback
import random

print("=== ЗАПУСК ИГРЫ С СИСТЕМОЙ СТРОИТЕЛЬСТВА ===")

class GameUI(FloatLayout):
    """Основной интерфейс игры"""

    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)

            print("✓ Инициализация GameUI")

            # Инициализируем мир
            self.world = World()
            print("✓ Мир создан")

            # Создаем штаб игрока
            hq_x = SCREEN_WIDTH // 4
            hq_y = SCREEN_HEIGHT // 2
            hq = Headquarters(hq_x, hq_y)
            self.world.add_building(hq)
            print("✓ Штаб создан")

            # Создаем несколько работяг
            for i in range(3):
                worker = Unit(
                    hq_x + random.randint(-80, 80),
                    hq_y + random.randint(-80, 80),
                    "worker"
                )
                self.world.add_unit(worker)

            print(f"✓ Всего юнитов: {len(self.world.units)}")

            # Генерируем ресурсы
            self.world.generate_resources()
            print(f"✓ Ресурсов создано: {len(self.world.resource_nodes)}")

            # Система выделения
            self.selection_system = SelectionSystem()
            print("✓ Система выделения создана")

            # Система строительства
            self.building_system = BuildingSystem(self.world)
            print("✓ Система строительства создана")

            # HUD
            self.hud = BuildHUD(self.world, self.selection_system, self.building_system)
            self.hud.size_hint = (1, 1)
            self.add_widget(self.hud)
            print("✓ HUD создан и добавлен")

            # Виджет игры
            self.game_widget = GameWidget(
                world=self.world,
                selection_system=self.selection_system,
                hud=self.hud,
                building_system=self.building_system
            )
            self.game_widget.size_hint = (1, 1)
            self.add_widget(self.game_widget)
            print("✓ Виджет игры создан")

            # ОБЯЗАТЕЛЬНО: Делаем HUD поверх игры
            self.remove_widget(self.hud)
            self.remove_widget(self.game_widget)

            # Сначала игра (нижний слой)
            self.add_widget(self.game_widget)
            # Потом HUD (верхний слой)
            self.add_widget(self.hud)

            print("✓ Порядок виджетов установлен: Игра → HUD (поверх)")

            # Обновление HUD
            Clock.schedule_interval(self.update_hud, 1.0/10.0)
            print("✓ Таймер HUD установлен")

            print("\n=== ИГРА ГОТОВА ===")
            print("🎮 УПРАВЛЕНИЕ:")
            print("  ЛКМ по юниту - выбрать")
            print("  ЛКМ + движение - выделить область")
            print("  ЛКМ по земле - движение выделенных юнитов")
            print("  ЛКМ по ресурсу - сбор ресурсов")
            print("  🏗️ Строить - войти в режим строительства")
            print("  🎯 Работяга - обучить нового работягу")
            print("  ⏹ Стоп - остановить выделенных юнитов")
            print("  🏠 Вернуть - вернуть работягов на базу")
            print("  Выберите казарму для найма войск")

        except Exception as e:
            print(f"✗ Ошибка в GameUI.__init__: {e}")
            print(traceback.format_exc())
            raise

    def update_hud(self, dt):
        """Обновление HUD"""
        self.hud.update()

class FantasyRTS(App):
    """Главное приложение"""

    def build(self):
        print("=== СОЗДАНИЕ ИНТЕРФЕЙСА ===")
        try:
            self.title = "Fantasy RTS - Система строительства"
            Window.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
            Window.clearcolor = (0.1, 0.1, 0.2, 1)
            return GameUI()
        except Exception as e:
            print(f"✗ Ошибка в build(): {e}")
            print(traceback.format_exc())
            raise

if __name__ == '__main__':
    try:
        FantasyRTS().run()
    except Exception as e:
        print(f"✗ Критическая ошибка: {e}")
        print(traceback.format_exc())
        input("Нажмите Enter для выхода...")