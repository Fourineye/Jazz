from typing import Iterable
from . import Surface, Vec2
from .global_dict import Globals
from .components import Label, Sprite
from .user_interface import DEFAULT_FONT
from .utils import Rect, Color


class TextBox(Sprite):
    def __init__(self, name="TextBox", **kwargs):
        font = kwargs.get("font", DEFAULT_FONT)
        text_color = kwargs.get("text_color", (255, 255, 255))
        text = kwargs.get("text", "")
        if not kwargs.get("asset", False):
            size = kwargs.get("size", Vec2(font.size(text)) + (10, 10))
            box = Surface(size)
            box.fill(kwargs.get("bg_color", (32, 32, 32)))
            kwargs.setdefault("asset", box)
        super().__init__(name, **kwargs)
        self._text = Label(
            font=font,
            text_color=text_color,
            text=text,
            pos=(self._draw_offset[0] + 5, self._draw_offset[1] + self.source.get_height() / 2),
            anchor=(0, 1)
        )
        self.add_child(self._text)

        self._cursor = Label(
            font=font,
            text_color=text_color,
            text="|",
            anchor=(0, 1),
            pos=(self._draw_offset[0] + self.source.get_width(), self._draw_offset[1] + self.source.get_height() / 2),
            visible=False
        )
        self.add_child(self._cursor)

        self._blink_rate: float = kwargs.get("blink_rate", 0.25)
        self._blink: float = 0.0
        self._active: bool = False

    def update(self, delta: float):
        if self._active:
            self._blink += delta
            if self._blink >= self._blink_rate:
                self._blink -= self._blink_rate
                self._cursor.visible = not self._cursor.visible

            if Globals.input.text:
                self.set_text(self._text.text_content + Globals.input.text)
            elif Globals.key.press("backspace"):
                self.set_text(self._text.text_content[:-1])
            elif not self.rect.collidepoint(Globals.mouse.pos):
                if Globals.mouse.click(0):
                    self._cursor.visible = False
                    self._active = False
            elif Globals.key.press("enter"):
                self._active = False
                self._cursor.visible = False
        else:
            if self.rect.collidepoint(Globals.mouse.pos):
                if Globals.mouse.click(0):
                    self._active = True

    def set_text(self, text):
        self._text.set_text(text)
        self._cursor.local_pos = (
            self._text._draw_offset[0] + self._text.source.get_width(),
            self._text._draw_offset[1] + self._text.source.get_height() / 2
        )


# class CheckBox(Sprite):
#     def __init__(self, name="CheckBox", **kwargs):
#         source = Surface((16, 16))
#         source.fill((10, 10, 25))
#         pygame.draw.circle(source, (20, 20, 40), (7, 7), 8)
#         pygame.draw.rect(source, (128, 128, 128), (0, 0, 16, 16), 1)
#         super().__init__(name, asset=source, **kwargs)
#         self._checkmark = jazz.Surface((24, 16))
#         pygame.draw.lines(
#             self._checkmark, (64, 128, 64), False, ((0, 8), (8, 16), (16, 0))
#         )
#         self.checked = False
#
#     def update(self, delta):
#         if self.rect.collidepoint(Globals.mouse.pos):
#             if Globals.mouse.click(0):
#                 self.checked = not self.checked

    # def draw(self, surface, offset=None):
    #     ...

class Primatives:
    @staticmethod
    def rect(rect: Rect, color: Color, w=1):
        Globals.renderer.draw_color = color
        if not isinstance(rect, Rect):
            rect = Rect(*rect)
        for i in range(w):
            Globals.renderer.draw_rect(rect.inflate(-2 * i, -2 * i))

    @staticmethod
    def line(p1: Vec2, p2: Vec2, color:Color, w: int=1):
        Globals.renderer.draw_color = color
        if w == 1:
            Globals.renderer.draw_line(p1, p2)
        else:
            for x in range(-w // 2, w //2):
                for y in range(-w // 2, w //2):
                    if x ** 2 + y ** 2 <= (w // 2) ** 2:
                        Globals.renderer.draw_line(p1 + Vec2(x,y), p2 + Vec2(x, y))

    @staticmethod
    def lines(points: I
              
              terable[Vec2], )





              
