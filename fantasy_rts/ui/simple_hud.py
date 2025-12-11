"""Чистый и минималистичный HUD"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
import random

class CleanHUD(FloatLayout):
    """Чистый минималистичный HUD без фона"""

    def __init__(self, world, selection_system, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.selection_system = selection_system

        print("=== СОЗДАНИЕ ЧИСТОГО HUD ===")

        # 1. Панель ресурсов вверху слева (полупрозрачная)
        self.create_resource_panel()

        # 2. Панель кнопок внизу
        self.create_button_panel()

        # 3. Информационная панель вверху справа
        self.create_info_panel()

        print("=== ЧИСТЫЙ HUD СОЗДАН ===")

    def create_resource_panel(self):
        """Создать панель ресурсов"""
        resource_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(300, 50),
            spacing=15,
            padding=[15, 10]
        )
        resource_panel.pos = (20, Window.height - 70)

        # Фон панели ресурсов (полупрозрачный темный)
        with resource_panel.canvas.before:
            Color(0.1, 0.1, 0.2, 0.8)  # Полупрозрачный темно-синий
            RoundedRectangle(
                pos=resource_panel.pos,
                size=resource_panel.size,
                radius=[10]
            )

        # Дерево
        wood_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_x=None, width=120)

        # Иконка дерева
        with wood_layout.canvas.before:
            Color(0.6, 0.4, 0.2, 1)  # Коричневый
            Rectangle(
                pos=(resource_panel.pos[0] + 15, resource_panel.pos[1] + 10),
                size=(30, 30)
            )

        self.wood_label = Label(
            text="200",
            font_size=20,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left'
        )
        self.wood_label.bind(size=self.wood_label.setter('text_size'))
        wood_layout.add_widget(Label(size_hint_x=None, width=40))  # Отступ для иконки
        wood_layout.add_widget(self.wood_label)

        # Золото
        gold_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_x=None, width=120)

        # Иконка золота
        with gold_layout.canvas.before:
            Color(1, 0.8, 0, 1)  # Золотой
            Rectangle(
                pos=(resource_panel.pos[0] + 165, resource_panel.pos[1] + 10),
                size=(30, 30)
            )

        self.gold_label = Label(
            text="200",
            font_size=20,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left'
        )
        self.gold_label.bind(size=self.gold_label.setter('text_size'))
        gold_layout.add_widget(Label(size_hint_x=None, width=40))  # Отступ для иконки
        gold_layout.add_widget(self.gold_label)

        resource_panel.add_widget(wood_layout)
        resource_panel.add_widget(gold_layout)
        self.add_widget(resource_panel)

        print("✓ Панель ресурсов создана")

    def create_button_panel(self):
        """Создать панель с кнопками"""
        button_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(0.8, None),
            height=70,
            spacing=20,
            padding=[20, 10]
        )
        button_panel.pos_hint = {'center_x': 0.5, 'y': 0.02}

        # Фон панели кнопок (полупрозрачный)
        with button_panel.canvas.before:
            Color(0.1, 0.1, 0.2, 0.8)  # Полупрозрачный темный
            RoundedRectangle(
                pos=button_panel.pos,
                size=button_panel.size,
                radius=[15]
            )
        button_panel.bind(pos=self.update_button_bg, size=self.update_button_bg)

        # Кнопки
        self.create_buttons(button_panel)

        self.add_widget(button_panel)
        print("✓ Панель кнопок создана")

    def update_button_bg(self, instance, value):
        """Обновить фон панели кнопок"""
        if instance.canvas.before:
            for instr in instance.canvas.before.get_group('roundedrect'):
                if isinstance(instr, RoundedRectangle):
                    instr.pos = instance.pos
                    instr.size = instance.size

    def create_buttons(self, panel):
        """Создать стилизованные кнопки"""
        # Кнопка "Новый работяга"
        train_btn = Button(
            text='🎯 Новый работяга',
            font_size=16,
            bold=True,
            background_color=(0.2, 0.8, 0.3, 1),  # Зеленый
            background_normal='',
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        # Скругленные углы для кнопки
        with train_btn.canvas.before:
            Color(0.2, 0.8, 0.3, 1)
            train_btn.rect = RoundedRectangle(
                pos=train_btn.pos,
                size=train_btn.size,
                radius=[8]
            )
        train_btn.bind(
            pos=lambda btn, pos: setattr(btn.rect, 'pos', pos),
            size=lambda btn, size: setattr(btn.rect, 'size', size)
        )
        train_btn.bind(on_press=self.train_worker)

        # Кнопка "Стоп"
        stop_btn = Button(
            text='⏹ Стоп',
            font_size=16,
            bold=True,
            background_color=(0.9, 0.2, 0.2, 1),  # Красный
            background_normal='',
            color=(1, 1, 1, 1),
            size_hint=(1, 1)
        )
        with stop_btn.canvas.before:
            Color(0.9, 0.2, 0.2, 1)
            stop_btn.rect = RoundedRectangle(
                pos=stop_btn.pos,
                size=stop_btn.size,
                radius=[8]
            )
        stop_btn.bind(
            pos=lambda btn, pos: setattr(btn.rect, 'pos', pos),
            size=lambda btn, size: setattr(btn.rect, 'size', size)
        )
        stop_btn.bind(on_press=self.stop_command)

        # Кнопка "Вернуть"
        return_btn = Button(
            text='🏠 Вернуть',
            font_size=16,
            bold=True,
            background_color=(1, 0.8, 0.2, 1),  # Желтый
            background_normal='',
            color=(0, 0, 0, 1),  # Черный текст для контраста
            size_hint=(1, 1)
        )
        with return_btn.canvas.before:
            Color(1, 0.8, 0.2, 1)
            return_btn.rect = RoundedRectangle(
                pos=return_btn.pos,
                size=return_btn.size,
                radius=[8]
            )
        return_btn.bind(
            pos=lambda btn, pos: setattr(btn.rect, 'pos', pos),
            size=lambda btn, size: setattr(btn.rect, 'size', size)
        )
        return_btn.bind(on_press=self.return_command)

        panel.add_widget(train_btn)
        panel.add_widget(stop_btn)
        panel.add_widget(return_btn)

        print("✓ Кнопки созданы")

    def create_info_panel(self):
        """Создать информационную панель"""
        info_panel = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(250, 80),
            spacing=5,
            padding=[15, 10]
        )
        info_panel.pos = (Window.width - 270, Window.height - 90)

        # Фон информационной панели
        with info_panel.canvas.before:
            Color(0.1, 0.1, 0.2, 0.8)
            RoundedRectangle(
                pos=info_panel.pos,
                size=info_panel.size,
                radius=[10]
            )

        self.info_label = Label(
            text="Выберите юнитов",
            font_size=16,
            color=(1, 1, 1, 1),
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

        info_panel.add_widget(self.info_label)
        info_panel.add_widget(self.selection_label)
        self.add_widget(info_panel)

        print("✓ Информационная панель создана")

    def update(self):
        """Обновить HUD"""
        # Ресурсы
        if self.world.headquarters:
            wood = self.world.headquarters.resources.get('wood', 0)
            gold = self.world.headquarters.resources.get('gold', 0)
            self.wood_label.text = str(int(wood))
            self.gold_label.text = str(int(gold))

        # Информация о выделении
        selected_count = len(self.selection_system.selected_units)
        self.selection_label.text = f"Выделено: {selected_count}"

        # Типы выделенных юнитов
        if selected_count == 0:
            self.info_label.text = "Выберите юнитов"
        else:
            workers = len([u for u in self.selection_system.selected_units if u.unit_type == 'worker'])
            infantry = len([u for u in self.selection_system.selected_units if u.unit_type == 'infantry'])
            archers = len([u for u in self.selection_system.selected_units if u.unit_type == 'archer'])

            types = []
            if workers > 0:
                types.append(f"Работяги: {workers}")
            if infantry > 0:
                types.append(f"Пехота: {infantry}")
            if archers > 0:
                types.append(f"Лучники: {archers}")

            self.info_label.text = " | ".join(types) if types else "Смешанный отряд"

    def train_worker(self, instance):
        """Обучить нового работягу"""
        print("🎯 Нажата кнопка 'Новый работяга'")
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
        """Команда остановки"""
        print("⏹ Нажата кнопка 'Стоп'")
        self.selection_system.command_stop()

    def return_command(self, instance):
        """Команда возврата"""
        print("🏠 Нажата кнопка 'Вернуть'")
        workers = self.selection_system.get_selected_workers()
        if workers:
            self.selection_system.command_return(self.world)
            print(f"🏠 {len(workers)} работяг возвращаются на базу")