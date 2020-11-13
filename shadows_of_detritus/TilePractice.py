import pygame as pg
import sys
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

        # Load the map used for the current screen/area
        self.map = TiledMap(path.join(map_folder, 'debug_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # The sprite of the player
        self.player_img = pg.image.load(path.join(dev_player_folder, PLAYER_IMG)).convert_alpha()

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

        # Load the tiles based on the map from self.map
        """for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':  # Where there is a 1, place a border
                    Border(self, col, row)
                if tile == "W":
                    Wall(self, col, row)
                if tile == "F":
                    TextBox(self, col, row)
                if tile == "S":
                    Special(self, col, row)
                if tile == "Q":
                    Path(self, 0, col, row)
                if tile == "E":
                    Path(self, 1, col, row)
                if tile == "A":
                    Path(self, 2, col, row)
                if tile == "B":
                    Path(self, 3, col, row)
                if tile == "C":
                    Path(self, 4, col, row)
                if tile == "D":
                    Path(self, 5, col, row)

                # These must blited first
                if tile == 'P':  # Set the player starting position to wherever P is
                    self.player = Player(self, col, row)
                if tile == "M":
                    Mob(self, col, row)"""

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width,
                         tile_object.height)
            if tile_object.name == 'mushroom':
                Mob(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'interactable':
                Special(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        # Intialize the camera and limit it to the current loaded map size
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    # game loop - set self.playing = False to end the game
    def run(self):
        self.playing = True
        self.text_open = True
        # Use this to start the game in debug mode
        self.debug_mode = True
        while self.playing:
            # Set the dt value, used for entity movement, to the fps / 1000
            self.dt = self.clock.tick(FPS) / 1000.0

            # Do all the functions nested in these functions
            if self.text_open:
                self.show_go_screen()
                self.text_open = False
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

    def show_start_screen_1(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab1, debug_screen_bg_start_tab1_rect)
        self.main_layer.blit(debug_screen_bg_savefile_1, (84, 400))
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
                        debug.play()
                    else:
                        pass
                keys = pg.key.get_pressed()

                if keys[pg.K_RIGHT]:
                    menu_screen = False
                    g.show_start_screen_2()

                if keys[pg.K_LEFT]:
                    menu_screen = False
                    g.show_start_screen_3()

                if keys[pg.K_KP_ENTER]:
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

    def menu_3_submenu_1(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3_m_1, debug_screen_bg_start_tab3_m_1_rect)

        # Buttons

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

                if keys[pg.K_RIGHT]:
                    menu_screen = False
                    pass

                if keys[pg.K_LEFT]:
                    menu_screen = False
                    pass

                if keys[pg.K_RETURN]:
                    menu_screen = False
                    g.show_start_screen_3()

                if keys[pg.K_DOWN]:
                    menu_screen = False
                    pass

                if keys[pg.K_UP]:
                    menu_screen = False
                    g.show_start_screen_3()

                if keys[pg.K_ESCAPE]:
                    self.quit()

    def show_start_screen_3(self):
        self.main_layer.fill(BLACK)
        self.main_layer.blit(debug_screen_bg_start_tab3, debug_screen_bg_start_tab3_rect)

        # Buttons
        self.main_layer.blit(debug_screen_bg_arrow_keys_s, (511, 337))
        self.main_layer.blit(debug_screen_bg_arrow_keys_u, (651, 337))

        self.main_layer.blit(debug_screen_bg_on_widget_s, (511, 625))
        self.main_layer.blit(debug_screen_bg_off_widget_u, (654, 628))

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

                if keys[pg.K_RIGHT]:
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_LEFT]:
                    menu_screen = False
                    g.show_start_screen_2()

                if keys[pg.K_RETURN]:
                    menu_screen = False
                    g.show_start_screen_1()

                if keys[pg.K_DOWN]:
                    g.menu_3_submenu_1()
                    menu_screen = False

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 300 <= mouse[0] <= 300 + 403 and 400 <= mouse[1] <= 400 + 139:
                        title_screen = False
                        g.show_start_screen_1()
                    else:
                        pass

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


# create the game object
g = Game()
while True:
    g.new()
    g.run()
    g.show_go_screen()
