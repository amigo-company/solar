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
class ColorHint:
    def __init__(self, col: str = '', col_hover: str = '', col_active: str = ''):
        self.color: str = col
        self.color_hover: str = col_hover
        self.color_active: str = col_active
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
        self.action = lambda: None
        self.fgd = ColorHint(DEFAULT_FGD, DEFAULT_FGD_HOVER, DEFAULT_FGD_ACTIVE)
        self.bgd = ColorHint(DEFAULT_BGD, DEFAULT_BGD_HOVER, DEFAULT_BGD_ACTIVE)
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
            self.action()
        self._pressed = pressed

    def update(self):
        bgd = self.bgd.get_color()
        fgd = self.fgd.get_color()
        print(f"{tl.move(self.x, self.y)}{bgd}{fgd}{self.text}", end="")


class RaisedButton(_IButton_):
    def __init__(self, text: str = "", x: int = 0, y: int = 0):
        super().__init__(text, x, y)
        self.bevel = ColorHint(tl.fgd(60, 60, 60), tl.fgd(100, 100, 100), tl.fgd(240, 240, 240))

    def _check_bounds(self, x: int, y: int) -> bool:
        return self.x <= x < self.x + len(self.text) +2 and self.y <= y < self.y +3
    
    def get_size(self) -> tuple[int, int]:
        return len(self.text) +2, 4

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
            self.action()
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
class _IList_(Module):
    def __init__(self, items: list, x: int, y: int, width: int, height: int):
        self.items = items
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_x = 0
        self.scroll_y = 0

        self.fgd = ColorHint(DEFAULT_FGD, DEFAULT_FGD_HOVER, DEFAULT_FGD_ACTIVE)
        self.bgd = ColorHint(tl.ANSI_RESET, DEFAULT_BGD_HOVER, DEFAULT_BGD_ACTIVE)
        self.hover_item = -1
        self.active_item = -1

    def _check_bounds(self, x: int, y: int) -> bool:
        return (self.x <= x < self.x + self.width) and (self.y <= y < self.y + self.height)
    
    def get_item(self):
        return self.items[self.active_item]

class ItemSelectList(_IList_):
    def __init__(self, items: list, x: int, y: int, width: int, height: int):
        super().__init__(items, x, y, width, height)
        
    def mouse_move(self, x, y):
        self.hover_item = (y - self.y +self.scroll_y) if self._check_bounds(x, y) else -1

    def mouse_button(self, x, y, button):
        if button == 1 and self._check_bounds(x, y):
            self.active_item = (y - self.y +self.scroll_y)
            if self.active_item > (len(self.items) -1):
                self.active_item = -1

    def mouse_scroll(self, x, y, direction):
        if self._check_bounds(x, y):
            self.scroll_y += direction
        self.scroll_y = max(0, min(len(self.items) -1, self.scroll_y))

    def update(self):
        print(tl.ANSI_RESET + tl.fgd(255, 255, 255), end='')
        tl.draw_box(self.x -1, self.y -1, self.width +1, self.height +1)

        draw = ''
        for y in range(self.height -1):
            id = y + self.scroll_y
            item = self.items[id] if id < len(self.items) else ''
            
            on_hover, on_active = id == self.hover_item, id == self.active_item
            self.bgd.hover, self.fgd.hover = on_hover, on_hover
            self.bgd.active, self.fgd.active = on_active, on_active

            padding = ' ' * max(0, self.width - len(item) -1)
            draw += f"{tl.move(self.x, self.y +y)}{self.bgd.get_color()}{self.fgd.get_color()}{item}{padding}"

        print(draw, end='')

    