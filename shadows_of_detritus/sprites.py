import pygame as pg
import math
from settings import *
from menu_widget_loader import *
from player_image_loader import *
from mob_image_loader import *
from item_image_loader import *
import pytmx

# Use pygame's built in vector movement to a variable for future calculations
vec = pg.math.Vector2


# Define the various properties of the player
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        # Assign this player sprite to the following group
        self.groups = game.all_sprites, game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        # Use this this to begin the name.all_sprites, assigning to the main game function
        self.game = game
        # Get the image assigned in Game and rescale it by 200%
        self.image = pg.transform.scale(game.player_img, (32, 40))
        # Debug Shapes
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        # Get the rect of the image to use in later functions and comaprisons
        self.rect = PLAYER_HIT_RECT
        self.rect.center = (0, 0)
        self.rect.x = x - 10
        self.rect.y = y - 10
        # set the position of the player to the vector(x, y) times the TILESIZE in settings.py
        self.pos = vec(x, y)
        # These flags are used to detect the direction of the player. Currently, only 5/9 directions are implemented
        # The diagonals don't work at the moment
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.standing = True
        # Set the walk count, used to cycle through walking animation, to 0
        self.walkCount = 0
        self.move = PLAYER_SPEED
        self.move_diag = self.move * 0.7071
        self.booster = False

    # Register key input and return a movement update
    def get_keys(self):
        # set the movement vector to 0 when called
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        self.booster = True if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else False
        self.move = PLAYER_SPEED * 2 if keys[pygame.K_LSHIFT] and self.booster else PLAYER_SPEED

        if keys[pg.K_KP_ENTER]:
            print("Enter is currently being pressed")

        if keys[pg.K_LEFT] or keys[pg.K_a]:  # When Left or A is pressed
            self.vel.x = -self.move

        if keys[pg.K_RIGHT] or keys[pg.K_d]:  # When Right or D is pressed
            self.vel.x = self.move

        if keys[pg.K_UP] or keys[pg.K_w]:  # When Up or W is pressed
            self.vel.y = -self.move

        if keys[pg.K_DOWN] or keys[pg.K_s]:  # When Down or S is pressed
            self.vel.y = self.move

        elif self.vel.x != 0 and self.vel.y != 0:  # If the movement vector is not 0 (moving along the diagonals)
            self.vel.x *= 0.7071  # Square Root of 2
            self.vel.y *= 0.7071

    # Define collsion with any sprite in the selected group. Currently, only using the wall group
    def collide_with_walls(self, dir):
        # If the direction of the sprite is x
        if dir == 'x':
            # Hits is a collison with a sprite in the game.walls group
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:  # When the player hits a wall
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def interact(self, dir):
        # The algotithim: When the player is within a hitbox od an interactable object, draw a text box or a sprite
        keys = pg.key.get_pressed()

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.interactable, False)
            if hits:  # When the player hits a wall
                self.game.text_open = True
                self.game.inter_obj_id = 1

            else:
                self.game.text_open = False
                self.game.inter_obj_id = 0
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.interactable, False)
            if hits:  # When the player hits a wall
                self.game.text_open = True
                self.game.inter_obj_id = 1
                print(self.game.text_open)
            else:
                self.game.text_open = False
                self.game.inter_obj_id = 0

    # Update everything that will be drawn to the screen(s)
    def update(self):
        # Start the keys for events
        self.get_keys()
        # Set the current walkcount to 0 if walkcount + 1 is >= the number of frames * 3
        if self.walkCount + 1 >= 12:
            self.walkCount = 0
            # Reintialize and redeclare the key events
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:  # When the Right or D is pressed, the player is facing right
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.standing = False

        elif keys[pg.K_LEFT] or keys[pg.K_a]:  # When the Right or A is pressed, the player is facing left
            self.right = False
            self.left = True
            self.up = False
            self.down = False
            self.standing = False

        elif keys[pg.K_UP] or keys[pg.K_w]:  # When the Right or A is pressed, the player is facing up
            self.right = False
            self.left = False
            self.up = True
            self.down = False
            self.standing = False

        elif keys[pg.K_DOWN] or keys[pg.K_s]:  # When the Right or A is pressed, the player is facing down
            self.right = False
            self.left = False
            self.up = False
            self.down = True
            self.standing = False

        else:  # Otherwise, the player is standing and set walkcount to 0
            self.standing = True
            self.walkCount = 0

        if not self.standing and not self.booster:
            # Cycle through the frames of movement animation and rescale it to 200% of the sprite's original size
            if self.vel.x == PLAYER_SPEED:
                # Must achieve a value of 2
                self.image = pg.transform.scale(walkRight[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            elif self.vel.x == -PLAYER_SPEED:
                self.image = pg.transform.scale(walkLeft[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            elif self.vel.y == PLAYER_SPEED:
                self.image = pg.transform.scale(walkDown[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            elif self.vel.y == -PLAYER_SPEED:
                self.image = pg.transform.scale(walkUp[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            elif self.vel.y >= self.move_diag or self.vel.x >= self.move_diag:
                self.image = pg.transform.scale(walkUpLeft[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            elif self.vel.y <= -self.move_diag or self.vel.x <= -self.move_diag:
                self.image = pg.transform.scale(walkUpRight[self.walkCount // 6], (32, 40))
                self.walkCount += 1
            # Otherwise, the player is standing still, so use the player idle sprite
            else:
                self.image = pg.transform.scale(self.game.player_img, (32, 40))

        # Dash
        if self.booster and not self.standing:
            # Cycle through the frames of movement animation and rescale it to 200% of the sprite's original size
            if self.vel.x == self.move:
                self.image = pg.transform.scale(dashRight[self.walkCount // 6], (48, 48))
                self.walkCount += 1
            elif self.vel.x == -self.move:
                self.image = pg.transform.scale(dashLeft[self.walkCount // 6], (48, 48))
                self.walkCount += 1
            elif self.vel.y == self.move:
                # The calculation must result in 4
                self.image = pg.transform.scale(dashDown[self.walkCount // 3], (64, 72))
                self.walkCount += 1
            elif self.vel.y == -self.move:
                self.image = pg.transform.scale(dashUp[self.walkCount // 3], (64, 72))
                self.walkCount += 1
            # This fixes the issue of the upwards diagonals not working
            elif self.vel.y >= self.move_diag or self.vel.x >= self.move_diag:
                # must equal 2
                self.image = pg.transform.scale(dashUpRight[self.walkCount // 6], (48, 72))
                self.walkCount += 1
            elif self.vel.y <= -self.move_diag or self.vel.x <= -self.move_diag:
                self.image = pg.transform.scale(dashUpLeft[self.walkCount // 6], (48, 72))
                self.walkCount += 1
            # Otherwise, the player is standing still, so use the player idle sprite
            else:
                self.image = pg.transform.scale(self.game.player_img, (32, 40))

        # The position is equal to the velocity by the fps calculation
        self.pos += self.vel * self.game.dt
        # set the player x pos to the x in the above calculation
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.dir = 'x'
        # set the player y pos to the y in the above calculation
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.dir = 'y'


# A monster, that collides with walls, cannot touch the player or else the game crashes
class Hostile_Mob(pg.sprite.Sprite):
    # The sprite used here is assumed to match the game's 32 by 32 resolution
    def __init__(self, game, x, y, w, h):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(mushroom, (32, 32))  # pg.transform.scale(game.player_img, (32, 40))
        self.rect = pg.Rect(x, y, w, h)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.walkCount = 0
        # self.acc = vec(8, 0)
        # self.rect.center = self.pos
        self.move = 100
        # self.player_position = (0, 0)

    def collide_with_walls(self, dir):
        # If the direction of the sprite is x
        if dir == 'x':
            # Hits is a collison with a sprite in the game.walls group
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:  # When the player hits a wall
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_player(self, dir):
        # If the direction of the sprite is x
        if dir == 'x':
            # Hits is a collison with a sprite in the game.walls group
            hits = pg.sprite.spritecollide(self, self.game.player_group, False)
            if hits:  # When the player hits a wall
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                self.kill()
                self.game.battle()
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.player_group, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.kill()
                self.game.battle()

    def update(self):
        if not self.game.player.standing:
            self.vel = pg.math.Vector2(self.game.player.rect.x - self.rect.x,
                                       self.game.player.rect.y - self.rect.y)
            self.vel.normalize()

            self.vel.scale_to_length(self.move)
            # self.rect.move_ip(self.vel)

            # Increase the speed as the mob moves around
            if self.move < 500:
                self.move += 1

            if self.walkCount + 1 >= 8:
                self.walkCount = 0

            if self.vel == -self.move:
                self.image = pg.transform.scale(mushroom_running[self.walkCount // 4], (32, 40))
                self.walkCount += 1
            if self.vel == +self.move:
                self.image = pg.transform.scale(mushroom_running[self.walkCount // 4], (32, 40))
                self.walkCount += 1
            else:
                self.image = pg.transform.scale(mushroom, (32, 40))

            self.pos += self.vel * self.game.dt
            self.rect.x = self.pos.x
            self.collide_with_walls('x')
            self.collide_with_player('x')
            self.rect.y = self.pos.y
            self.collide_with_walls('y')
            self.collide_with_player('y')


class Fearful_Mob(pg.sprite.Sprite):
    # The sprite used here is assumed to match the game's 32 by 32 resolution
    def __init__(self, game, x, y, w, h):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(mushroom, (32, 32))  # pg.transform.scale(game.player_img, (32, 40))
        self.rect = pg.Rect(x, y, w, h)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        # self.acc = vec(8, 0)
        # self.rect.center = self.pos
        self.move = 100
        # self.player_position = (0, 0)

    def collide_with_walls(self, dir):
        # If the direction of the sprite is x
        if dir == 'x':
            # Hits is a collison with a sprite in the game.walls group
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:  # When the player hits a wall
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_with_player(self, dir):
        # If the direction of the sprite is x
        if dir == 'x':
            # Hits is a collison with a sprite in the game.walls group
            hits = pg.sprite.spritecollide(self, self.game.player_group, False)
            if hits:  # When the player hits a wall
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                self.kill()
                self.game.battle()
        if dir == 'y':  # When the player hits a wall
            hits = pg.sprite.spritecollide(self, self.game.player_group, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.kill()
                self.game.battle()

    def update(self):
        if not self.game.player.standing:
            self.vel = pg.math.Vector2(self.game.player.rect.x - self.rect.x,
                                       self.game.player.rect.y - self.rect.y)
            self.vel.normalize()

            self.vel.scale_to_length(-self.move)
            # self.rect.move_ip(self.vel)

            # Increase the speed as the mob moves around
            if self.move < 500:
                self.move += 1
            else:
                self.move = 100

            self.pos += self.vel * self.game.dt
            self.rect.x = self.pos.x
            self.collide_with_walls('x')
            self.collide_with_player('x')
            self.rect.y = self.pos.y
            self.collide_with_walls('y')
            self.collide_with_player('y')


# An unused bullet projectile
class Bullet(pg.sprite.Sprite):
    def __int__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = debug_bullet
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.vel = dir * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()


# The generic wall for all collisions
class Obstacle(pg.sprite.Sprite):
    # The sprite used here is assumed to match the game's 32 by 32 resolution
    def __init__(self, game, x, y, w, h):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# A special debug tile, used to test interaction and part of the interactables group
class Special(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.interactable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


# A door or other entrance that will load a new area
class TextBox(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # The sprite used here is assumed to match the game's 32 by 32 resolution
        self.groups = game.text_boxes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = debug_screen_bg_button
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def update(self):
        keys = pg.key.get_pressed()

        if not self.state:
            self.kill()


class VFX(pg.sprite.Sprite):
    # The sprite used here is assumed to match the game's 32 by 32 resolution
    def __int__(self, game, pos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = debug_bullet
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > 40:
            self.kill()
