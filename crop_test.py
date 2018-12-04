from game_objects.projectile import Projectile
from matplotlib import pyplot as plt
from math import pi

if __name__ == '__main__':
    p = Projectile(src='images/meteor_1.png')
    images = 24
    divisor = 6
    ratio = pi/divisor
    for i in range(images):
        plt.subplot(6, 4, i+1)
        p.rotate(ratio)
        plt.imshow(p.np)
        plt.title(f'{i+1}pi/{images/2}')
        plt.xticks([])
        plt.yticks([])
    plt.show()
