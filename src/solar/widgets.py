from . import terminal as tl
from .interface import Module

DEFAULT_BGD = tl.bgd(80, 80, 80)
DEFAULT_BGD_HOVER = tl.bgd(128, 128, 128)
DEFAULT_BGD_ACTIVE = tl.bgd(255, 255, 255)

DEFAULT_FGD = tl.fgd(255, 255, 255)
DEFAULT_FGD_HOVER = tl.fgd(255, 255, 255)
DEFAULT_FGD_ACTIVE = tl.fgd(10, 10, 10)

# ----------------------------------------------------------------------------------------------------------------------
# Color Hint
class _ColorHint_:
    def __init__(self):
        self.color: str = ''
        self.color_hover: str = ''
        self.color_active: str = ''
        self.hover: bool = False
        self.active: bool = False

    def get_color(self):
        return self.color_active if self.active else self.color_hover if self.hover else self.color


# ----------------------------------------------------------------------------------------------------------------------
# Button
class _IButton_(Module):
    def __init__(self, text: str, x: int, y: int):
        self.text = text
        self.x = x
        self.y = y
        self.call = lambda: None
        self.fgd = _ColorHint_()
        self.bgd = _ColorHint_()
        self.fgd.color = DEFAULT_FGD
        self.fgd.color_hover = DEFAULT_FGD_HOVER
        self.fgd.color_active = DEFAULT_FGD_ACTIVE
        self.bgd.color = DEFAULT_BGD
        self.bgd.color_hover = DEFAULT_BGD_HOVER
        self.bgd.color_active = DEFAULT_BGD_ACTIVE
        self._pressed = False


class TextButton(_IButton_):
    def __init__(self, text: str, x: int = 0, y: int = 0):
        super().__init__(text, x, y)

    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + len(self.text) and self.y == y
    
    def mouse_move(self, x, y):
        bounds = self._check_bounds(x, y)
        self.bgd.hover = bounds
        self.fgd.hover = bounds

    def mouse_button(self, x, y, button):
        pressed = self._check_bounds(x, y) and button == 1
        self.bgd.active = pressed
        self.fgd.active = pressed

        if not pressed and self._pressed:
            self.call()
        self._pressed = pressed

    def update(self):
        bgd = self.bgd.get_color()
        fgd = self.fgd.get_color()
        print(f"{tl.move(self.x, self.y)}{bgd}{fgd}{self.text}", end="")


class RaisedButton(_IButton_):
    def __init__(self, text: str = "", x: int = 0, y: int = 0):
        super().__init__(text, x, y)
        self.bevel = _ColorHint_()
        self.bevel.color = tl.fgd(60, 60, 60)
        self.bevel.color_hover = tl.fgd(100, 100, 100)
        self.bevel.color_active = tl.fgd(240, 240, 240)


    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + len(self.text) +2 and self.y <= y < self.y +3

    def mouse_move(self, x, y):
        bounds = self._check_bounds(x, y)
        self.fgd.hover = bounds
        self.bgd.hover = bounds
        self.bevel.hover = bounds

    def mouse_button(self, x, y, button):
        pressed = self._check_bounds(x, y) and button == 1
        self.fgd.active = pressed
        self.bgd.active = pressed
        self.bevel.active = pressed
        if not pressed and self._pressed:
            self.call()
        self._pressed = pressed

    def update(self):
        bgd = self.bgd.get_color()
        fgd = self.fgd.get_color()
        bevel = self.bevel.get_color()

        width = len(self.text) +2
        height = int(self._pressed)
        draw  = tl.move(self.x, self.y) + tl.ANSI_RESET + (' ' * width)             # reset + clear spaces
        draw += tl.move(self.x, self.y + 3) + tl.ANSI_RESET + bevel + ('░' * width) # sides
        draw += tl.move(self.x, self.y +height) + bgd + bevel + ('▔' * width)       # upper bevel
        draw += tl.move(self.x, self.y + 2 +height) + ('▃' * width)                 # lower bevel
        draw += tl.move(self.x, self.y + 1 +height) + bgd + fgd + f" {self.text} "  # center
        print(draw, end="")




# ----------------------------------------------------------------------------------------------------------------------
# Lists
# class __IList__(Module):
#     def __init__(self, items: list):
#         self.items = items
#         self.padding: int = 0


# class ItemSelectList(__IList__):
#     def __init__(self, items: list = []):
#         super().__init__(items)
#         self.background = tl.ANSI_RESET
#         self.background_hover = tl.bgd(128, 128, 128)
#         self.background_active = tl.bgd(255, 255, 255)

#         self.foreground = tl.fgd(255, 255, 255)
#         self.foreground_acrive = tl.fgd(10, 10, 10)

#         self._bgd = self.background
#         self._fgd = self.foreground

    

    