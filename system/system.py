from matplotlib import pyplot as plt
from pyglet.canvas import get_display


# from interfaces.game_interface import GameInterface
# from widgets.event_window import EventWindow


def plot_pictures(rows, cols, *images):
    for i, image in enumerate(images):
        try:
            plt.subplot(rows, cols, i + 1)
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])
        except Exception as e:
            print(f'Crashed at: {i} {e}')
    plt.show()


def get_window():
    return get_display().get_windows()[0]


def get_player():
    try:
        return get_window().current_interface.player
    except:
        return None


def get_enemy():
    try:
        return get_window().current_interface.enemy
    except:
        return None
