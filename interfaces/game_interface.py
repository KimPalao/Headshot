import dlib
import json
import traceback
import time

import cv2 as cv

from random import randint

from typing import List

from pyglet import options, gl, clock, app
from pyglet.graphics import Batch
from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.window import get_platform, FPSDisplay, key

from pygarrayimage.arrayimage import ArrayInterfaceImage

from widgets.event_window import EventWindow
from widgets.facecam import Facecam
from widgets.interface import Interface
from widgets.player import Player
from widgets.projectile import Projectile
from widgets.rectangle import Rectangle

options['debug_gl'] = False
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


class GameInterface(Interface):
    aii: ArrayInterfaceImage = None
    background_sprite: Sprite = None
    batch: Batch = None
    border: Rectangle = None
    detector = dlib.get_frontal_face_detector()
    image = None
    facecam: Facecam = None
    face_cascade = dlib.get_frontal_face_detector()
    foreground_sprite: Sprite = None
    fps_display: FPSDisplay = None
    keys = key.KeyStateHandler()
    player: Player = None
    projectiles: List[Projectile] = []

    def __init__(self):
        super().__init__()
        background = load('images/background.png')
        self.background_sprite = Sprite(background)
        self.background_sprite.image.anchor_x = self.background_sprite.image.width / 2
        self.background_sprite.image.anchor_y = self.background_sprite.image.height / 2
        foreground = load('images/foreground.png')
        self.foreground_sprite = Sprite(foreground)
        self.foreground_sprite.image.anchor_x = self.foreground_sprite.image.width / 2
        self.foreground_sprite.image.anchor_y = self.foreground_sprite.image.height / 2
        self.foreground_sprite.scale = 1.3
        self.face_cascade = cv.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
        self.detector = dlib.get_frontal_face_detector()
        self.facecam = Facecam(face_cascade=self.face_cascade).start()
        img = self.facecam.read()
        self.aii = ArrayInterfaceImage(img, 'BGR')
        self.image = self.aii.texture
        self.player = Player(src='chihiro.png')
        self.border = Rectangle(width=self.image.width + 10, height=self.image.height + 10)
        self.player.scale = 1.2
        self.batch = Batch()
        self.projectiles: List[Projectile] = []
        self.scheduled_functions = (
            (self.randomize_projectiles, 2),
            (self.check_direction, 1/120)
        )

    def on_bind(self):
        self.fps_display = FPSDisplay(self.window)
        self.background_sprite.x = self.window.width / 2
        self.background_sprite.y = self.window.height / 2
        self.foreground_sprite.x = self.window.width / 2
        self.foreground_sprite.y = self.window.height / 2
        self.image.x = (self.window.width - self.image.width) / 2
        self.image.y = (self.window.height - self.image.height) / 2
        self.border.x = (self.window.width - self.border.width) / 2
        self.border.y = (self.window.height - self.border.height) / 2
        self.player.move(x=self.window.width / 2, y=self.window.height / 2)

        @self.facecam.event('on_face_move')
        def follow_face(x, y, width, height):
            new_x = self.image.x + x + width // 2
            new_y = self.image.y + y + height // 2
            self.player.move(new_x, new_y)

        self.window.push_handlers(self.facecam)
        self.window.push_handlers(self.keys)
        for func in self.scheduled_functions:
            clock.schedule_interval(*func)
        # clock.schedule_interval(self.randomize_projectiles, 2)
        # clock.schedule_interval(self.check_direction, 1 / 120)

    def on_draw(self):
        self.window.clear()
        self.background_sprite.draw()
        self.foreground_sprite.draw()
        self.border.draw()
        # aii.view_new_array(facecam.read())
        self.fps_display.draw()
        self.player.draw()
        self.batch.draw()
        for projectile in self.projectiles:
            if projectile.active:
                projectile.forward()
                if self.player.check_for_collision(projectile):
                    projectile.delete()
                    print(self.player.take_damage(projectile.damage))

    def randomize_projectiles(self, dt):
        x = randint(0, self.window.width)
        y = randint(0, self.window.height)
        projectile = Projectile(src='images/candy_cane.png', x=x, y=y, damage=10.0, batch=self.batch, speed=0,
                                background=(255, 255, 255), acceleration=4)
        projectile.scale = 2
        projectile.point(self.player.x, self.player.y)
        self.projectiles.append(projectile)

    def check_direction(self, dt):
        unit = 10
        if self.keys[key.DOWN]:
            if self.player.get_bot_bound() - unit >= self.border.y:
                self.player.y -= unit
        elif self.keys[key.UP]:
            if self.player.get_bot_bound() + self.player.height + unit <= self.border.y + self.border.height:
                self.player.y += unit
        if self.keys[key.LEFT]:
            if self.player.get_left_bound() - unit >= self.border.x:
                self.player.x -= unit
        elif self.keys[key.RIGHT]:
            if self.player.get_left_bound() + self.player.width + unit <= self.border.x + self.border.width:
                self.player.x += unit
        fg_ratio = 0.4
        bg_ratio = 0.1
        self.foreground_sprite.x = (self.window.width * (1 + fg_ratio)) / 2 - self.player.x * fg_ratio
        self.foreground_sprite.y = (self.window.height * (1 + fg_ratio)) / 2 - self.player.y * fg_ratio
        self.background_sprite.x = (self.window.width * (1 + bg_ratio)) / 2 - self.player.x * bg_ratio
        self.background_sprite.y = (self.window.height * (1 + bg_ratio)) / 2 - self.player.y * bg_ratio
