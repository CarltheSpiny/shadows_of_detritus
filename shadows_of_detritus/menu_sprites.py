import pygame as pg
import math
from settings import *
from menu_widget_loader import *

vec = pg.math.Vector2


class Widget(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self._layer = 3
        # Assign this player sprite to the following group
        self.groups = game.menu
        pg.sprite.Sprite.__init__(self, self.groups)
        # Use this this to begin the name.all_sprites, assigning to the main game function
        self.game = game
        # Get the image assigned in Game and rescale it by 200%
        self.image = image
        self.x = x
        self.y = y

    def draw(self):
        self.game.main_layer.blit(self.image, (self.x, self.y))
