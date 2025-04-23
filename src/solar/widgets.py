from . import terminal as tl
from .interface import Module

class __IButton__(Module):
    def __init__(self, text: str, x: int, y: int):
        self.text = text
        self.x = x
        self.y = y
        self.call = lambda: None
        self.foreground = tl.fgd(255, 255, 255)
        self.foreground_active = tl.fgd(10, 10, 10)
        self.background = tl.bgd(80, 80, 80)
        self.background_active = tl.bgd(255, 255, 255)
        self.background_hover = tl.bgd(128, 128, 128)

        self._fgd = self.foreground
        self._bgd = self.background
        self._pressed = False


class TextButton(__IButton__):
    def __init__(self, text: str, x: int = 0, y: int = 0):
        super().__init__(text, x, y)

    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + len(self.text) and self.y == y
    
    def mouse_move(self, x, y):
        self._bgd = self.background_hover if self._check_bounds(x, y) else self.background

    def mouse_button(self, x, y, button):
        bounds = self._check_bounds(x, y)
        if bounds and button == 1:
            self._bgd = self.background_active
            self._fgd = self.foreground_active
            self._pressed = True
        else:
            self._fgd = self.foreground
            self._bgd = self.background_hover if bounds else self.background
            if self._pressed:
                self.call()
            self._pressed = False

    def update(self):
        print(f"{tl.move(self.x, self.y)}{self._bgd}{self._fgd}{self.text}", end="")


class RaisedButton(__IButton__):
    def __init__(self, text: str = "", x: int = 0, y: int = 0):
        super().__init__(text, x, y)
        self.bevel = tl.fgd(60, 60, 60)
        self.bevel_hover = tl.fgd(100, 100, 100)

        self._bvl = self.bevel

    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + len(self.text) +2 and self.y <= y < self.y +3

    def mouse_move(self, x, y):
        if self._check_bounds(x, y):
            self._bgd = self.background_hover
            self._bvl = self.bevel_hover
        else:
            self._bgd = self.background
            self._bvl = self.bevel
        
    def mouse_button(self, x, y, button):
        bounds = self._check_bounds(x, y)
        if bounds and button == 1:
            self._bgd = self.background_active
            self._bvl = self.background_active
            self._fgd = self.foreground_active
            self._pressed = True
        else:
            self._fgd = self.foreground
            if bounds:
                self._bgd = self.background_hover
                self._bvl = self.bevel_hover
            else:
                self._bvl = self.background
                self._bvl = self.bevel
            if self._pressed:
                self.call()
            self._pressed = False

    def update(self):
        width = len(self.text) +2
        height = int(self._pressed)
        draw  = tl.move(self.x, self.y) + tl.ANSI_RESET + (' ' * width)                         # reset + clear spaces
        draw += tl.move(self.x, self.y + 3) + tl.ANSI_RESET + self._bvl + ('░' * width)         # sides
        draw += tl.move(self.x, self.y +height) + self._bgd + self._bvl + ('▔' * width)         # upper bevel
        draw += tl.move(self.x, self.y + 2 +height) + ('▃' * width)                             # lower bevel
        draw += tl.move(self.x, self.y + 1 +height) + self._bgd + self._fgd + f" {self.text} "  # center
        print(draw, end="")
