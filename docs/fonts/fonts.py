from pyglet import font
from os.path import join
from os import getcwd

press_start_2p = 'Press Start 2P'
font.add_file(join('fonts', 'press_start_2p', 'PressStart2P.ttf'))
font.load(press_start_2p)
