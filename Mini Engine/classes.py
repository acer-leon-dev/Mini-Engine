import pygame, math, config
from config import *
from modules.keys_list import Keybinds
from modules.game_functions import *


####################### DEFAULT VALUES ##########################   w
defaults = {'object_x': 0,
            'object_y': 0,
            'object_color': pygame.color.Color(255, 0, 0),
            'object_max_lin_spd': 0,
            'object_max_ang_spd': 0,
            'player_color': pygame.color.Color(255, 0, 0),
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
            'bullet_color': pygame.color.Color(255, 0, 0),
            'show_reload': False,
            'rel_t': 500,
            'rel_base_ang': 0,
            'rel_bar_x': 10,
            'rel_bar_y': 10,
            'rel_bar_width': 200,
            'rel_bar_height': 50,
            'rel_bar_border_color': pygame.color.Color(64, 64, 64),
            'rel_bar_border_thickness': 6,
            'rel_bar_content_color': pygame.color.Color(255, 0, 0),
            'block_color': pygame.color.Color(255, 0, 0),
            'font': r"fonts/Tw Cen MT Regular.TTF"
}

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
            self.original_model = pygame.image.load(model).convert_alpha()
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
        self.x += self.current_linear_speed * math.cos(math.radians(self.current_angle)) * config.dt
        self.y -= self.current_linear_speed * math.sin(math.radians(self.current_angle)) * config.dt

    def hit(self, object, function=None):
        if self.mask.overlap(object.mask,
                             (object.model_rect[0] - self.model_rect[0], object.model_rect[1] - self.model_rect[1])):
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
    def __init__(self, model, base_angle, width, height, max_angular_speed=128,
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
class Button(UIFeature):
    def __init__(self, width, height,
                 x=defaults['rel_bar_x'], y=defaults['rel_bar_y'], base_angle=0,
                 border_color=defaults['rel_bar_border_color'],
                 border_thickness=defaults['rel_bar_border_thickness'],
                 content_color=defaults['rel_bar_content_color'],
                 text=None, font=defaults['font'], text_color=(255, 255, 255),
                 function=None):
        super().__init__(width, height, x, y, base_angle)

        self.prime_model.set_colorkey((1, 1, 1))

        # APPEARANCE
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.content_color = content_color

        self.temp_content_color = self.content_color
        self.temp_border_color = self.border_color

        self.font = pygame.font.Font(font, 32)
        self.text = self.font.render(text, True, text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.width/2, self.height/2)



    def pre_draw_self(self, surface):
        self.prime_model.fill((1, 1, 1))
        self.update()
        self.prime_model.fill(self.temp_content_color)
        self.prime_model.blit(self.text, self.text_rect)
        pygame.draw.lines(self.prime_model, self.border_color, True,
                          ((0, 0), (self.width, 0), (self.width, self.height), (0, self.height)),
                          self.border_thickness)
    def update(self):
        if self.model_rect.collidepoint(MOUSE.get_pos()[0], MOUSE.get_pos()[1]):
            self.temp_content_color = self.content_color - pygame.color.Color(50, 50, 50)
            self.temp_border_color = self.border_color - pygame.color.Color(30, 30, 30)
        else:
            self.temp_content_color = self.content_color

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
        self.prime_model.fill(self.content_color, ( (0, 0),
                                                         (self.content_percent * self.width, self.height) )
        )
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

    def player_exceeds_window_bounds(self) -> None:
        c = 1
        if self.x + self.width / 2 > WINDOW_WIDTH:
            self.x = WINDOW_WIDTH - self.width/2 - c
        if self.x - self.width / 2 < 0:
            self.x = self.width/2 + c
        if self.y + self.height / 2 > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height/2 - c
        if self.y - self.height / 2 < 0:
            self.y = self.height/2 + c


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

        self.x += self.current_speed_x * config.dt
        self.y += self.current_speed_y * config.dt

        self.player_exceeds_window_bounds()


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

        self.x += self.current_speed_x * config.dt
        self.y += self.current_speed_y * config.dt

        self.player_exceeds_window_bounds()


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
            self.current_angle += self.max_angular_speed * config.dt
        if keys[self.keys['right']]:
            self.current_angle -= self.max_angular_speed * config.dt

        if keys[self.keys['forward']]:
            self.current_linear_speed = self.max_linear_speed
        elif keys[self.keys['backward']]:
            self.current_linear_speed = -self.max_linear_speed
        else:
            self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * config.dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * config.dt


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
            self.current_angle += self.max_angular_speed * config.dt
        if keys[self.keys['right']]:
            self.current_angle -= self.max_angular_speed * config.dt

        if keys[self.keys['forward']]:
            if self.current_linear_speed < self.max_linear_speed:
                self.current_linear_speed += self.linear_acceleration * config.dt
        elif keys[self.keys['backward']]:
            if self.current_linear_speed > -self.max_linear_speed:
                self.current_linear_speed -= self.linear_acceleration * config.dt
        else:
            if self.current_linear_speed > 10:
                self.current_linear_speed -= self.linear_decceleration * config.dt
            elif self.current_linear_speed < -10:
                self.current_linear_speed += self.linear_decceleration * config.dt
            elif -10 <= self.current_linear_speed <= 10:
                self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * config.dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * config.dt

        self.player_exceeds_window_bounds()


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
                self.current_angular_speed += self.angular_acceleration * config.dt
        elif keys[self.keys['right']]:
            if self.current_angular_speed > -self.max_angular_speed:
                self.current_angular_speed -= self.angular_acceleration * config.dt
        else:
            if self.current_angular_speed > 10:
                self.current_angular_speed -= self.angular_decceleration * config.dt
            elif self.current_angular_speed < -10:
                self.current_angular_speed += self.angular_decceleration * config.dt
            elif -10 <= self.current_angular_speed <= 10:
                self.current_angular_speed = 0

        self.current_angle += self.current_angular_speed * config.dt

        if keys[self.keys['forward']]:
            if self.current_linear_speed < self.max_linear_speed:
                self.current_linear_speed += self.linear_acceleration * config.dt
        elif keys[self.keys['backward']]:
            if self.current_linear_speed > -self.max_linear_speed:
                self.current_linear_speed -= self.linear_acceleration * config.dt
        else:
            if self.current_linear_speed > 10:
                self.current_linear_speed -= self.linear_decceleration * config.dt
            elif self.current_linear_speed < -10:
                self.current_linear_speed += self.linear_decceleration * config.dt
            elif -10 <= self.current_linear_speed <= 10:
                self.current_linear_speed = 0

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * config.dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * config.dt

        self.player_exceeds_window_bounds()


# Can shoot. Inherits movement of Invader.
class SpaceInvader(Invader):
    def __init__(self, scene, model, base_angle, bullet_model, bullet_base_angle, facing_angle,
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
        self.bullet_store = scene.bullet_store
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

        self.x += self.current_speed_x * config.dt
        self.y += self.current_speed_y * config.dt

        self.player_exceeds_window_bounds()

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
            self.shooting = True
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                event.type == pygame.WINDOWLEAVE or \
                not (-1 < MOUSE.get_pos()[0] < WINDOW_WIDTH + 1 and
                     -1 < MOUSE.get_pos()[1] < WINDOW_HEIGHT + 1):
            self.shooting = False

        # For reloading weapons.
        if event.type == self.reload_event:
            self.reloading = False
            pygame.time.set_timer(self.reload_event, 0)


# Can shoot. Inherits movement of Soldier.
class Soldier(Animal):
    def __init__(self, scene, model, base_angle, bullet_model, bullet_base_angle,
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
        self.bullet_store = scene.bullet_store
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

        self.current_angle += self.current_angular_speed * config.dt

        self.x += math.cos(math.radians(self.current_angle)) * self.current_linear_speed * config.dt
        self.y -= math.sin(math.radians(self.current_angle)) * self.current_linear_speed * config.dt

        self.player_exceeds_window_bounds()

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
            self.shooting = True
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1) or \
                event.type == pygame.WINDOWLEAVE or \
                not (-1 < MOUSE.get_pos()[0] < WINDOW_WIDTH + 1 and
                     -1 < MOUSE.get_pos()[1] < WINDOW_HEIGHT + 1):
            self.shooting = False

        # For reloading weapons.
        if event.type == self.reload_event:
            self.reloading = False
            pygame.time.set_timer(self.reload_event, 0)