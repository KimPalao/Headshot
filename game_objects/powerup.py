from abc import ABC
from os import getcwd
from os.path import join

# from game_objects.player import Player
from game_objects.projectile import Projectile


class Powerup(Projectile, ABC):

    def on_collide(self, player):
        self.delete()


class HealPowerup(Powerup):
    def __init__(self, speed=10, damage=20, *args, **kwargs):
        src = join(getcwd(), 'images', 'heal_powerup.png')
        super().__init__(src=src, speed=speed, damage=damage, *args, **kwargs)

    def on_collide(self, player):
        player.health += self.damage
        super().on_collide(player)


class ChargePowerup(Powerup):
    def __init__(self, speed=10, damage=20, *args, **kwargs):
        src = join(getcwd(), 'images', 'heal_powerup.png')
        super().__init__(src=src, speed=speed, damage=damage, *args, **kwargs)

    def on_collide(self, player):
        player.energy_bar += self.damage
        super().on_collide(player)


powerups = [HealPowerup]
