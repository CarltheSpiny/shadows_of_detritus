import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Shadows of Detritus: Prologue"
BGCOLOR = DARKGREY  # This is used to fill any empty space on the screen with this color

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player Settings
PLAYER_SPEED = 200  # This is the speed of the player
# PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'd1.png'  # This is the sprite of the player used by default, when no direction is inputted
PLAYER_HIT_RECT = pg.Rect(0, 0, 16, 20)  # The Hitbox of the player, used by some debug functions

# Mob Settings
MOB_IMG = ""

# Bullet Settings
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
