import pygame, math, config
from pygame import Color
from modules.game_functions import *
from modules.keys_list import Keybinds
from scenes import *

#################################################



game = Game()

PLAYER = Soldier(scene=game,
                 model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                 width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                 x=PLAYER_X, y=PLAYER_Y,
                 max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
                 keybinds=PLAYER_KEYBINDS,
                 bullet_model=PLAYER_BULLET_MODEL,
                 bullet_base_angle=PLAYER_BULLET_BASE_ANGLE,
                 bullet_speed=PLAYER_BULLET_SPEED,
                 bullet_width=PLAYER_BULLET_WIDTH, bullet_height=PLAYER_BULLET_HEIGHT,
                 reload_time=PLAYER_BULLET_RELOAD_TIME,
                 show_reload_bar=PLAYER_SHOW_RELOAD_BAR,
                 reload_bar_x=PLAYER_RELOAD_BAR_X, reload_bar_y=PLAYER_RELOAD_BAR_Y,
                 reload_bar_width=PLAYER_RELOAD_BAR_WIDTH, reload_bar_height=PLAYER_RELOAD_BAR_HEIGHT,
                 reload_bar_border_color=PLAYER_RELOAD_BAR_BORDER_COLOR,
                 reload_bar_border_thickness=PLAYER_RELOAD_BAR_BORDER_THICKNESS,
                 reload_bar_content_color=PLAYER_RELOAD_BAR_CONTENT_COLOR
                 )

if __name__ == "__main__":
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.WINDOWSHOWN:
                game.loaded = True
            ################################################# Create events for each scene
            if game.loaded:
                # Fire a bullet when left mouse button is clicked.
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    shoot_from_mouse(event, game.bullet_store)

                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                        game.menubutton.model_rect.collidepoint(MOUSE.get_pos()[0], MOUSE.get_pos()[1])):
                    game.unload_scene()

                if game.player.can_shoot:
                    game.player.update_weapon_status(event)

        ################################################# Render scenes below

        if game.loaded:
            game.play_scene(PLAYER)
        else:
            WINDOW.fill((0,0,0))
        #####################################################################

        # flip() the display to project render
        pygame.display.flip()

        # limit FPS and calculate delta value
        config.dt = classes.dt = clock.tick(GAME_FPS) / 1000

    pygame.quit()
