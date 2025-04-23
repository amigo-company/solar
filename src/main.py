import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__))) # prioritize local package

from solar import terminal as tl, interface

def get_module(module_path: str) -> interface.Module:
    directory = str(os.path.abspath(os.path.dirname(module_path))).replace('\\', '/')
    with open(module_path, 'r') as file:
        src = file.read()
    
    env = {}
    exec(f"import sys; sys.path.insert(0, '{directory}')", env)
    exec(src, env)
    module = env.get('Main')
    # assert isinstance(module, interface.Module), f"Resulting value is not an interface.Module. ({type(module)})"
    return module

width, height = tl.size()

file_selector_module = get_module("C:/amigo/software/solar/src/apps/file_manager/file_select.py")
interface.register_module(file_selector_module(0, 0, width, height))
interface.set_framerate(30)
interface.run()






# from datetime import datetime
# from solar import interface
# from solar import terminal as tl
# from solar.widgets import (
#     TextButton, RaisedButton,
#     ItemSelectList
# )

# class Control(interface.Module):
#     def __init__(self):
#         self.frames = 0
#         self.dt = datetime.now()
#         self.icon_x = 0

#     def update(self):
#         print(tl.move(self.icon_x, 1) + "🫨")
#         self.frames += 1
#         self.icon_x = 1 - self.icon_x
#         if (datetime.now() - self.dt).seconds > 1:
#             print(tl.move(0, 0) + f"FPS {self.frames}")
#             self.frames = 0
#             self.dt = datetime.now()

#     def keyboard(self, key, press, keycode):
#         if key == ord('q'):
#             interface.stop()

#     def resize(self, width: int, height: int):
#         # fill = tl.move(0, 0) + tl.bgd(0, 0, 0) + (' ' * width * height)
#         # print(fill, end='')

#         print(tl.move(0, 3) + f"Window resized to {width}x{height}")


# if __name__ == '__main__':
#     interface.register_module(Control())

#     button = TextButton(" Click me! ", 2, 6)
#     interface.register_module(button)

#     button2 = TextButton(" Or me! ", 2, 7)
#     interface.register_module(button2)

#     raised_button = RaisedButton(" Ctrl ", 2, 10)
#     interface.register_module(raised_button)

#     item_select_list = ItemSelectList(['foo', 'baar', 'jaaar'], x=50, y=1, width=20, height=10)
#     interface.register_module(item_select_list)

#     interface.set_framerate(30)
#     interface.run()
