import pygame
from modules.data_types import *
from modules.utility_functions import *

####################### CUSTOMIZATION ##########################
# User can change the following values to customize attributes

WINDOW_WIDTH: pixels = 1280
WINDOW_HEIGHT: pixels = 720
GAME_FPS = 120

pygame.init() # Do not change
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
MOUSE = pygame.mouse
MOUSE.set_visible(True)
clock = pygame.time.Clock() # Do not change
dt = 0 # Do not change

PLAYER_MODEL: ImageFilePath = r"Models/default_triangle player.png"
PLAYER_MODEL_BASE_ANGLE: angleDeg = 270
PLAYER_WIDTH: pixels = 50
PLAYER_HEIGHT: pixels = 50
PLAYER_X: pixels = WINDOW_WIDTH / 2
PLAYER_Y: pixels = WINDOW_HEIGHT / 2
PLAYER_LINEAR_SPEED: pixelspersecond = 250
PLAYER_ANGULAR_SPEED: int = 250
PLAYER_LINEAR_ACCELERATION: int = 200
PLAYER_LINEAR_DECCELERATION: Optional[int] = None
PLAYER_ANGULAR_ACCELERATION: int = 400
PLAYER_ANGULAR_DECCELERATION: Optional[int] = None
PLAYER_KEYBINDS: str = "w-a-s-d"

PLAYER_BULLET_MODEL: ImageFilePath = r"Models/default_bullet.png"
PLAYER_BULLET_BASE_ANGLE: angleDeg = 270
PLAYER_BULLET_WIDTH: pixels = 25
PLAYER_BULLET_HEIGHT: pixels = 50
PLAYER_FACING_ANGLE: angleDeg = 90
PLAYER_BULLET_SPEED: int = 1000
PLAYER_BULLET_RELOAD_TIME: miliseconds = 500

PLAYER_SHOW_RELOAD_BAR: bool = True
RELOAD_BAR_BASE_ANGLE = 0
PLAYER_RELOAD_BAR_WIDTH: pixels = 200
PLAYER_RELOAD_BAR_HEIGHT: pixels = 40
PLAYER_RELOAD_BAR_X: pixels = 10
PLAYER_RELOAD_BAR_Y: pixels = WINDOW_HEIGHT - PLAYER_RELOAD_BAR_HEIGHT - 10
PLAYER_RELOAD_BAR_BORDER_COLOR: rgbColor = (64, 64, 64)
PLAYER_RELOAD_BAR_BORDER_THICKNESS: pixels = 8
PLAYER_RELOAD_BAR_CONTENT_COLOR: rgbColor = (255, 0, 0)

INPUT_BULLET_MODEL: ImageFilePath = r"Models/default_bullet.png"
INPUT_BULLET_BASE_ANGLE: angleDeg = 270
INPUT_BULLET_WIDTH: pixels = 25
INPUT_BULLET_HEIGHT: pixels = 50
INPUT_BULLET_SPEED: pixelspersecond = 1000
INPUT_BULLET_SHOT_ANGLE: angleDeg = 90

BLOCK_COLOR = (255, 0, 0)
BLOCK_WIDTH: pixels = 100
BLOCK_HEIGHT: pixels = 100
BLOCK_OFFSET_X: pixels = None
BLOCK_OFFSET_Y: pixels = None
BLOCK_MAX_LINEAR_SPEED: pixels = 0
BLOCK_MAX_ANGULAR_SPEED: int = 0
BRICK_MODEL: Optional[ImageFilePath] = None
GEAR_MODEL: Optional[ImageFilePath] = r"Models/default_killgear.png"
GEAR_SPEED: int = 1

GRID_WIDTH: pixels = BLOCK_WIDTH
GRID_HEIGHT: pixels = BLOCK_HEIGHT
GRID_OFFSET_X: pixels = int((WINDOW_WIDTH - floor_to_nearest(0, WINDOW_WIDTH, BLOCK_WIDTH)) / 2)
GRID_OFFSET_Y: pixels = int((WINDOW_HEIGHT - floor_to_nearest(0, WINDOW_HEIGHT, BLOCK_HEIGHT)) / 2)
GRID_COLOR: rgbColor = (32, 32, 32)

