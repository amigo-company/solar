from core import terminal as tl

# ----------------------------------------------------------------------------------------------------------------------
# Module class
class Module:
    def update(self): ...
    def resize(self, width: int, height: int): ...
    def keyboard(self, key: int, press: bool, keycode: int): ...
    def mouse_move(self, x: int, y: int): ...
    def mouse_button(self, x: int, y: int, button: int): ...
    def mouse_scroll(self, x: int, y: int, direction: int): ...


# ----------------------------------------------------------------------------------------------------------------------
# Globals
width, height = tl.size()
modules: list[Module] = []
running = True


# ----------------------------------------------------------------------------------------------------------------------
# Modules
def register_module(module: Module):
    global modules
    modules.append(module)

def unregister_module(module: Module):
    global modules
    if module in modules:
        modules.remove(module)

def clear_modules():
    global modules
    modules = []


# ----------------------------------------------------------------------------------------------------------------------
# Framerate
_TIME_ELAPSED_SAMPLE_COUNT: int = 8
_BASE_FRAMETIME: float = 0.025
_ftime = _BASE_FRAMETIME
_time_elapsed_ptr: int = 0
_time_elapsed_samples: list[float] = [_BASE_FRAMETIME for _ in range(_TIME_ELAPSED_SAMPLE_COUNT)]
def set_framerate(fps: int):
    global _ftime
    _ftime = max(0.001, min(1.0, 1.0 / fps))


# ----------------------------------------------------------------------------------------------------------------------
# Runtime
def stop():
    global running
    running = False

def run():
    global _ftime, _time_elapsed_ptr, _time_elapsed_samples
    global width, height
    global running
    global modules
    import time
    from datetime import datetime

    tl.set_console_flags()
    tl.hide_cursor()
    tl.clear_screen()
    while running:
        t0 = datetime.now()
        print(tl.move(0, 0)) # no end='' to flush the buffer

        _w, _h = tl.size()
        if width != _w or height != _h:
            width, height = _w, _h
            for m in modules:
                m.resize(width, height)

        while ie := tl.read_input():
            if ie['type'] == tl.INPUT_MOUSE:
                if ie['event'] == tl.INPUT_MOUSE_MOVE:
                    for m in modules:
                        m.mouse_move(ie['x'], ie['y'])
                elif ie['event'] == tl.INPUT_MOUSE_BUTTON:
                    for m in modules:
                        m.mouse_button(ie['x'], ie['y'], ie['button'])
                elif ie['event'] == tl.INPUT_MOUSE_WHEEL:
                    for m in modules:
                        m.mouse_scroll(ie['x'], ie['y'], ie['button'])
            elif ie['type'] == tl.INPUT_KEYBOARD:
                for m in modules:
                    m.keyboard(ie['key'], ie['press'], ie['keycode'])

        for m in modules:
            m.update()

        _time_elapsed_samples[_time_elapsed_ptr] = float((datetime.now() - t0).microseconds) / 1_000_000
        time.sleep(max(0, _ftime - (sum(_time_elapsed_samples) / _TIME_ELAPSED_SAMPLE_COUNT)))
        _time_elapsed_ptr = (_time_elapsed_ptr +1) % _TIME_ELAPSED_SAMPLE_COUNT
    
    tl.show_cursor()
    tl.clear_screen()
    print(f"{tl.move(0, 1)}{tl.ANSI_RESET}", end='')
