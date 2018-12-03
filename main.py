import traceback
import time

from pyglet import options, gl, app
from pyglet.window import get_platform, key

from interfaces.main_interface import MainInterface
from widgets.event_window import EventWindow
from pyglet import clock
from interfaces.game_interface import GameInterface

options['debug_gl'] = False

# Used to enable transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Lets the game start in full screen mode
platform = get_platform()
display = platform.get_default_display()
screen = display.get_default_screen()
window = EventWindow(width=screen.width, height=screen.height, resizable=True)
keys = key.KeyStateHandler()
window.push_handlers(keys)
window.maximize()


if __name__ == '__main__':
    window.load_interface(MainInterface())
    # window.load_interface(GameInterface())
    try:
        # Own version of running the pyglet event loop.
        while 1:
            clock.tick()
            if window.has_exit:  # True when the user clicks X
                window.close()
                break
            for window in app.windows:  # Standard Pyglet event loop stuff
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()
            time.sleep(1 / 120)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        input()
