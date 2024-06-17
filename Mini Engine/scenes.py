import pygame, config, classes
from modules.game_functions import *
from config import *
from classes import *


class Scene:
    def __init__(self):
        self.loaded = False

    def play_scene(self):
        ######################## SCENE #########################
        self.loaded = True
        ########################################################

    def unload_scene(self):
        self.loaded = False

class Game(Scene):
    # IGNORE: To to prevent bugs
    player = BasePlayer(PLAYER_MODEL, PLAYER_MODEL_BASE_ANGLE, PLAYER_WIDTH, PLAYER_HEIGHT)

    def __init__(self):
        super().__init__()
        self.bullet_store = []
        self.block_store = []

        self.menubutton = Button(text="END",width=100, height=100, x=10, y=10,
                                 content_color=pygame.color.Color(69, 118, 255),
                                 border_thickness = 10)

    def play_scene(self, player):
        self.player = player

        ######################## SCENE #########################


        # Poll for key and mouse events.
        keys = pygame.key.get_pressed()

        # Create a new block when the "1" key is pressed.
        if keys[pygame.K_1]:
            create_brick(self.block_store, BRICK_MODEL, BLOCK_WIDTH, BLOCK_HEIGHT,
                         offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y)

        # Create a new gear when the "2" key is pressed.
        if keys[pygame.K_2]:
            create_gear(self.block_store, GEAR_MODEL, BLOCK_WIDTH, BLOCK_HEIGHT,
                        offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y,
                        max_angular_speed=GEAR_SPEED)

        # Refresh the window
        WINDOW.fill((0, 0, 0))

        # Create a 100x100 grid
        draw_grid(WINDOW, GRID_WIDTH, GRID_HEIGHT,
                  offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y, color=GRID_COLOR)

        # Draw bullets in the bullet store
        draw_stored_bullets(WINDOW, self.bullet_store)
        # Draw blocks in the block store
        draw_stored_blocks(WINDOW, self.block_store, self.player)

        # Check for collision between bullets and blocks
        check_bullet_block_collision(self.player, bullet_store=self.bullet_store, block_store=self.block_store)

        # Draw the player
        self.player.draw(WINDOW)

        self.menubutton.draw(WINDOW)

        ########################################################

    def unload_scene(self):
        self.loaded = False
        print(self.loaded)