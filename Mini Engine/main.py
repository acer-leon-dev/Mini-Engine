import pygame
import math
from keybinds import Keybinds

from typing import Optional
type ImageFilePath = str # The path to an image file
type miliseconds = float # A period of time in miliseconds
type rgbColor = tuple[int, int, int] # A color in rgb hex format
type pixels = int # An integer representing pixels
type pixelspersecond = int
type angleDeg = float # An angle in degrees
type Object = Object
type BasePlayer = BasePlayer
type Bullet = Bullet
type Block = Block

defaults = {'object_x': 0,
            'object_y': 0,
            'object_color': (255, 0, 0),
            'object_max_lin_spd': 0,
            'object_max_ang_spd': 0,
            'player_color': (255, 0 ,0),
            'player_x': 0,
            'player_y': 0,
            'player_max_lin_spd': 256,
            'player_max_ang_spd': 256,
            'player_lin_acc': 128,
            'player_lin_dacc': None,
            'player_ang_acc': 128,
            'player_ang_dacc': None,
            'keybinds': 'w-a-s-d',
            'bullet_spd': 1000,
            'bullet_width': 25,
            'bullet_height': 25,
            'bullet_color': (255, 0, 0),
            'show_reload': False,
            'rel_t': 500,
            'rel_base_ang': 0,
            'rel_bar_x': 10,
            'rel_bar_y': 10,
            'rel_bar_width': 200,
            'rel_bar_height':50,
            'rel_bar_border_color': (64, 64, 64),
            'rel_bar_border_thickness': 6,
            'rel_bar_content_color': (255, 0, 0),
            'block_color': (255, 0, 0)
}

def floor_to_nearest(offset: float, value: float, step: int) -> int:
    return range(int(offset), math.floor(value), step)[-1]

def limit_degrees(degrees):
    while degrees >= 360:
        degrees -= 360
    while degrees <= 0:
        degrees += 360
    return degrees

def exceeds_window(object: Object) -> bool:
    pass

def when_player_hit(player: BasePlayer):
    player.x = WINDOW_WIDTH/2
    player.y = WINDOW_HEIGHT/2
    player.current_linear_speed = 0
    player.current_angular_speed = 0

def draw_grid(screen: pygame.display, width: pixels, height: pixels,
              offset_x=0, offset_y=0, color: rgbColor=(32, 32, 32)):
    for x in range( offset_x, WINDOW_WIDTH, width):
        pygame.draw.line(screen, color, (x, 0), (x, WINDOW_HEIGHT), 2)
    for y in range( offset_y, WINDOW_HEIGHT, height):
        pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y), 2)

def draw_stored_bullets(screen: pygame.display, bullet_store: list[Bullet]):
    for bullet in bullet_store:
        bullet.draw(screen)
        # Check if bullet exceeeds bounds of window.
        if not (-(bullet.width + 10) < bullet.x < WINDOW_WIDTH + (bullet.width + 10) and
                -(bullet.height + 10) < bullet.y < WINDOW_HEIGHT + (bullet.height + 10)):
            bullet_store.remove(bullet)

def create_brick(model: ImageFilePath, width: pixels, height: pixels,
                          offset_x: pixels, offset_y: pixels,
                          max_linear_speed: int = 0, max_angular_speed: int = 0):
    if not any(block.model_rect.collidepoint(mouse.get_pos()) for block in stored_blocks):
        try:
            stored_blocks.append(
                Brick(model=model, base_angle=0,
                      width=width, height=height,
                      x=floor_to_nearest(offset_x - width, mouse.get_pos()[0], width) + (width/2),
                      y=floor_to_nearest(offset_y - height, mouse.get_pos()[1], height) + (height/2)
                      )
            )
        except IndexError: pass

def create_gear(model: ImageFilePath, width: pixels, height: pixels,
                          offset_x: pixels, offset_y: pixels,
                          max_linear_speed: int = 0, max_angular_speed: angleDeg = 0):
    if not any(block.model_rect.collidepoint(mouse.get_pos()) for block in stored_blocks):
        try:
            stored_blocks.append(
                Gear(model=model, base_angle=0,
                      width=width, height=height,
                      x=floor_to_nearest(offset_x - width, mouse.get_pos()[0], width) + (width/2),
                      y=floor_to_nearest(offset_y - height, mouse.get_pos()[1], height) + (height/2),
                      max_angular_speed=max_angular_speed
                      )
            )
        except IndexError: pass

def draw_stored_blocks(screen: pygame.display, block_store: list[Block]):
    for block in block_store:
        block.draw(screen)
        player.hit(block, lambda: when_player_hit(player))

def check_bullet_block_collision(bullet_store: list[Bullet], block_store: list[Block]):
    for bullet in bullet_store:
        # Check for collision with player.
        if bullet.kills_players:
            player.hit(bullet, lambda: when_player_hit(player))
        # Check for collision with blocks.
        for block in block_store:
            if bullet.hit(block):
                # try: bullet_store.remove(bullet)
                # except: pass
                try: block_store.remove(block)
                except ValueError: pass

def shoot_from_mouse(event: pygame.event):
        stored_bullets.append(
            Bullet(kills_players=True, bullet_angle=INPUT_BULLET_SHOT_ANGLE,
                   model=INPUT_BULLET_MODEL,
                   base_angle=INPUT_BULLET_BASE_ANGLE,
                   width=INPUT_BULLET_WIDTH, height=INPUT_BULLET_HEIGHT,
                   x=event.pos[0], y=event.pos[1],
                   max_linear_speed=INPUT_BULLET_SPEED
                   )
        )

# Blueprint for basic entities.
class Object:
    def __init__(self, model, base_angle, width, height,
                 color=defaults['object_color'],
                 x=defaults['object_x'], y=defaults['object_y'],
                 max_linear_speed=defaults['object_max_lin_spd'],
                 max_angular_speed=defaults['object_max_ang_spd']):

        # POSITION AND SHAPE
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.base_angle = base_angle
        # MOVEMENT
        self.max_linear_speed = max_linear_speed
        self.max_angular_speed = max_angular_speed

        self.current_linear_speed = 0
        self.current_angular_speed = 0
        self.current_angle = 0

        # APPEARANCE (model) AND HITBOX (mask)
        if model != None:
            self.original_model = pygame.image.load(model)
        else:
            self.original_model = pygame.surface.Surface((width, height))
            self.original_model.fill(color)
        self.scaled_model = pygame.transform.scale(self.original_model, (self.width, self.height))
        self.prime_model = pygame.transform.rotate(self.scaled_model, self.base_angle)
        self.model_rect = self.prime_model.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.prime_model)

    def draw(self, surface):
        self.pre_draw_self(surface)

        self.prime_model = pygame.transform.rotate(self.scaled_model, self.base_angle + self.current_angle)
        self.model_rect = self.prime_model.get_rect(center=(self.x, self.y))
        surface.blit(self.prime_model, self.model_rect)
        self.mask = pygame.mask.from_surface(self.prime_model)

        self.post_draw_self(surface)

    def pre_draw_self(self, surface):
        self.movement()

    def post_draw_self(self, surface):
        pass

    def movement(self):
        self.current_angle += self.current_angular_speed
        self.current_angle = limit_degrees(self.current_angle)
        self.x += self.current_linear_speed * math.cos(math.radians(self.current_angle)) * dt
        self.y -= self.current_linear_speed * math.sin(math.radians(self.current_angle)) * dt

    def hit(self, object, function=None):
        if self.mask.overlap(object.mask, (object.model_rect[0] - self.model_rect[0], object.model_rect[1] - self.model_rect[1])):
            try:
                function()
            except TypeError:
                pass
            return True

class Brick(Object):
    def __init__(self, model, base_angle, width, height,
                 color=defaults['block_color'],
                 x=0, y=0):
        super().__init__(model, base_angle, width, height,
                         color, x, y)

class Gear(Object):
    def __init__(self, model, base_angle, width, height,max_angular_speed=128,
                 color=defaults['block_color'],
                 x=0, y=0, ):
        super().__init__(model, base_angle, width, height,
                         color, x, y, max_angular_speed=max_angular_speed)
        self.current_angular_speed = self.max_angular_speed

class Bullet(Object):
    def __init__(self, kills_players, base_angle, bullet_angle, model,
                 width, height, color=defaults['bullet_color'],
                 x=0, y=0, max_linear_speed=500):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed)

        self.max_linear_speed = max_linear_speed
        self.base_angle = base_angle
        self.current_angle = bullet_angle

        self.kills_players = kills_players

        self.current_linear_speed = max_linear_speed

# Blueprint for UI objects.
class UIFeature():
    def __init__(self, width, height, x=0, y=0, base_angle=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.base_angle = base_angle

        self.original_model = pygame.Surface((self.width, self.height))
        self.prime_model = pygame.transform.rotate(self.original_model, self.base_angle)
        self.model_rect = self.prime_model.get_rect(topleft=(self.x, self.y))

        self.current_angle = 0

    def draw(self, surface):
        self.pre_draw_self(surface)

        self.prime_model = pygame.transform.rotate(self.prime_model, self.current_angle + self.base_angle)
        self.model_rect = self.prime_model.get_rect(topleft=(self.x, self.y))
        surface.blit(self.prime_model, self.model_rect)

        self.post_draw_self(surface)

    def pre_draw_self(self, surface):
        self.update()

    def post_draw_self(self, surface):
        pass

    def update(self):
        pass

# Displays reloading time for a given player with shooting abilities.
class ReloadBar(UIFeature):
    def __init__(self, width, height, player,
                 x=defaults['rel_bar_x'], y=defaults['rel_bar_y'], base_angle=0,
                 border_color=defaults['rel_bar_border_color'],
                 border_thickness=defaults['rel_bar_border_thickness'],
                 content_color=defaults['rel_bar_content_color']
                 ):
        super().__init__(width, height, x, y, base_angle)

        self.prime_model.set_colorkey((1, 1, 1))

        # APPEARANCE
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.content_color = content_color
        self.player = player

        self.content_percent = 0

    def pre_draw_self(self, surface):
        self.prime_model.fill((1, 1, 1))

        self.update()
        pygame.draw.rect(self.prime_model, self.content_color, (0, 0,
                                                                self.content_percent * self.width,
                                                                self.height))

        pygame.draw.lines(self.prime_model, self.border_color, True,
                          ((0, 0), (self.width, 0), (self.width, self.height), (0, self.height)),
                          self.border_thickness)

    def update(self):
        if self.player.reloading:
            if self.content_percent >= 1:
                self.content_percent = 0
            if self.content_percent < 1:
                self.content_percent += dt / (self.player.reload_time / 1000)
            else:
                self.content_percent = 1
        else:
            self.content_percent = 1

# Blueprint for player objects.
class BasePlayer(Object):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'],
                 max_angular_speed=defaults['player_max_ang_spd'],
                 linear_acceleration=defaults['player_lin_acc'],
                 linear_decceleration=defaults['player_lin_dacc'],
                 angular_acceleration=defaults['player_ang_acc'],
                 angular_decceleration=defaults['player_ang_dacc'],
                 keybinds=defaults['keybinds']):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, max_angular_speed
                         )
        # MOVEMENT
        self.linear_acceleration = linear_acceleration
        self.linear_decceleration = linear_decceleration if linear_decceleration != None else \
            linear_acceleration

        self.angular_acceleration = angular_acceleration
        self.angular_decceleration = angular_decceleration if angular_decceleration != None else \
            angular_acceleration
        # KEYBINDS
        self.keys = Keybinds.split_binds(keybinds)
        # SHOOTING
        self.can_shoot = False

# Moves up, down, left and right; turns instantly in accordance with movement.
class Dot(BasePlayer):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], keybinds='w-a-s-d'):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, keybinds)

        self.current_speed_y = 0
        self.current_speed_x = 0

    def pre_draw_self(self, screen):
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            self.current_speed_x = -self.max_linear_speed
        if keys[self.keys['right']]:
            self.current_speed_x = self.max_linear_speed
        if keys[self.keys['left']] and keys[self.keys['right']]:
            self.current_speed_x = 0
        if not keys[self.keys['left']] and not keys[self.keys['right']]:
            self.current_speed_x = 0

        if keys[self.keys['forward']]:
            self.current_speed_y = -self.max_linear_speed
        if keys[self.keys['backward']]:
            self.current_speed_y = self.max_linear_speed
        if keys[self.keys['forward']] and keys[self.keys['backward']]:
            self.current_speed_y = 0
        if not keys[self.keys['forward']] and not keys[self.keys['backward']]:
            self.current_speed_y = 0
        if self.current_speed_x > 0:
            self.current_angle = 270
        if self.current_speed_x < 0:
            self.current_angle = 90
        if self.current_speed_y > 0:
            self.current_angle = 180
        if self.current_speed_y < 0:
            self.current_angle = 0
        if self.current_speed_x < 0 and self.current_speed_y < 0:
            self.current_angle = (90 + 0) / 2
        if self.current_speed_x < 0 and self.current_speed_y > 0:
            self.current_angle = (90 + 180) / 2
        if self.current_speed_x > 0 and self.current_speed_y < 0:
            self.current_angle = (270 + 360) / 2
        if self.current_speed_x > 0 and self.current_speed_y > 0:
            self.current_angle = (270 + 180) / 2

        self.x += self.current_speed_x * dt
        self.y += self.current_speed_y * dt

# Moves up, down, left and right; never turns around.
class Invader(BasePlayer):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], keybinds='w-a-s-d'):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, keybinds)

        self.current_speed_y = 0
        self.current_speed_x = 0

    def pre_draw_self(self, screen):
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            self.current_speed_x = -self.max_linear_speed
        if keys[self.keys['right']]:
            self.current_speed_x = self.max_linear_speed
        if keys[self.keys['left']] and keys[self.keys['right']]:
            self.current_speed_x = 0
        if not keys[self.keys['left']] and not keys[self.keys['right']]:
            self.current_speed_x = 0

        if keys[self.keys['forward']]:
            self.current_speed_y = -self.max_linear_speed
        if keys[self.keys['backward']]:
            self.current_speed_y = self.max_linear_speed
        if keys[self.keys['forward']] and keys[self.keys['backward']]:
            self.current_speed_y = 0
        if not keys[self.keys['forward']] and not keys[self.keys['backward']]:
            self.current_speed_y = 0

        self.x += self.current_speed_x * dt
        self.y += self.current_speed_y * dt

# Moves forward and backward; turns left and right.
class Animal(BasePlayer):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], max_angular_speed=defaults['player_max_ang_spd'],
                 keybinds='w-a-s-d'):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, max_angular_speed,
                         keybinds)

    def pre_draw_self(self, screen):
        self.update()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            self.current_angle += self.max_angular_speed * dt
        if keys[self.keys['right']]:
            self.current_angle -= self.max_angular_speed * dt

        if keys[self.keys['forward']]:
            self.current_linear_speed = self.max_linear_speed
        elif keys[self.keys['backward']]:
            self.current_linear_speed = -self.max_linear_speed
        else:
            self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * dt

# Moves forward and backward; turns left and right with acceleration.
class Car(BasePlayer):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], max_angular_speed=defaults['player_max_ang_spd'],
                 linear_acceleration=defaults['player_lin_acc'], linear_decceleration=defaults['player_lin_dacc'],
                 keybinds='w-a-s-d'):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, max_angular_speed,
                         linear_acceleration, linear_decceleration,
                         keybinds)
    def pre_draw_self(self, screen):
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            self.current_angle += self.max_angular_speed * dt
        if keys[self.keys['right']]:
            self.current_angle -= self.max_angular_speed * dt


        if keys[self.keys['forward']]:
            if self.current_linear_speed < self.max_linear_speed:
                self.current_linear_speed += self.linear_acceleration * dt
        elif keys[self.keys['backward']]:
            if self.current_linear_speed > -self.max_linear_speed:
                self.current_linear_speed -= self.linear_acceleration * dt
        else:
            if self.current_linear_speed > 10:
                self.current_linear_speed -= self.linear_decceleration * dt
            elif self.current_linear_speed < -10:
                self.current_linear_speed += self.linear_decceleration * dt
            elif -10 <= self.current_linear_speed <= 10:
                self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * dt

# Moves forward and backward with acceleration; turns left and right with acceleration.
class IcyCar(BasePlayer):
    def __init__(self, model, base_angle, width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], max_angular_speed=defaults['player_max_ang_spd'],
                 linear_acceleration=defaults['player_lin_acc'], linear_decceleration=defaults['player_lin_dacc'],
                 angular_acceleration=defaults['player_ang_acc'], angular_decceleration=defaults['player_ang_dacc'],
                 keybinds='w-a-s-d'
                 ):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, max_angular_speed,
                         linear_acceleration, linear_decceleration,
                         angular_acceleration, angular_decceleration,
                         keybinds)

    def pre_draw_self(self, screen):
        self.movement()

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            if self.current_angular_speed < self.max_angular_speed:
                self.current_angular_speed += self.angular_acceleration * dt
        elif keys[self.keys['right']]:
            if self.current_angular_speed > -self.max_angular_speed:
                self.current_angular_speed -= self.angular_acceleration * dt
        else:
            if self.current_angular_speed > 10:
                self.current_angular_speed -= self.angular_decceleration * dt
            elif self.current_angular_speed < -10:
                self.current_angular_speed += self.angular_decceleration * dt
            elif -10 <= self.current_angular_speed <= 10:
                self.current_angular_speed = 0

        self.current_angle += self.current_angular_speed * dt

        if keys[self.keys['forward']]:
            if self.current_linear_speed < self.max_linear_speed:
                self.current_linear_speed += self.linear_acceleration * dt
        elif keys[self.keys['backward']]:
            if self.current_linear_speed > -self.max_linear_speed:
                self.current_linear_speed -= self.linear_acceleration * dt
        else:
            if self.current_linear_speed > 10:
                self.current_linear_speed -= self.linear_decceleration * dt
            elif self.current_linear_speed < -10:
                self.current_linear_speed += self.linear_decceleration * dt
            elif -10 <= self.current_linear_speed <= 10:
                self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * dt

# Can shoot. Inherits movement of Invader.
class SpaceInvader(Invader):
    def __init__(self, model, base_angle, bullet_model, bullet_base_angle, bullet_store, facing_angle,
                 width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], keybinds='w-a-s-d',
                 bullet_speed=defaults['bullet_spd'],
                 bullet_width=defaults['bullet_width'],
                 bullet_height=defaults['bullet_height'],
                 reload_time=defaults['rel_t'],
                 reload_bar_base_angle=defaults['rel_base_ang'],
                 show_reload_bar=defaults['show_reload'],
                 reload_bar_x=defaults['rel_bar_x'], reload_bar_y=defaults['rel_bar_y'],
                 reload_bar_width=defaults['rel_bar_width'], reload_bar_height=defaults['rel_bar_height'],
                 reload_bar_border_color=defaults['rel_bar_border_color'],
                 reload_bar_border_thickness=defaults['rel_bar_border_thickness'],
                 reload_bar_content_color=defaults['rel_bar_content_color']
                ):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, keybinds)

        self.current_angle = facing_angle
        self.can_shoot = True
        self.bullet_model = bullet_model
        self.bullet_base_angle = bullet_base_angle
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.bullet_speed = bullet_speed
        self.bullet_store = bullet_store
        self.reload_time = reload_time
        self.show_reload_bar = show_reload_bar
        self.reload_bar = ReloadBar(player=self,
                                    base_angle=reload_bar_base_angle,
                                    x=reload_bar_x,
                                    y=reload_bar_y,
                                    width=reload_bar_width,
                                    height=reload_bar_height,
                                    border_color=reload_bar_border_color,
                                    border_thickness=reload_bar_border_thickness,
                                    content_color=reload_bar_content_color)

        self.shooting = False
        self.reloading = False
        self.reload_event = pygame.event.custom_type()

    def pre_draw_self(self, surface):
        self.movement()
        self.shoot()

    def post_draw_self(self, surface):
        if self.show_reload_bar:
            self.reload_bar.draw(surface)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']]:
            self.current_speed_x = -self.max_linear_speed
        if keys[self.keys['right']]:
            self.current_speed_x = self.max_linear_speed
        if keys[self.keys['left']] and keys[self.keys['right']]:
            self.current_speed_x = 0
        if not keys[self.keys['left']] and not keys[self.keys['right']]:
            self.current_speed_x = 0

        if keys[self.keys['forward']]:
            self.current_speed_y = -self.max_linear_speed
        if keys[self.keys['backward']]:
            self.current_speed_y = self.max_linear_speed
        if keys[self.keys['forward']] and keys[self.keys['backward']]:
            self.current_speed_y = 0
        if not keys[self.keys['forward']] and not keys[self.keys['backward']]:
            self.current_speed_y = 0

        self.x += self.current_speed_x * dt
        self.y += self.current_speed_y * dt

    def shoot(self):
        if self.shooting:
            if not self.reloading:
                self.bullet_store.append(
                    Bullet(kills_players=False,
                           width=self.bullet_width, height=self.bullet_height,
                           base_angle=self.bullet_base_angle,
                           x = self.x + 20*math.cos(math.radians(self.current_angle)),
                           y = self.y - 20*math.sin(math.radians(self.current_angle)),
                           max_linear_speed=self.bullet_speed,
                           bullet_angle=self.current_angle,
                           model=self.bullet_model)
                )
                self.reloading = True
                pygame.time.set_timer(self.reload_event, self.reload_time)

    def update_weapon_status(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shooting = True
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                event.type == pygame.WINDOWLEAVE or \
                not (-1 < mouse.get_pos()[0] < WINDOW_WIDTH + 1 and
                     -1 < mouse.get_pos()[1] < WINDOW_HEIGHT + 1):
            player.shooting = False

        # For reloading weapons.
        if event.type == player.reload_event:
            player.reloading = False
            pygame.time.set_timer(player.reload_event, 0)

# Can shoot. Inherits movement of Soldier.
class Soldier(Animal):
    def __init__(self, model, base_angle, bullet_model, bullet_base_angle, bullet_store,
                 width, height, color=defaults['player_color'],
                 x=defaults['player_x'], y=defaults['player_y'],
                 max_linear_speed=defaults['player_max_lin_spd'], max_angular_speed=defaults['player_max_ang_spd'],
                 keybinds='w-a-s-d',
                 bullet_speed=defaults['bullet_spd'],
                 bullet_width=defaults['bullet_width'],
                 bullet_height=defaults['bullet_height'],
                 reload_time=defaults['rel_t'],
                 show_reload_bar=defaults['show_reload'],
                 reload_bar_x=defaults['rel_bar_x'], reload_bar_y=defaults['rel_bar_y'],
                 reload_bar_width=defaults['rel_bar_width'], reload_bar_height=defaults['rel_bar_height'],
                 reload_bar_border_color=defaults['rel_bar_border_color'],
                 reload_bar_border_thickness=defaults['rel_bar_border_thickness'],
                 reload_bar_content_color=defaults['rel_bar_content_color']
                 ):
        super().__init__(model, base_angle, width, height, color, x, y,
                         max_linear_speed, max_angular_speed,
                         keybinds)

        self.can_shoot = True
        self.bullet_model = bullet_model
        self.bullet_base_angle = bullet_base_angle
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.bullet_speed = bullet_speed
        self.bullet_store = bullet_store
        self.reload_time = reload_time
        self.show_reload_bar = show_reload_bar
        self.reload_bar = ReloadBar(player=self,
                                    base_angle=0,
                                    x=reload_bar_x,
                                    y=reload_bar_y,
                                    width=reload_bar_width,
                                    height=reload_bar_height,
                                    border_color=reload_bar_border_color,
                                    border_thickness=reload_bar_border_thickness,
                                    content_color=reload_bar_content_color)

        self.shooting = False
        self.reloading = False
        self.reload_event = pygame.event.custom_type()

    def pre_draw_self(self, surface):
        self.movement()
        self.shoot()

    def post_draw_self(self, surface):
        if self.show_reload_bar:
            self.reload_bar.draw(surface)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[self.keys['left']] and keys[self.keys['right']]:
            self.current_angular_speed = 0
        elif keys[self.keys['left']]:
            self.current_angular_speed = self.max_angular_speed
        elif keys[self.keys['right']]:
            self.current_angular_speed = -self.max_angular_speed
        else:
            self.current_angular_speed = 0
        if keys[self.keys['forward']] and keys[self.keys['backward']]:
            self.current_linear_speed = 0
        elif keys[self.keys['forward']]:
            self.current_linear_speed = self.max_linear_speed
        elif keys[self.keys['backward']]:
            self.current_linear_speed = -self.max_linear_speed
        else:
            self.current_linear_speed = 0

        self.current_angle += self.current_angular_speed * dt

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * dt

    def shoot(self):
        if self.shooting:
            if not self.reloading:
                self.bullet_store.append(
                    Bullet(kills_players=False,
                           width=self.bullet_width, height=self.bullet_height,
                           base_angle=self.bullet_base_angle,
                           x=self.x + 20 * math.cos(math.radians(self.current_angle)),
                           y=self.y - 20 * math.sin(math.radians(self.current_angle)),
                           max_linear_speed=self.bullet_speed,
                           bullet_angle=self.current_angle,
                           model=self.bullet_model)
                )
                self.reloading = True
                pygame.time.set_timer(self.reload_event, self.reload_time)

    def update_weapon_status(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shooting = True
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                event.type == pygame.WINDOWLEAVE or \
                not (-1 < mouse.get_pos()[0] < WINDOW_WIDTH + 1 and
                     -1 < mouse.get_pos()[1] < WINDOW_HEIGHT + 1):
            player.shooting = False

        # For reloading weapons.
        if event.type == player.reload_event:
            player.reloading = False
            pygame.time.set_timer(player.reload_event, 0)

#################################################
# CUSTOMIZATION
WINDOW_WIDTH: pixels = 1280
WINDOW_HEIGHT: pixels = 720
GAME_FPS = 120

# CUSTOMIZATION: User can change the following values to customize attributes
PLAYER_MODEL: ImageFilePath = r"Models/default_triangle player.png"
PLAYER_MODEL_BASE_ANGLE: angleDeg = 0
PLAYER_WIDTH: pixels = 50
PLAYER_HEIGHT: pixels = 50
PLAYER_X: pixels = WINDOW_WIDTH/2
PLAYER_Y: pixels = WINDOW_HEIGHT/2
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
INPUT_BULLET_SPEED: pixelspersecond = 0
INPUT_BULLET_SHOT_ANGLE: angleDeg = 90

BLOCK_COLOR = (255, 0, 0)
BLOCK_WIDTH: pixels = 100
BLOCK_HEIGHT: pixels = 100
BLOCK_OFFSET_X: pixels = None
BLOCK_OFFSET_Y: pixels = None
BLOCK_MAX_LINEAR_SPEED: pixels = 0
BLOCK_MAX_ANGULAR_SPEED: int = 0
BRICK_MODEL: Optional[ImageFilePath] =  None
GEAR_MODEL: Optional[ImageFilePath] =  r"Models/default_killgear.png"
GEAR_SPEED: int = 1

GRID_WIDTH: pixels = BLOCK_WIDTH
GRID_HEIGHT: pixels = BLOCK_HEIGHT
GRID_OFFSET_X: pixels = int((WINDOW_WIDTH - floor_to_nearest(0, WINDOW_WIDTH, BLOCK_WIDTH))/2)
GRID_OFFSET_Y: pixels = int((WINDOW_HEIGHT - floor_to_nearest(0, WINDOW_HEIGHT, BLOCK_HEIGHT))/2)
GRID_COLOR: rgbColor = (32, 32, 32)


#################################################

# IGNORE: To to prevent bugs
player = BasePlayer(PLAYER_MODEL, PLAYER_MODEL_BASE_ANGLE, PLAYER_WIDTH, PLAYER_HEIGHT)
# Create the bullet and block stores. Necessary for creating bullets and blocks.
stored_bullets = []
stored_blocks = []

# Player presets. Uncomment player to use it.

player = Dot(model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
             width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
             x=PLAYER_X, y=PLAYER_Y,
             max_linear_speed=PLAYER_LINEAR_SPEED,
             keybinds=PLAYER_KEYBINDS)
"""
player = Invader(model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                 width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                 x=PLAYER_X, y=PLAYER_Y,
                 max_linear_speed=PLAYER_LINEAR_SPEED,
                 keybinds=PLAYER_KEYBINDS)

player = Animal(model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                x=PLAYER_X, y=PLAYER_Y,
                max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
                keybinds=PLAYER_KEYBINDS)

player = Car(model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
             width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
             x=PLAYER_X, y=PLAYER_Y,
             max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
             linear_acceleration=PLAYER_LINEAR_ACCELERATION, linear_decceleration=PLAYER_LINEAR_DECCELERATION,
             keybinds=PLAYER_KEYBINDS
            )
            
player = IcyCar(model=PLAYER_MODEL, base_angle=PLAYER_MODEL_BASE_ANGLE,
                width=PLAYER_WIDTH, height=PLAYER_HEIGHT,
                x=PLAYER_X, y=PLAYER_Y,
                max_linear_speed=PLAYER_LINEAR_SPEED, max_angular_speed=PLAYER_ANGULAR_SPEED,
                linear_acceleration=PLAYER_LINEAR_ACCELERATION, linear_decceleration=PLAYER_LINEAR_DECCELERATION,
                angular_acceleration=PLAYER_ANGULAR_ACCELERATION, angular_decceleration=PLAYER_ANGULAR_DECCELERATION,
                keybinds=PLAYER_KEYBINDS
                )
                
player = SpaceInvader(bullet_store=stored_bullets, facing_angle=PLAYER_FACING_ANGLE,
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

player = Soldier(bullet_store=stored_bullets,
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
"""

if __name__ == "__main__":

    # Initialize the library
    pygame.init()
    # Create window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    mouse = pygame.mouse
    mouse.set_visible(True)
    # Create delta time
    clock = pygame.time.Clock(); dt = 0

    running = True
    while running:
        # Poll for pygame events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Fire a bullet when left mouse button is clicked.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                shoot_from_mouse(event)

            if player.can_shoot:
                player.update_weapon_status(event)

        # Poll for key and mouse events.
        keys = pygame.key.get_pressed()

        # Create a new block when the "1" key is pressed.
        if keys[pygame.K_1]:
            create_brick(BRICK_MODEL, BLOCK_WIDTH, BLOCK_HEIGHT,
                                  offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y)

        # Create a new gear when the "2" key is pressed.
        if keys[pygame.K_2]:
            create_gear(GEAR_MODEL, BLOCK_WIDTH, BLOCK_HEIGHT,
                         offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y,
                         max_angular_speed=GEAR_SPEED)

        ################################################# Render game below

        # Refresh the window
        window.fill((0,0,0))

        # Create a 100x100 grid
        draw_grid(window, GRID_WIDTH, GRID_HEIGHT,
                  offset_x=GRID_OFFSET_X, offset_y=GRID_OFFSET_Y, color=GRID_COLOR)

        # Draw bullets in the bullet store
        draw_stored_bullets(window, stored_bullets)
        # Draw blocks in the block store
        draw_stored_blocks(window, stored_blocks)

        # Check for collision between bullets and blocks
        check_bullet_block_collision(bullet_store=stored_bullets, block_store=stored_blocks)

        # Draw the player
        player.draw(window)

        # flip() the display to project render
        pygame.display.flip()

        # limit FPS and calculate delta value
        dt = clock.tick(GAME_FPS) / 1000

    pygame.quit()