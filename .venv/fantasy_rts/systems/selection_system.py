"""Система выделения юнитов"""
from utils.helpers import point_in_rect

class SelectionSystem:
    """Система управления выделением юнитов"""

    def __init__(self):
        self.selection_start = None
        self.selection_end = None
        self.selecting = False
        self.selected_units = []

    def start_selection(self, x, y):
        """Начать выделение"""
        self.selection_start = (x, y)
        self.selecting = True

    def update_selection(self, x, y):
        """Обновить выделение (при движении мыши/пальца)"""
        if self.selecting:
            self.selection_end = (x, y)

    def finish_selection(self, x, y, world, hud):
        """Завершить выделение"""
        if not self.selecting:
            return

        self.selection_end = (x, y)

        # Определяем область выделения
        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        left = min(x1, x2)
        right = max(x1, x2)
        bottom = min(y1, y2)
        top = max(y1, y2)

        # Если область достаточно большая - выделяем юнитов в области
        if (right - left) > 10 or (top - bottom) > 10:
            self.select_units_in_area(left, right, bottom, top, world)
        else:
            # Если клик - проверяем, по чему кликнули
            self.handle_click(x1, y1, world, hud)

        self.selecting = False
        self.selection_start = None
        self.selection_end = None

    def select_units_in_area(self, left, right, bottom, top, world):
        """Выделить юнитов в области"""
        # Сначала снимаем выделение со всех
        self.clear_selection()

        # Выделяем юнитов в области
        for unit in world.units:
            if left <= unit.x <= right and bottom <= unit.y <= top:
                unit.selected = True
                self.selected_units.append(unit)

    def handle_click(self, x, y, world, hud):
        """Обработка одиночного клика"""
        # 1. Проверяем, кликнули ли по уже выделенному юниту
        clicked_unit = None
        for unit in self.selected_units:
            dx = unit.x - x
            dy = unit.y - y
            distance = (dx*dx + dy*dy)**0.5
            if distance < unit.size/2:
                clicked_unit = unit
                break

        if clicked_unit:
            # Если кликнули по выделенному юниту - ничего не делаем
            return

        # 2. Проверяем, кликнули ли по другому юниту
        for unit in world.units:
            dx = unit.x - x
            dy = unit.y - y
            distance = (dx*dx + dy*dy)**0.5
            if distance < unit.size/2:
                # Нашли юнита, выделяем только его
                self.clear_selection()
                unit.selected = True
                self.selected_units.append(unit)
                return

        # 3. Проверяем, кликнули ли по ресурсу
        resource = world.get_resource_at_position(x, y, radius=30)
        if resource and self.selected_units:
            # Даем команду на сбор ресурсов ВСЕМ выделенным работягам
            self.command_gather(resource, world)
            return

        # 4. Клик по земле - движение ВСЕХ выделенных юнитов
        if self.selected_units:
            self.command_move(x, y, world)

    def command_move(self, x, y, world):
        """Команда движения всем выделенным юнитам"""
        for unit in self.selected_units:
            unit.set_move_target(x, y)

    def command_gather(self, resource, world):
        """Команда сбора ресурсов всем выделенным работягам"""
        if not world.headquarters:
            return

        for unit in self.selected_units:
            if unit.unit_type == 'worker':
                unit.set_gather_target(resource, world.headquarters)

    def command_stop(self):
        """Команда остановки всем выделенным юнитам"""
        for unit in self.selected_units:
            unit.set_move_target(unit.x, unit.y)  # Останавливаем на месте

    def command_return(self, world):
        """Команда возврата на базу всем выделенным работягам"""
        if not world.headquarters:
            return

        for unit in self.selected_units:
            if unit.unit_type == 'worker':
                unit.set_return_target(world.headquarters)

    def clear_selection(self):
        """Очистить выделение"""
        for unit in self.selected_units:
            unit.selected = False
        self.selected_units = []

    def get_selection_area(self):
        """Получить область выделения для отрисовки"""
        if not self.selecting or not self.selection_start or not self.selection_end:
            return None

        x1, y1 = self.selection_start
        x2, y2 = self.selection_end
        left = min(x1, x2)
        right = max(x1, x2)
        bottom = min(y1, y2)
        top = max(y1, y2)

        return {
            'pos': (left, bottom),
            'size': (right - left, top - bottom)
        }

    def get_selected_workers(self):
        """Получить выделенных работяг"""
        return [unit for unit in self.selected_units if unit.unit_type == 'worker']