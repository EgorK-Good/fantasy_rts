"""Вспомогательные функции"""
import math

def distance(x1, y1, x2, y2):
    """Расстояние между двумя точками"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def point_in_rect(x, y, rect_x, rect_y, width, height):
    """Проверка, находится ли точка в прямоугольнике"""
    return (rect_x <= x <= rect_x + width and
            rect_y <= y <= rect_y + height)

def lerp(a, b, t):
    """Линейная интерполяция"""
    return a + (b - a) * t

def clamp(value, min_val, max_val):
    """Ограничение значения"""
    return max(min_val, min(value, max_val))