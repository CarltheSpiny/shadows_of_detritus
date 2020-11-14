import pygame as pg
import sys
import pygame.mixer_music
from os import path
from settings import *
from sprites import *
from menu_sprites import *
from tilemap import *
from sound_engine import *
from text_renderer import draw_text


# The Game function
class Game:
    def __init__(self):
        pg.init()
        # The main screen
        self.main_layer = pg.display.set_mode((WIDTH, HEIGHT))
        # The Caption
        pg.display.set_caption(TITLE)
        # Start the clock function
        self.clock = pg.time.Clock()
        # Load the data in the load_data function
        self.load_data()

    def load_data(self):
        # Set the directory of the textures and sound to this one
        game_folder = path.dirname(__file__)
        # Define the folders to get textures/sprites from
        dev_player_folder = path.join(game_folder, "assets/textures/dev_player")
        dev_sound_folder = path.join(game_folder, "assets/sounds/dev_music")
        map_folder = path.join(game_folder, "assets/tile_maps")

        self.font = path.join(game_folder, 'assets/textures/font/apple_kid.ttf')
        # Load the map used for the current screen/area
        self.map = TiledMap(path.join(map_folder, 'debug_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # The sprite of the player
        self.player_img = pg.image.load(path.join(dev_player_folder, PLAYER_IMG)).convert_alpha()

        self.movement = 1
        self.guide = True

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.main_layer.blit(text_surface, text_rect)

    # initialize all variables and do all the setup for a new game
    def new(self):
        # Establish the all_sprites group
        self.all_sprites = pg.sprite.LayeredUpdates()
        # Establish the walls group
        self.walls = pg.sprite.Group()
        # Establish the interactables group
        self.interactable = pg.sprite.Group()
        # Establish the buildings group
        self.buildings = pg.sprite.Group()
        # Establish the mobs group
        self.mobs = pg.sprite.Group()
        # Establish the non-playable charcters group
        self.npc = pg.sprite.Group()
        # Establish the bullets/projectile group
        self.bullets = pg.sprite.Group()

        self.player_group = pg.sprite.Group()

        self.menu = pg.sprite.Group()

        self.text_boxes = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width,
                         tile_object.height)
            if tile_object.name == 'mushroom':
                Hostile_Mob(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'ramblin_mushroom':
                Fearful_Mob(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'interactable':
                Special(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        # Intialize the camera and limit it to the current loaded map size
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        self.text_open = False
        self.inter_obj_id = 1

    # game loop - set self.playing = False to end the game
    def run(self):
        self.playing = True
        self.debug_mode = True
        while self.playing:
            # Set the dt value, used for entity movement, to the fps / 1000
            self.dt = self.clock.tick(FPS) / 1000.0

            # Do all the functions nested in these functions

            self.events()
            if not self.paused:
                self.update()

            self.draw()

    # When the player quits the game
    def quit(self):
        pg.quit()
        sys.exit()

    # update portion of the game loop
    def update(self):
        # Update all sprites
        self.all_sprites.update()
        # Bound the camera to the player
        self.camera.update(self.player)

    # When in debug mode, draw a grid
    def draw_grid(self):
        if self.debug_mode:
            for x in range(0, WIDTH, TILESIZE):
                pg.draw.line(self.main_layer, LIGHTGREY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILESIZE):
                pg.draw.line(self.main_layer, LIGHTGREY, (0, y), (WIDTH, y))

    # Draw all sprites in the all sprites group
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # When in debug mode
        if self.debug_mode:
            # self.main_layer.fill(BGCOLOR)
            # self.draw_grid()
            pass
        # Draw every sprite in the all sprites group, only in the area of the camera
        self.main_layer.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.main_layer.blit(sprite.image, self.camera.apply(sprite))

        if self.text_open:
            self.paused = True
            self.main_layer.blit(debug_dialouge, (32, 577))
            if self.inter_obj_id == 1:
                self.draw_text("A sign, hoping that someday it will say more than just a few words",
                               self.font, 50, WHITE, 930, 657, align="se")

        pg.display.flip()

    # Catch all events here
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                if event.key == pg.K_q:
                    self.text_open = not self.text_open
                    self.player.interact(self.player.dir)
                if event.key == pg.K_RETURN:
                    self.text_open = not self.text_open

    def show_start_screen_1(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab1, debug_screen_bg_start_tab1_rect)
        self.main_layer.blit(debug_screen_bg_savefile_1, (84, 370))
        self.main_layer.blit(debug_screen_bg_arrow_s, (497, 396))
        self.main_layer.blit(debug_screen_bg_savefile_2, (84, 500))
        self.main_layer.blit(debug_screen_bg_savefile_3, (84, 630))
        # Widget(g, 84, 400, debug_screen_bg_savefile_1)

        mouse = pygame.mouse.get_pos()

        pygame.display.flip()

        menu_screen = True
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # This calculation is x <= mouse_x <= x + w and y <= mouse_y <= y + h
                    # Where x = x_pos of the image, y = y_pos of the image,
                    # w = width of the image file, and h = height of the image file
                    if 84 <= mouse[0] <= 84 + 462 and 400 <= mouse[1] <= 400 + 133:
                        menu_screen = False
                    else:
                        pass
                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT]:
                    menu_screen = False
                    g.show_start_screen_2()

                if keys[pg.K_LEFT]:
                    menu_screen = False
                    g.show_start_screen_3()

                if keys[pg.K_RETURN]:
                    menu_screen = False

                if keys[pg.K_ESCAPE]:
                    self.quit()

            # Mouse
            mouse = pygame.mouse.get_pos()

    def show_start_screen_2(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab2, debug_screen_bg_start_tab2_rect)

        mouse = pygame.mouse.get_pos()

        pygame.display.flip()

        menu_screen = True
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT]:
                    menu_screen = False
                    g.show_start_screen_3()

                if keys[pg.K_LEFT]:
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_RETURN]:
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_ESCAPE]:
                    self.quit()
            # Mouse
            mouse = pygame.mouse.get_pos()

    def show_start_screen_3(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3, debug_screen_bg_start_tab3_rect)

        # Buttons
        if self.movement == 1:
            self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_u, (651, 337))

        if self.movement == 2:
            self.main_layer.blit(debug_screen_bg_arrow_keys_u, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_s, (651, 337))

        if self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

        if not self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_u, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_s, (654, 628))

        pygame.display.flip()

        menu_screen = True
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT]:
                    # Next Screen
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_LEFT]:
                    # Previous Screen
                    menu_screen = False
                    g.show_start_screen_2()

                if keys[pg.K_RETURN]:
                    # Go to the game screen
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_DOWN] and self.movement == 1:
                    # Choose settings
                    g.menu_3_submenu_1()
                    menu_screen = False
                if keys[pg.K_DOWN] and self.movement == 2:
                    # Choose settings
                    g.menu_3_submenu_2()
                    menu_screen = False

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def menu_3_submenu_1(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3_m_1, debug_screen_bg_start_tab3_m_1_rect)

        # Buttons
        if self.movement == 1:
            self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_u, (651, 337))

        if self.movement == 2:
            self.main_layer.blit(debug_screen_bg_arrow_keys_u, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_s, (651, 337))

        if self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

        if not self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_u, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_s, (654, 628))

        pygame.display.flip()

        menu_screen = True
        setting = 0
        choosing = False
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
                    # Show the wasd option selected
                    menu_screen = False
                    self.movement = 2
                    g.menu_3_submenu_2()

                if keys[pg.K_RETURN]:
                    # Save and confirm
                    menu_screen = False
                    self.movement = 1
                    g.show_start_screen_3()

                if keys[pg.K_DOWN]:
                    menu_screen = False
                    self.movement = 1
                    g.menu_3_submenu_3()

                if keys[pg.K_UP]:
                    # Save and confirm
                    menu_screen = False
                    self.movement = 1
                    g.show_start_screen_3()

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def menu_3_submenu_2(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3_m_2, debug_screen_bg_start_tab3_m_2_rect)

        if self.movement == 1:
            self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_u, (651, 337))

        if self.movement == 2:
            self.main_layer.blit(debug_screen_bg_arrow_keys_u, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_s, (651, 337))

        if self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

        if not self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_u, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_s, (654, 628))

        pygame.display.flip()

        menu_screen = True
        setting = 0
        choosing = False
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                    # Show menu with the arrow keys selected
                    menu_screen = False
                    self.movement = 1
                    g.menu_3_submenu_1()

                if keys[pg.K_RETURN]:
                    # Confirm and save
                    menu_screen = False
                    self.movement = 2
                    g.show_start_screen_3()

                if keys[pg.K_DOWN]:
                    menu_screen = False
                    self.movement = 2
                    g.menu_3_submenu_3()

                if keys[pg.K_UP]:
                    # Save and confirm
                    menu_screen = False
                    self.movement = 2
                    g.show_start_screen_3()

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def menu_3_submenu_3(self):
        # Guide/Hints settings

        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3_m_3, debug_screen_bg_start_tab3_m_3_rect)

        if self.movement == 1:
            self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_u, (651, 337))

        if self.movement == 2:
            self.main_layer.blit(debug_screen_bg_arrow_keys_u, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_s, (651, 337))

        if self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

        if not self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_u, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_s, (654, 628))

        pygame.display.flip()

        menu_screen = True
        setting = 0
        choosing = False
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
                    # Go to the off button
                    menu_screen = False
                    self.guide = False
                    g.menu_3_submenu_4()

                if keys[pg.K_RETURN]:
                    # Confirm settings and go back to the setting overview
                    menu_screen = False
                    self.guide = True
                    g.show_start_screen_3()

                if keys[pg.K_DOWN]:
                    # Go back to the movement selection menu
                    menu_screen = False
                    self.guide = True
                    g.menu_3_submenu_1()

                if keys[pg.K_UP]:
                    # Go back to the movement select
                    menu_screen = False
                    self.guide = True
                    g.menu_3_submenu_1()

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def menu_3_submenu_4(self):
        # Guide/Hints settings

        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3_m_3, debug_screen_bg_start_tab3_m_3_rect)

        if self.movement == 1:
            self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_u, (651, 337))

        if self.movement == 2:
            self.main_layer.blit(debug_screen_bg_arrow_keys_u, (511, 337))
            self.main_layer.blit(debug_screen_bg_wasd_s, (651, 337))

        if self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

        if not self.guide:
            self.main_layer.blit(debug_screen_bg_on_widget_u, (511, 625))
            self.main_layer.blit(debug_screen_bg_off_widget_s, (654, 628))

        pygame.display.flip()

        menu_screen = True
        setting = 0
        choosing = False
        while menu_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT] or keys[pg.K_LEFT]:
                    # Go to the on button
                    menu_screen = False
                    self.guide = True
                    g.menu_3_submenu_3()

                if keys[pg.K_RETURN]:
                    # Confirm settings and go back to the setting overview
                    menu_screen = False
                    self.guide = False
                    g.show_start_screen_3()

                if keys[pg.K_DOWN]:
                    # Go back to the movement selection menu
                    menu_screen = False
                    g.menu_3_submenu_1()

                if keys[pg.K_UP]:
                    # Go back to the movement select
                    menu_screen = False
                    self.guide = False
                    g.menu_3_submenu_1()

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def show_go_screen(self):
        self.main_layer.blit(debug_screen_bg, debug_screen_bg_rect)

        # Use this to check the position of the press enter to start button
        self.main_layer.blit(debug_screen_bg_button, (300, 400))
        # pygame.draw.rect(self.main_layer, (182, 79, 135), [300, 400, 403, 139])

        # draw_text(self.main_layer, "Click here to start the game!", 18, WIDTH / 2, 300, WHITE)
        # x = 256, y = 300, font size is 18, width is 190, height is 30

        mouse = pygame.mouse.get_pos()

        pygame.display.flip()
        title_screen = True
        while title_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RETURN]:
                    title_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_ESCAPE]:
                    self.quit()

                else:
                    pass
            # Mouse
            mouse = pygame.mouse.get_pos()

    def battle(self):
        self.main_layer.blit(debug_battle, debug_screen_bg_rect)

        mouse = pygame.mouse.get_pos()

        pygame.display.flip()
        battle_screen = True
        while battle_screen:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                keys = pg.key.get_pressed()

                if keys[pg.K_RETURN]:
                    battle_screen = False

                else:
                    pass
            # Mouse
            mouse = pygame.mouse.get_pos()


# create the game object
g = Game()
g.show_go_screen()
while True:
    g.new()
    g.run()
