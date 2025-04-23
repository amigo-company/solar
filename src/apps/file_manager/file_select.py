from solar import (
    terminal as tl,
    widgets,
    interface
)

# import mytest
# mytest.hello()

class Main(interface.Module):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.button_select = widgets.RaisedButton(" Select ", 0, 0)
        self.button_cancel = widgets.RaisedButton(" Cancel ", 0, 0)

        self.buttons_width = self.button_select.get_size()[0] + self.button_cancel.get_size()[0] +1
        self.button_select.x = width - self.buttons_width -1
        self.button_select.y = height -5
        self.button_cancel.x = width - self.button_cancel.get_size()[0] -1
        self.button_cancel.y = height -5
        self.button_cancel.action = self.action_button_cancel

        interface.register_module(self.button_select)
        interface.register_module(self.button_cancel)

    # def keyboard(self, key, press, keycode):
    #     if key == ord('q'):
    #         interface.stop()

    def action_button_cancel(self):
        interface.stop()