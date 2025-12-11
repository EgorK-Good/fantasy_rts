"""Стилизованные кнопки для игры"""
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty
from core.constants import UI_COLORS, BUTTON_STYLE


class GameButton(Button):
    """Стилизованная кнопка для игры"""

    background_color = ListProperty(UI_COLORS['BUTTON_NORMAL'])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Настройки шрифта
        self.font_size = BUTTON_STYLE['font_size']
        self.bold = BUTTON_STYLE['bold']
        self.color = UI_COLORS['TEXT']
        self.padding = BUTTON_STYLE['padding']

        # Создаем скругленные углы
        with self.canvas.before:
            Color(*self.background_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[BUTTON_STYLE['border_radius']]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """Обновить позицию и размер прямоугольника"""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_press(self):
        """При нажатии"""
        self.background_color = UI_COLORS['BUTTON_PRESSED']

    def on_release(self):
        """При отпускании"""
        self.background_color = UI_COLORS['BUTTON_NORMAL']