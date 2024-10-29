import arcade
import random
import math
from modulo import OBJECT_SCALE, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(arcade.Sprite):
    def __init__(self, enemy_type):
        super().__init__(enemy_type, scale=1 * OBJECT_SCALE)

        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = random.choice([-100, SCREEN_HEIGHT + 100])
        self.speed = 3
        self.player = None
        self.vida = 50
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        dist = math.hypot(dx, dy)
        dx /= dist
        dy /= dist
        self.center_x += dx * self.speed
        self.center_y += dy * self.speed

        self.offset_x = math.sin(self.center_x * 0.01) * 1.2
        self.offset_y = math.sin(self.center_y * 0.01) * 1.2
        self.center_x += self.offset_x
        self.center_y += self.offset_y

class CobraEnemy(Enemy):
    def __init__(self):
        super().__init__("./Sprites/COBA.png")
        self.speed = 3

class PandaEnemy(Enemy):
    def __init__(self):
        super().__init__("./Sprites/PANDA.png")
        self.vida = 50
        self.speed = 3

class KiwiEnemy(Enemy):
    def __init__(self):
        super().__init__("./Sprites/kiwi.png")
        self.speed = 5
class caracol(Enemy):
    def __init__(self):
        super().__init__("./Sprites/caracol.png")
        self.vida = 50
        self.speed = 2
class AbeiaEnemy(Enemy):
    def __init__(self):
        super().__init__("./Sprites/beia.png")
        self.speed = 5
        self.dash_speed = 1000
        self.dash_duration = 0.5  # duração do dash em segundos
        self.dash_timer = 0
        self.dash_cooldown = 2  # tempo de espera entre dashes em segundos
        self.dash_cooldown_timer = 0
        self.dashing = False

    def update(self):
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        dist = math.hypot(dx, dy)

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1
            dx /= dist
            dy /= dist
            self.center_x += dx * self.speed
            self.center_y += dy * self.speed
        else:
            if dist > 200:  # distância para dar um dash
                if not self.dashing:
                    self.dash_timer = 0
                    self.dashing = True
                self.dash_timer += 1
                if self.dash_timer >= 60 * self.dash_duration:
                    self.dashing = False
                    self.dash_cooldown_timer = 60 * self.dash_cooldown
                else:
                    dx /= dist
                    dy /= dist
                    self.center_x += dx * self.dash_speed / 60
                    self.center_y += dy * self.dash_speed / 60
            else:
                dx /= dist
                dy /= dist
                self.center_x += dx * self.speed
                self.center_y += dy * self.speed

class NovoMacacoEnemy(Enemy):
    def __init__(self, personagem):
        self.fart_sound = arcade.load_sound("MACACO.mp3")
        super().__init__("./Sprites/Macaco.png")
        self.tiro_timer = 0
        self.player = personagem.jogador
        self.angle = 0
        self.distancia_para_girar = 200

    def update(self):
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        dist = math.hypot(dx, dy)

        if dist > self.distancia_para_girar:
            dx /= dist
            dy /= dist
            self.center_x += dx * self.speed
            self.center_y += dy * self.speed
        else:
            self.angle += 1
            self.center_x = self.player.center_x + math.cos(math.radians(self.angle)) * self.distancia_para_girar
            self.center_y = self.player.center_y + math.sin(math.radians(self.angle)) * self.distancia_para_girar
        self.offset_x = math.sin(self.center_x * 0.01) * 2
        self.offset_y = math.sin(self.center_y * 0.01) * 2
        self.center_x += self.offset_x
        self.center_y += self.offset_y
        