"""HUD интерфейс - всегда поверх игры"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.text import Label as CoreLabel
from core.constants import UI_COLORS, BUTTON_STYLE
from ui.buttons import GameButton
import random

class ResourceDisplay(BoxLayout):
    """Отображение ресурсов"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (None, None)
        self.size = (300, 50)
        self.spacing = 15
        self.padding = [15, 10]

        # Фон с закругленными углами
        with self.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Дерево
        wood_box = BoxLayout(orientation='horizontal', spacing=8)

        # Иконка дерева
        with wood_box.canvas.before:
            Color(*UI_COLORS['RESOURCE_WOOD'])
            Rectangle(
                pos=(0, 0),
                size=(30, 30)
            )
        wood_box.add_widget(Widget(size=(30, 30)))

        # Текст
        self.wood_label = Label(
            text="200",
            font_size=22,
            bold=True,
            color=UI_COLORS['TEXT'],
            size_hint=(None, None),
            size=(80, 30)
        )
        wood_box.add_widget(self.wood_label)

        # Золото
        gold_box = BoxLayout(orientation='horizontal', spacing=8)

        # Иконка золота
        with gold_box.canvas.before:
            Color(*UI_COLORS['RESOURCE_GOLD'])
            Rectangle(
                pos=(0, 0),
                size=(30, 30)
            )
        gold_box.add_widget(Widget(size=(30, 30)))

        # Текст
        self.gold_label = Label(
            text="200",
            font_size=22,
            bold=True,
            color=UI_COLORS['TEXT'],
            size_hint=(None, None),
            size=(80, 30)
        )
        gold_box.add_widget(self.gold_label)

        self.add_widget(wood_box)
        self.add_widget(gold_box)

    def update_rect(self, *args):
        """Обновить фон"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_values(self, wood, gold):
        """Обновить значения ресурсов"""
        self.wood_label.text = str(int(wood))
        self.gold_label.text = str(int(gold))

class HUD(FloatLayout):
    """Главный HUD интерфейс - всегда поверх игры"""

    def __init__(self, world, selection_system, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.selection_system = selection_system

        # ВАЖНО: Отключаем обработку касаний для HUD, чтобы они проходили к игре
        # КНОЧКИ сами обработают свои касания
        self.disabled = False

        # Прозрачный фон (можно сделать полупрозрачный для отладки)
        with self.canvas.before:
            Color(0, 0, 0, 0)  # Полностью прозрачный
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)

        # Создаем HUD элементы
        self.create_hud_elements()

    def update_bg(self, *args):
        """Обновить фон"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def create_hud_elements(self):
        """Создать элементы HUD"""
        # 1. Панель ресурсов вверху слева
        self.resource_display = ResourceDisplay()
        self.resource_display.pos_hint = {'x': 0.02, 'y': 0.92}
        self.add_widget(self.resource_display)

        # 2. Панель управления внизу по центру
        control_panel = GridLayout(
            cols=3,
            rows=1,
            size_hint=(0.6, None),
            height=70,
            spacing=15,
            padding=[20, 10]
        )
        control_panel.pos_hint = {'center_x': 0.5, 'y': 0.02}

        # Фон панели управления
        with control_panel.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            self.control_bg = Rectangle(pos=control_panel.pos, size=control_panel.size)
        control_panel.bind(pos=self.update_control_bg, size=self.update_control_bg)

        # Создаем кнопки
        self.create_buttons(control_panel)

        self.add_widget(control_panel)

        # 3. Информационная панель вверху справа
        self.info_panel = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(250, 60),
            spacing=5,
            padding=[10, 5]
        )
        self.info_panel.pos_hint = {'right': 0.98, 'y': 0.92}

        with self.info_panel.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            self.info_bg = Rectangle(pos=self.info_panel.pos, size=self.info_panel.size)
        self.info_panel.bind(pos=self.update_info_bg, size=self.update_info_bg)

        self.info_label = Label(
            text="Выберите юнитов",
            font_size=16,
            color=UI_COLORS['TEXT'],
            halign='left',
            valign='middle'
        )
        self.info_label.bind(size=self.info_label.setter('text_size'))

        self.selection_label = Label(
            text="Выделено: 0",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            halign='left',
            valign='middle'
        )
        self.selection_label.bind(size=self.selection_label.setter('text_size'))

        self.info_panel.add_widget(self.info_label)
        self.info_panel.add_widget(self.selection_label)
        self.add_widget(self.info_panel)

    def update_control_bg(self, *args):
        """Обновить фон панели управления"""
        if hasattr(self, 'control_bg'):
            for child in self.children:
                if isinstance(child, GridLayout) and child.cols == 3:
                    self.control_bg.pos = child.pos
                    self.control_bg.size = child.size
                    break

    def update_info_bg(self, *args):
        """Обновить фон информационной панели"""
        self.info_bg.pos = self.info_panel.pos
        self.info_bg.size = self.info_panel.size

    def create_buttons(self, panel):
        """Создать кнопки управления"""
        # Кнопка "Новый работяга"
        train_btn = GameButton(
            text='[size=16][b]🎯 Новый работяга[/b][/size]',
            markup=True,
            background_color=UI_COLORS['BUTTON_GREEN'],
            size_hint=(1, 1)
        )
        train_btn.bind(on_press=self.train_worker)

        # Кнопка "Стоп"
        stop_btn = GameButton(
            text='[size=16][b]⏹ Стоп[/b][/size]',
            markup=True,
            background_color=UI_COLORS['BUTTON_RED'],
            size_hint=(1, 1)
        )
        stop_btn.bind(on_press=self.stop_command)

        # Кнопка "Вернуть"
        return_btn = GameButton(
            text='[size=16][b]🏠 Вернуть[/b][/size]',
            markup=True,
            background_color=UI_COLORS['BUTTON_YELLOW'],
            size_hint=(1, 1)
        )
        return_btn.bind(on_press=self.return_command)

        panel.add_widget(train_btn)
        panel.add_widget(stop_btn)
        panel.add_widget(return_btn)

    def update(self):
        """Обновить HUD"""
        if self.world.headquarters:
            wood = self.world.headquarters.resources.get('wood', 0)
            gold = self.world.headquarters.resources.get('gold', 0)
            self.resource_display.update_values(wood, gold)

        # Обновить информацию о выделении
        selected_count = len(self.selection_system.selected_units)
        self.selection_label.text = f"Выделено: {selected_count}"

        # Обновить информацию в зависимости от выделения
        if selected_count == 0:
            self.info_label.text = "Выберите юнитов"
        else:
            workers = len([u for u in self.selection_system.selected_units if u.unit_type == 'worker'])
            infantry = len([u for u in self.selection_system.selected_units if u.unit_type == 'infantry'])
            archers = len([u for u in self.selection_system.selected_units if u.unit_type == 'archer'])

            info_parts = []
            if workers > 0:
                info_parts.append(f"Работяги: {workers}")
            if infantry > 0:
                info_parts.append(f"Пехота: {infantry}")
            if archers > 0:
                info_parts.append(f"Лучники: {archers}")

            self.info_label.text = " | ".join(info_parts) if info_parts else "Смешанный отряд"

    def train_worker(self, instance):
        """Обучить нового работягу"""
        if self.world.headquarters and self.world.headquarters.can_train_unit('worker'):
            if self.world.headquarters.train_unit('worker'):
                from entities.unit import Unit

                new_worker = Unit(
                    x=self.world.headquarters.x + random.randint(-30, 30),
                    y=self.world.headquarters.y + random.randint(-30, 30),
                    unit_type="worker"
                )
                self.world.add_unit(new_worker)
                print("✓ Новый работяга обучен!")

    def stop_command(self, instance):
        """Команда остановки выделенным юнитам"""
        self.selection_system.command_stop()
        print("⏹ Команда 'Стоп' выполнена")

    def return_command(self, instance):
        """Команда возврата на базу выделенным работягам"""
        workers = self.selection_system.get_selected_workers()
        if workers:
            self.selection_system.command_return(self.world)
            print(f"🏠 {len(workers)} работяг возвращаются на базу")