import pygame
import random
import player_image_loader
import menu_widget_loader

# from pygame.locals import *

WIDTH = 512
HEIGHT = 512
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
main_layer = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Template")
clock = pygame.time.Clock()


# The images
# player_images = pygame.image.load('assets/textures/dev_player')


# The classes

class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 32, self.y + 32, 20, 52)

    def draw(self, win):
        # Records walking when the player reaches the end of the current screen
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(player_image_loader.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            elif self.right:
                win.blit(player_image_loader.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

        else:
            win.blit(player_image_loader.idle, (self.x, self.y))
        self.hitbox = (self.x + 32, self.y + 32, 20, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


def redrawGameWindow():
    main_layer.blit(menu_widget_loader.debug_screen_bg, (0, 0))
    player.draw(main_layer)

    pygame.display.update()


# Game loop
player = Player(200, 410, 48, 48)
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > player.vel:
        player.x -= player.vel
        player.left = True
        player.right = False
        player.standing = False

    elif keys[pygame.K_RIGHT] and player.x < 500 - player.width - player.vel:
        player.x += player.vel
        player.right = True
        player.left = False
        player.standing = False

    else:
        player.standing = True
        player.walkCount = 0

    # Update
    redrawGameWindow()

    # Draw / render
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
