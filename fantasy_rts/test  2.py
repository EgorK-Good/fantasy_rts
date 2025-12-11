# test_imports.py
import traceback

print("=== ТЕСТИРОВАНИЕ ВСЕХ ИМПОРТОВ ===")

try:
    print("1. Импорт констант...")
    from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
    print(f"✓ Константы: экран {SCREEN_WIDTH}x{SCREEN_HEIGHT}, тайл {TILE_SIZE}")
except Exception as e:
    print(f"✗ Ошибка констант: {e}")
    print(traceback.format_exc())

try:
    print("\n2. Импорт сущностей...")
    from entities.entity import Entity
    print("✓ Entity импортирован")
    from entities.unit import Unit
    print("✓ Unit импортирован")
    from entities.resource import ResourceNode
    print("✓ ResourceNode импортирован")
    from entities.building import Building, Farm, Barracks
    print("✓ Building, Farm, Barracks импортированы")
    from entities.headquarters import Headquarters
    print("✓ Headquarters импортирован")
except Exception as e:
    print(f"✗ Ошибка сущностей: {e}")
    print(traceback.format_exc())

try:
    print("\n3. Импорт мира...")
    from world.map import GameMap
    print("✓ GameMap импортирован")
    from world.world import World
    print("✓ World импортирован")
except Exception as e:
    print(f"✗ Ошибка мира: {e}")
    print(traceback.format_exc())

try:
    print("\n4. Импорт систем...")
    from systems.selection_system import SelectionSystem
    print("✓ SelectionSystem импортирован")
    from systems.building_system import BuildingSystem
    print("✓ BuildingSystem импортирован")
except Exception as e:
    print(f"✗ Ошибка систем: {e}")
    print(traceback.format_exc())

try:
    print("\n5. Импорт UI...")
    from ui.game_widget import GameWidget
    print("✓ GameWidget импортирован")
    from ui.build_hud import BuildHUD
    print("✓ BuildHUD импортирован")
except Exception as e:
    print(f"✗ Ошибка UI: {e}")
    print(traceback.format_exc())

print("\n=== ТЕСТ ЗАВЕРШЕН ===")
input("Нажмите Enter для выхода...")