from game_objects.projectile import Projectile
from matplotlib import pyplot as plt
from math import pi

if __name__ == '__main__':
    p = Projectile(src='projectiles/dull_knife.png')
    images = 24
    divisor = 6
    ratio = pi/divisor
    for i in range(images):
        plt.subplot(6, 4, i+1)
        p.rotate(ratio)
        plt.imshow(p.np)
        plt.title(f'{i}pi/{images}')
        plt.xticks([])
        plt.yticks([])
    plt.show()
