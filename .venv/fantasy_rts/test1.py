# check_files.py
import os
import sys


def check_project_structure():
    """Проверить структуру проекта"""
    expected_files = [
        'main.py',
        'requirements.txt',
        'core/__init__.py',
        'core/constants.py',
        'entities/__init__.py',
        'entities/entity.py',
        'entities/unit.py',
        'entities/resource.py',
        'entities/building.py',
        'entities/headquarters.py',
        'world/__init__.py',
        'world/map.py',
        'world/world.py',
        'systems/__init__.py',
        'systems/selection_system.py',
        'systems/building_system.py',
        'ui/__init__.py',
        'ui/game_widget.py',
        'ui/build_hud.py',
        'utils/__init__.py',
        'utils/helpers.py'
    ]

    print("=== ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА ===")

    missing_files = []
    for file_path in expected_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"✗ Отсутствует: {file_path}")
        else:
            print(f"✓ Есть: {file_path}")

    if missing_files:
        print(f"\n✗ Отсутствует {len(missing_files)} файлов:")
        for f in missing_files:
            print(f"  - {f}")
        return False

    print("\n✓ Все файлы на месте!")
    return True


if __name__ == "__main__":
    check_project_structure()