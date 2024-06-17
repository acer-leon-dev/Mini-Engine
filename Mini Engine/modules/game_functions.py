import pygame, math
from classes import *

def object_exceeds_window_bounds(object: obj) -> bool:
    return not (-(object.width + 10) < object.x < WINDOW_WIDTH + (object.width + 10) and
                -(object.height + 10) < object.y < WINDOW_HEIGHT + (object.height + 10))


def when_player_hit(player: obj) -> None:
    player.x = WINDOW_WIDTH / 2
    player.y = WINDOW_HEIGHT / 2
    player.current_linear_speed = 0
    player.current_angular_speed = 0


def draw_grid(screen: pygame.display, width: pixels, height: pixels,
              offset_x: pixels=0, offset_y: pixels=0,
              color: rgbColor = (32, 32, 32), thickness: pixels=2) -> None:
    for x in range(offset_x, WINDOW_WIDTH, width):
        pygame.draw.line(screen, color, (x, 0), (x, WINDOW_HEIGHT), thickness)
    for y in range(offset_y, WINDOW_HEIGHT, height):
        pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y), thickness)


def draw_stored_bullets(screen: pygame.display, bullet_store: list[obj]) -> None:
    for bullet in bullet_store:
        bullet.draw(screen)
        # Check if bullet exceeeds bounds of window.
        if object_exceeds_window_bounds(bullet):
            bullet_store.remove(bullet)


def create_brick(block_store: list, model: ImageFilePath, width: pixels, height: pixels,
                 offset_x: pixels, offset_y: pixels,
                 max_linear_speed: int = 0, max_angular_speed: int = 0) -> None:
    if not any(block.model_rect.collidepoint(MOUSE.get_pos()) for block in block_store):
        try:
            block_store.append(
                Brick(model=model, base_angle=0,
                      width=width, height=height,
                      x=floor_to_nearest(offset_x - width, MOUSE.get_pos()[0], width) + (width / 2),
                      y=floor_to_nearest(offset_y - height, MOUSE.get_pos()[1], height) + (height / 2)
                      )
            )
        except IndexError: pass


def create_gear(block_store: list, model: ImageFilePath, width: pixels, height: pixels,
                offset_x: pixels, offset_y: pixels,
                max_linear_speed: int = 0, max_angular_speed: angleDeg = 0) -> None:
    if not any(block.model_rect.collidepoint(MOUSE.get_pos()) for block in block_store):
        try: block_store.append(Gear(model=model, base_angle=0,
                                width=width, height=height,
                                x=floor_to_nearest(offset_x - width, MOUSE.get_pos()[0], width) + (width / 2),
                                y=floor_to_nearest(offset_y - height, MOUSE.get_pos()[1], height) + (height / 2),
                                max_angular_speed=max_angular_speed
                                    )
                                )
        except IndexError: pass


def draw_stored_blocks(screen: pygame.display, block_store: list[obj], player: obj) -> None:
    for block in block_store:
        block.draw(screen)
        player.hit(block, lambda: when_player_hit(player))


def check_bullet_block_collision(player: obj,
                                 bullet_store: list[obj], block_store: list[obj]) -> None:
    for bullet in bullet_store:
        # Check for collision with player.
        if bullet.kills_players: player.hit(bullet, lambda: when_player_hit(player))
        # Check for collision with blocks.
        for block in block_store:
            if bullet.hit(block):
                # Delete the bullet upon hit
                # try: bullet_store.remove(bullet)
                # except: pass
                try:
                    block_store.remove(block)
                except ValueError:
                    pass


def shoot_from_mouse(event: pygame.event, bullet_store: list[obj]) -> None:
    bullet_store.append(
        Bullet(kills_players=True, bullet_angle=INPUT_BULLET_SHOT_ANGLE,
               model=INPUT_BULLET_MODEL,
               base_angle=INPUT_BULLET_BASE_ANGLE,
               width=INPUT_BULLET_WIDTH, height=INPUT_BULLET_HEIGHT,
               x=event.pos[0], y=event.pos[1],
               max_linear_speed=INPUT_BULLET_SPEED
               )
    )