from core import interface
from core import terminal as tl
from datetime import datetime

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


if __name__ == '__main__':
    interface.register_module(Control())
    interface.set_framerate(20)
    interface.run()
