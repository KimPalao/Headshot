from abc import ABC
from os import getcwd
from os.path import join

# from game_objects.player import Player
from pyglet import clock

from audio import powerup
from game_objects.projectile import Projectile


class Powerup(Projectile, ABC):

    def on_collide(self, player):
        powerup.play()
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


class ShieldPowerup(Powerup):
    def __init__(self, speed=10, damage=0.8, *args, **kwargs):
        src = join(getcwd(), 'images', 'shield_powerup.png')
        super().__init__(src=src, speed=speed, damage=damage, *args, **kwargs)

    def on_collide(self, player):
        player.damage_modifier *= self.damage
        super().on_collide(player)


class ImmunityPowerup(Powerup):
    def __init__(self, speed=10, damage=0.8, *args, **kwargs):
        src = join(getcwd(), 'images', 'immunity_powerup.png')
        super().__init__(src=src, speed=speed, damage=damage, *args, **kwargs)

    def on_collide(self, player):
        original_modifier = player.damage_modifier
        clock.schedule_once(lambda x: setattr(player, 'damage_modifier', original_modifier), 10)
        player.damage_modifier = 0
        super().on_collide(player)


class DamagePowerup(Powerup):
    def __init__(self, speed=10, damage=10, *args, **kwargs):
        src = join(getcwd(), 'images', 'damage_buff_powerup.png')
        super().__init__(src=src, speed=speed, damage=damage, *args, **kwargs)

    def on_collide(self, player):
        player.damage += self.damage
        super().on_collide(player)


powerups = [HealPowerup, ChargePowerup, ShieldPowerup, ImmunityPowerup]
