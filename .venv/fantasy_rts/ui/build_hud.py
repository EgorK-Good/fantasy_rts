"""HUD с кнопками строительства и найма"""
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from core.constants import UI_COLORS, UNIT_STATS, BUILDING_STATS
import random

class BuildHUD(FloatLayout):
    """HUD с расширенными возможностями"""

    def __init__(self, world, selection_system, building_system, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.selection_system = selection_system
        self.building_system = building_system
        self.build_mode = None

        print("=== СОЗДАНИЕ РАСШИРЕННОГО HUD ===")

        # 1. Панель ресурсов
        self.create_resource_panel()

        # 2. Основная панель управления
        self.create_main_panel()

        # 3. Панель строительства (появляется при выборе работяг)
        self.build_panel = None

        # 4. Панель найма войск (появляется при выборе казармы)
        self.recruit_panel = None

        # 5. Информационная панель
        self.create_info_panel()

        print("=== РАСШИРЕННЫЙ HUD СОЗДАН ===")

    def create_resource_panel(self):
        """Создать панель ресурсов и населения"""
        resource_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            size=(350, 60),
            spacing=15,
            padding=[15, 10]
        )
        resource_panel.pos = (20, Window.height - 80)

        # Фон
        with resource_panel.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            RoundedRectangle(
                pos=resource_panel.pos,
                size=resource_panel.size,
                radius=[10]
            )

        # Население
        pop_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_x=None, width=100)
        self.pop_label = Label(
            text="10/10",
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left'
        )
        self.pop_label.bind(size=self.pop_label.setter('text_size'))
        pop_layout.add_widget(Label(text="👥", font_size=20, size_hint_x=None, width=30))
        pop_layout.add_widget(self.pop_label)

        # Дерево
        wood_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_x=None, width=100)
        self.wood_label = Label(
            text="200",
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left'
        )
        self.wood_label.bind(size=self.wood_label.setter('text_size'))
        wood_layout.add_widget(Label(text="🌳", font_size=20, size_hint_x=None, width=30))
        wood_layout.add_widget(self.wood_label)

        # Золото
        gold_layout = BoxLayout(orientation='horizontal', spacing=8, size_hint_x=None, width=100)
        self.gold_label = Label(
            text="200",
            font_size=18,
            bold=True,
            color=(1, 1, 1, 1),
            halign='left'
        )
        self.gold_label.bind(size=self.gold_label.setter('text_size'))
        gold_layout.add_widget(Label(text="💰", font_size=20, size_hint_x=None, width=30))
        gold_layout.add_widget(self.gold_label)

        resource_panel.add_widget(pop_layout)
        resource_panel.add_widget(wood_layout)
        resource_panel.add_widget(gold_layout)
        self.add_widget(resource_panel)

    def create_main_panel(self):
        """Создать основную панель управления"""
        main_panel = BoxLayout(
            orientation='horizontal',
            size_hint=(0.9, None),
            height=80,
            spacing=15,
            padding=[20, 10]
        )
        main_panel.pos_hint = {'center_x': 0.5, 'y': 0.02}

        # Фон
        with main_panel.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            RoundedRectangle(
                pos=main_panel.pos,
                size=main_panel.size,
                radius=[15]
            )
        main_panel.bind(pos=self.update_panel_bg, size=self.update_panel_bg)

        # Основные кнопки
        buttons = [
            ("🏗️ Строить", self.enter_build_mode, UI_COLORS['BUTTON_BLUE']),
            ("🎯 Работяга", self.train_worker, UI_COLORS['BUTTON_GREEN']),
            ("⏹ Стоп", self.stop_command, UI_COLORS['BUTTON_RED']),
            ("🏠 Вернуть", self.return_command, UI_COLORS['BUTTON_YELLOW']),
        ]

        for text, callback, color in buttons:
            btn = self.create_styled_button(text, color)
            btn.bind(on_press=callback)
            main_panel.add_widget(btn)

        self.add_widget(main_panel)
        self.main_panel = main_panel

    def update_panel_bg(self, instance, value):
        """Обновить фон панели"""
        if instance.canvas.before:
            for instr in instance.canvas.before.get_group('roundedrect'):
                if isinstance(instr, RoundedRectangle):
                    instr.pos = instance.pos
                    instr.size = instance.size

    def create_styled_button(self, text, color):
        """Создать стилизованную кнопку"""
        btn = Button(
            text=text,
            font_size=16,
            bold=True,
            background_color=color,
            background_normal='',
            color=(1, 1, 1, 1) if color[0] + color[1] + color[2] < 1.5 else (0, 0, 0, 1),
            size_hint=(1, 1)
        )

        # Скругленные углы
        with btn.canvas.before:
            Color(*color)
            btn.rect = RoundedRectangle(
                pos=btn.pos,
                size=btn.size,
                radius=[8]
            )

        btn.bind(
            pos=lambda b, pos: setattr(b.rect, 'pos', pos),
            size=lambda b, size: setattr(b.rect, 'size', size)
        )

        return btn

    def create_info_panel(self):
        """Создать информационную панель"""
        info_panel = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 100),
            spacing=5,
            padding=[15, 10]
        )
        info_panel.pos = (Window.width - 320, Window.height - 110)

        # Фон
        with info_panel.canvas.before:
            Color(*UI_COLORS['PANEL_BG'])
            RoundedRectangle(
                pos=info_panel.pos,
                size=info_panel.size,
                radius=[10]
            )

        self.mode_label = Label(
            text="Режим: Обычный",
            font_size=16,
            color=UI_COLORS['TEXT'],
            halign='left'
        )
        self.mode_label.bind(size=self.mode_label.setter('text_size'))

        self.selection_label = Label(
            text="Выделено: 0",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            halign='left'
        )
        self.selection_label.bind(size=self.selection_label.setter('text_size'))

        self.info_label = Label(
            text="Выберите объект",
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            halign='left'
        )
        self.info_label.bind(size=self.info_label.setter('text_size'))

        info_panel.add_widget(self.mode_label)
        info_panel.add_widget(self.selection_label)
        info_panel.add_widget(self.info_label)
        self.add_widget(info_panel)

    def show_build_panel(self):
        """Показать панель строительства"""
        if self.build_panel:
            self.remove_widget(self.build_panel)

        self.build_panel = GridLayout(
            cols=3,
            rows=1,
            size_hint=(None, None),
            size=(450, 70),
            spacing=10,
            padding=[10, 5]
        )
        self.build_panel.pos = (Window.width//2 - 225, 100)

        # Фон
        with self.build_panel.canvas.before:
            Color(0.1, 0.2, 0.3, 0.9)
            RoundedRectangle(
                pos=self.build_panel.pos,
                size=self.build_panel.size,
                radius=[10]
            )

        # Кнопка "Ферма"
        farm_btn = self.create_styled_button("🌾 Ферма\n150🌳 50💰", (0.3, 0.7, 0.3, 1))
        farm_btn.bind(on_press=lambda x: self.start_building('farm'))

        # Кнопка "Казармы"
        barracks_btn = self.create_styled_button("⚔️ Казармы\n200🌳 100💰", (0.3, 0.3, 0.7, 1))
        barracks_btn.bind(on_press=lambda x: self.start_building('barracks'))

        # Кнопка "Отмена"
        cancel_btn = self.create_styled_button("❌ Отмена", (0.7, 0.2, 0.2, 1))
        cancel_btn.bind(on_press=self.cancel_build_mode)

        self.build_panel.add_widget(farm_btn)
        self.build_panel.add_widget(barracks_btn)
        self.build_panel.add_widget(cancel_btn)

        self.add_widget(self.build_panel)

    def show_recruit_panel(self):
        """Показать панель найма войск"""
        if self.recruit_panel:
            self.remove_widget(self.recruit_panel)

        self.recruit_panel = GridLayout(
            cols=4,
            rows=1,
            size_hint=(None, None),
            size=(600, 70),
            spacing=10,
            padding=[10, 5]
        )
        self.recruit_panel.pos = (Window.width//2 - 300, 100)

        # Фон
        with self.recruit_panel.canvas.before:
            Color(0.2, 0.1, 0.3, 0.9)
            RoundedRectangle(
                pos=self.recruit_panel.pos,
                size=self.recruit_panel.size,
                radius=[10]
            )

        # Кнопки найма
        buttons = [
            ("🛡️ Пехотинец\n100🌳 50💰", 'infantry', (0.3, 0.3, 0.8, 1)),
            ("🏹 Лучник\n80🌳 100💰", 'archer', (0.8, 0.5, 0.2, 1)),
            ("👑 Командир\n200🌳 200💰", 'commander', (0.9, 0.1, 0.1, 1)),
        ]

        for text, unit_type, color in buttons:
            btn = self.create_styled_button(text, color)
            btn.bind(on_press=lambda x, ut=unit_type: self.recruit_unit(ut))
            self.recruit_panel.add_widget(btn)

        # Кнопка "Закрыть"
        close_btn = self.create_styled_button("❌ Закрыть", (0.7, 0.2, 0.2, 1))
        close_btn.bind(on_press=self.close_recruit_panel)
        self.recruit_panel.add_widget(close_btn)

        self.add_widget(self.recruit_panel)

    def enter_build_mode(self, instance):
        """Войти в режим строительства"""
        print("🏗️ Вход в режим строительства")
        self.build_mode = 'building'
        self.show_build_panel()
        self.mode_label.text = "Режим: Строительство"
        self.info_label.text = "Выберите тип здания"

    def start_building(self, building_type):
        """Начать строительство здания"""
        print(f"🏗️ Начато строительство: {building_type}")

        # Проверяем, есть ли выделенные работяги
        selected_workers = self.selection_system.get_selected_workers()
        if not selected_workers:
            self.info_label.text = "Выберите работяг для строительства!"
            print("✗ Нет выделенных работяг")
            return

        # Проверяем, хватает ли ресурсов
        if not self.building_system.can_afford_building(building_type):
            self.info_label.text = "Недостаточно ресурсов!"
            print(f"✗ Недостаточно ресурсов для {building_type}")
            return

        # Входим в режим строительства
        if self.building_system.start_building_mode(building_type):
            # Выбираем первого работяга как строителя
            self.building_system.select_builder(selected_workers[0])

            # Убираем панель строительства
            if self.build_panel:
                self.remove_widget(self.build_panel)
                self.build_panel = None

            self.mode_label.text = f"Режим: Строительство {building_type}"
            self.info_label.text = "Кликните на карте, чтобы разместить здание"
            print(f"✓ Режим строительства {building_type} активирован")
        else:
            self.info_label.text = "Ошибка входа в режим строительства"
            print(f"✗ Не удалось войти в режим строительства {building_type}")

    def cancel_build_mode(self, instance):
        """Отменить режим строительства"""
        print("❌ Отмена режима строительства")
        self.building_system.exit_building_mode()

        if self.build_panel:
            self.remove_widget(self.build_panel)
            self.build_panel = None

        self.build_mode = None
        self.mode_label.text = "Режим: Обычный"
        self.info_label.text = "Строительство отменено"

    def recruit_unit(self, unit_type):
        """Нанять юнита"""
        print(f"🎖️ Наем юнита: {unit_type}")

        # Ищем выбранную казарму
        selected_barracks = None
        for building in self.world.buildings:
            if (hasattr(building, 'building_type') and
                building.building_type == 'barracks' and
                hasattr(building, 'build_state') and
                building.build_state == 'complete' and
                building.selected):
                selected_barracks = building
                break

        if not selected_barracks:
            self.info_label.text = "Выберите казарму!"
            print("✗ Не выбрана казарма")
            return

        # Проверяем лимит населения
        if not self.world.can_train_unit(unit_type):
            self.info_label.text = "Достигнут лимит населения!"
            print(f"✗ Достигнут лимит населения для {unit_type}")
            return

        # Проверяем ресурсы
        if unit_type not in UNIT_STATS:
            self.info_label.text = "Неизвестный тип юнита!"
            print(f"✗ Неизвестный тип юнита: {unit_type}")
            return

        cost = UNIT_STATS[unit_type]['cost']
        if (self.world.headquarters and
            (self.world.headquarters.resources.get('wood', 0) < cost.get('wood', 0) or
             self.world.headquarters.resources.get('gold', 0) < cost.get('gold', 0))):
            self.info_label.text = "Недостаточно ресурсов!"
            print(f"✗ Недостаточно ресурсов для {unit_type}")
            return

        # Пытаемся нанять юнита
        if hasattr(selected_barracks, 'train_unit'):
            if selected_barracks.train_unit(unit_type, self.world):
                # Оплачиваем
                if self.world.headquarters:
                    self.world.headquarters.resources['wood'] -= cost.get('wood', 0)
                    self.world.headquarters.resources['gold'] -= cost.get('gold', 0)

                self.info_label.text = f"{unit_type} в очереди на обучение"
                print(f"✓ {unit_type} добавлен в очередь обучения")
            else:
                self.info_label.text = "Не удалось нанять юнита"
                print(f"✗ Не удалось нанять {unit_type}")
        else:
            self.info_label.text = "Это здание не может обучать!"
            print(f"✗ Здание не может обучать юнитов")

    def close_recruit_panel(self, instance):
        """Закрыть панель найма"""
        print("❌ Закрытие панели найма")
        if self.recruit_panel:
            self.remove_widget(self.recruit_panel)
            self.recruit_panel = None
        self.mode_label.text = "Режим: Обычный"

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
                self.info_label.text = "Новый работяга обучен!"
                print("✓ Новый работяга обучен!")
            else:
                self.info_label.text = "Недостаточно ресурсов!"
                print("✗ Недостаточно ресурсов для работяги")
        else:
            self.info_label.text = "Нельзя обучить работягу!"
            print("✗ Нельзя обучить работягу")

    def stop_command(self, instance):
        """Команда остановки"""
        print("⏹ Нажата кнопка 'Стоп'")
        self.selection_system.command_stop()
        self.info_label.text = "Команда 'Стоп' выполнена"

    def return_command(self, instance):
        """Команда возврата"""
        print("🏠 Нажата кнопка 'Вернуть'")
        workers = self.selection_system.get_selected_workers()
        if workers:
            self.selection_system.command_return(self.world)
            self.info_label.text = f"{len(workers)} работяг возвращаются"
            print(f"🏠 {len(workers)} работяг возвращаются на базу")
        else:
            self.info_label.text = "Нет выделенных работяг"
            print("✗ Нет выделенных работяг для возврата")

    def update(self):
        """Обновить HUD"""
        # Обновляем ресурсы
        if self.world.headquarters:
            wood = self.world.headquarters.resources.get('wood', 0)
            gold = self.world.headquarters.resources.get('gold', 0)
            self.wood_label.text = str(int(wood))
            self.gold_label.text = str(int(gold))

            # Обновляем население
            if hasattr(self.world, 'get_current_population') and hasattr(self.world, 'get_max_population'):
                current_pop = self.world.get_current_population()
                max_pop = self.world.get_max_population()
                self.pop_label.text = f"{current_pop}/{max_pop}"

                # Подсвечиваем лимит населения
                if current_pop >= max_pop:
                    self.pop_label.color = (1, 0.2, 0.2, 1)  # Красный
                elif current_pop >= max_pop * 0.8:
                    self.pop_label.color = (1, 1, 0.2, 1)   # Желтый
                else:
                    self.pop_label.color = UI_COLORS['TEXT']  # Белый

        # Обновляем информацию о выделении
        selected_count = len(self.selection_system.selected_units)
        self.selection_label.text = f"Выделено: {selected_count}"

        # Определяем тип выделенного объекта
        if selected_count == 0:
            # Проверяем, выделено ли здание
            building_selected = False
            for building in self.world.buildings:
                if hasattr(building, 'selected') and building.selected:
                    building_selected = True

                    # Если выделена казарма
                    if hasattr(building, 'building_type') and building.building_type == 'barracks':
                        # Показываем панель найма, если еще не показана
                        if not self.recruit_panel:
                            self.show_recruit_panel()
                            self.mode_label.text = "Режим: Набор войск"

                        # Обновляем информацию о тренировке
                        if hasattr(building, 'current_training') and building.current_training:
                            if hasattr(building, 'get_training_percentage'):
                                training_percent = building.get_training_percentage() * 100
                                self.info_label.text = f"Обучается: {building.current_training} ({training_percent:.0f}%)"
                            else:
                                self.info_label.text = f"Обучается: {building.current_training}"
                        elif hasattr(building, 'training_queue') and building.training_queue:
                            self.info_label.text = f"В очереди: {len(building.training_queue)} юнитов"
                        else:
                            self.info_label.text = "Казарма свободна"
                        break
                    else:
                        self.info_label.text = f"Выбрано: {getattr(building, 'description', 'Здание')}"

            if not building_selected:
                self.info_label.text = "Выберите объект"

        else:
            # Убираем панель найма, если есть выделенные юниты
            if self.recruit_panel:
                self.remove_widget(self.recruit_panel)
                self.recruit_panel = None
                self.mode_label.text = "Режим: Обычный"

            # Информация о выделенных юнитах
            workers = len([u for u in self.selection_system.selected_units if hasattr(u, 'unit_type') and u.unit_type == 'worker'])
            infantry = len([u for u in self.selection_system.selected_units if hasattr(u, 'unit_type') and u.unit_type == 'infantry'])
            archers = len([u for u in self.selection_system.selected_units if hasattr(u, 'unit_type') and u.unit_type == 'archer'])
            commanders = len([u for u in self.selection_system.selected_units if hasattr(u, 'unit_type') and u.unit_type == 'commander'])

            types = []
            if workers > 0:
                types.append(f"Работяги: {workers}")
            if infantry > 0:
                types.append(f"Пехота: {infantry}")
            if archers > 0:
                types.append(f"Лучники: {archers}")
            if commanders > 0:
                types.append(f"Командиры: {commanders}")

            self.info_label.text = " | ".join(types) if types else "Смешанный отряд"

        # Обновляем режим строительства
        if (hasattr(self.building_system, 'building_mode') and
            self.building_system.building_mode and
            not self.build_panel and
            hasattr(self.building_system, 'selected_builder') and
            not self.building_system.selected_builder):
            # Если строитель умер или пропал
            self.building_system.exit_building_mode()
            self.mode_label.text = "Режим: Обычный"
            self.info_label.text = "Строитель не найден"