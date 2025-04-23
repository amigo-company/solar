import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # prioritize local package

from datetime import datetime
from solar import interface
from solar import terminal as tl
from solar.widgets import TextButton, RaisedButton

class Control(interface.Module):
    def __init__(self):
        self.frames = 0
        self.dt = datetime.now()
        self.icon_x = 0

    def update(self):
        print(tl.move(self.icon_x, 1) + "🫨")
        self.frames += 1
        self.icon_x = 1 - self.icon_x
        if (datetime.now() - self.dt).seconds > 1:
            print(tl.move(0, 0) + f"FPS {self.frames}")
            self.frames = 0
            self.dt = datetime.now()

    def keyboard(self, key, press, keycode):
        if key == ord('q'):
            interface.stop()

    def resize(self, width: int, height: int):
        print(tl.move(0, 3) + f"Window resized to {width}x{height}")


if __name__ == '__main__':
    interface.register_module(Control())

    button = TextButton(" Click me! ", 2, 6)
    interface.register_module(button)

    button2 = TextButton(" Or me! ", 2, 7)
    interface.register_module(button2)

    raised_button = RaisedButton(" Click me! ", 2, 10)
    interface.register_module(raised_button)

    interface.set_framerate(20)
    interface.run()
