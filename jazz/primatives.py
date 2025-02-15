from contextlib import contextmanager

import pygame
from pygame._sdl2 import Texture

from .global_dict import Globals
from .utils import Rect, Color, Vec2


class Draw:
    CIRCLE = [Vec2(1, 0).rotate(i * 10) for i in range(36)]

    @staticmethod
    @contextmanager
    def canvas(texture: Texture):
        Globals.renderer.target = texture
        try:
            yield None
        finally:
            Globals.renderer.target = None

    @staticmethod
    def line(p1: Vec2, p2: Vec2, color: Color, w: int = 1):
        if Globals.app.experimental:
            Globals.renderer.draw_color = color
            if w == 1:
                Globals.renderer.draw_line(p1, p2)
            else:
                for x in range(-w // 2, w // 2):
                    for y in range(-w // 2, w // 2):
                        if x**2 + y**2 <= (w // 2) ** 2:
                            Globals.renderer.draw_line(
                                p1 + Vec2(x, y), p2 + Vec2(x, y)
                            )
        else:
            pygame.draw.line(Globals.display, color, p1, p2, w)

    @staticmethod
    def lines(points: list[Vec2], color, w=1, closed=False):
        if Globals.app.experimental:
            for i in range(1, len(points)):
                Draw.line(points[i - 1], points[i], color, w)
            if closed:
                Draw.line(points[-1], points[0], color, w)
        else:
            pygame.draw.lines(Globals.display, color, closed, points, w)

    @staticmethod
    def rect(rect: Rect, color: Color, w=1):
        if Globals.app.experimental:
            Globals.renderer.draw_color = color
            if not isinstance(rect, Rect):
                rect = Rect(*rect)
            for i in range(w):
                Globals.renderer.draw_rect(rect.inflate(-2 * i, -2 * i))
        else:
            pygame.draw.rect(Globals.display, color, rect, w)

    @staticmethod
    def circle(center: Vec2, radius: int, color: Color, w: int = 1):
        if Globals.app.experimental:
            Draw.lines(
                [center + x * radius for x in Draw.CIRCLE], color, w, True
            )
        else:
            pygame.draw.circle(Globals.display, color, center, radius, w)

    @staticmethod
    def fill_rect(rect: Rect, color: Color):
        if Globals.app.experimental:
            Globals.renderer.draw_color = color
            if not isinstance(rect, Rect):
                rect = Rect(*rect)
            Globals.renderer.fill_rect(rect)
        else:
            pygame.draw.rect(Globals.display, color, rect)

    @staticmethod
    def fill_circle(center: Vec2, radius: int, color: Color):
        if Globals.app.experimental:
            Globals.renderer.draw_color = color
            for i in range(len(Draw.CIRCLE)):
                Globals.renderer.fill_triangle(
                    center,
                    center + Draw.CIRCLE[i] * radius,
                    center + Draw.CIRCLE[(i + 1) % len(Draw.CIRCLE)] * radius,
                )
        else:
            pygame.draw.circle(Globals.display, color, center, radius)
