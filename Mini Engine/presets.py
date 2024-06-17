import classes, config
from classes import *

Dot(scene="""SET TO CURRENT SCENE""", model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
             width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
             x=PLAYER_X, y=PLAYER_Y,
             max_linear_speed=PLAYER_LINEAR_SPEED,
             keybinds=PLAYER_KEYBINDS
             )


Invader(scene="""SET TO CURRENT SCENE""", model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                 width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                 x=PLAYER_X, y=PLAYER_Y,
                 max_linear_speed=PLAYER_LINEAR_SPEED,
                 keybinds=PLAYER_KEYBINDS
                 )


Animal(scene="""SET TO CURRENT SCENE""", model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                x=PLAYER_X, y=PLAYER_Y,
                max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
                keybinds=PLAYER_KEYBINDS
                )


Car(scene="""SET TO CURRENT SCENE""", model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
             width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
             x=PLAYER_X, y=PLAYER_Y,
             max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
             linear_acceleration=PLAYER_LINEAR_ACCELERATION, linear_decceleration=PLAYER_LINEAR_DECCELERATION,
             keybinds=PLAYER_KEYBINDS
             )


IcyCar(scene="""SET TO CURRENT SCENE""", model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                x=PLAYER_X, y=PLAYER_Y,
                max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
                linear_acceleration=PLAYER_LINEAR_ACCELERATION, linear_decceleration=PLAYER_LINEAR_DECCELERATION,
                angular_acceleration=PLAYER_ANGULAR_ACCELERATION, angular_decceleration=PLAYER_ANGULAR_DECCELERATION,
                keybinds=PLAYER_KEYBINDS
                )


SpaceInvader(scene="""SET TO CURRENT SCENE""",
                      facing_angle=PLAYER_FACING_ANGLE,
                      model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                      width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                      x=PLAYER_X, y=PLAYER_Y,
                      max_linear_speed=PLAYER_LINEAR_SPEED,
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


Soldier(scene="""SET TO CURRENT SCENE""",
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