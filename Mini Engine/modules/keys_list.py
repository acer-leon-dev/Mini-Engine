import pygame

class Keybinds:
    def __init__(self):
        self.key = {
            'a': pygame.K_a,
            'b': pygame.K_b,
            'c': pygame.K_c,
            'd': pygame.K_d,
            'e': pygame.K_e,
            'f': pygame.K_f,
            'g': pygame.K_g,
            'h': pygame.K_h,
            'i': pygame.K_i,
            'j': pygame.K_j,
            'k': pygame.K_k,
            'l': pygame.K_l,
            'm': pygame.K_m,
            'n': pygame.K_n,
            'o': pygame.K_o,
            'p': pygame.K_p,
            'q': pygame.K_q,
            'r': pygame.K_r,
            's': pygame.K_s,
            't': pygame.K_t,
            'u': pygame.K_u,
            'v': pygame.K_v,
            'w': pygame.K_w,
            'x': pygame.K_x,
            'y': pygame.K_y,
            'z': pygame.K_z,
            ' ': pygame.K_SPACE,
            'UP': pygame.K_UP,
            'DOWN': pygame.K_DOWN,
            'LEFT': pygame.K_LEFT,
            'RIGHT': pygame.K_RIGHT
        }

    # {keybinds} must be formatted as "A-B-C-D", with
    # the characters replaced with the desired binds in {key} in
    # the order of: up/forward, left, down/backward, right
    def split_binds(self, keybinds):
        binds = keybinds.split('-')

        keys = {
            'forward': self.key[binds[0]],
            'left': self.key[binds[1]],
            'backward': self.key[binds[2]],
            'right': self.key[binds[3]]
            }

        return keys

Keybinds = Keybinds()

if __name__ == "__main__":
    pass