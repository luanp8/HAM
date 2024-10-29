import arcade
import math
import random
from modulo import SCREEN_HEIGHT, SCREEN_WIDTH
from enemy import CobraEnemy,KiwiEnemy,AbeiaEnemy,PandaEnemy,NovoMacacoEnemy, caracol
SPRITE_SCALING_LASER = 0.8
BULLET_SPEED = 5
DASH_SPEED = 1000
OBJECT_SCALE = SCREEN_WIDTH / 1920 

class Personagem(arcade.View):
    def __init__(self):
        super().__init__()
        self.music = arcade.load_sound("fundo.mp3")
        arcade.play_sound(self.music, looping=True)
        self.jogador = arcade.Sprite(
            "./Sprites/pixil-frame-0.png",
            scale=0.1 * OBJECT_SCALE,
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.dash_speed = 1000
        self.dash_duration = 0.5
        self.dash_timer = 0
        self.background = arcade.Sprite(
            "./Sprites/fundo.png",
            scale=OBJECT_SCALE,
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.macaco_bullet_list = arcade.SpriteList()
        self.movendo_direita = False
        self.movendo_esquerda = False
        self.movendo_baixo = False
        self.movendo_cima = False
        self.angle = 0
        self.game_over = False
        self.wave = 1
        self.wave_timer = 10
        self.enemy_limit = 5
        self.game_over_texture = arcade.Sprite(
            "./Sprites/gameover.png",
            scale=5 * OBJECT_SCALE,
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.gg_texture = arcade.Sprite(
            "./Sprites/gg.jpg",
            scale=OBJECT_SCALE,
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.life = arcade.Sprite(
            "./Sprites/vida.png",
             scale=1 * OBJECT_SCALE,
            center_x=40,
            center_y=SCREEN_HEIGHT - 20
        )
        self.onda = arcade.Sprite(
            "./Sprites/wave.png",
            scale=1 * OBJECT_SCALE,
            center_x=40,
            center_y=SCREEN_HEIGHT - 60
            )
        self.ponto = arcade.Sprite(
            "./Sprites/pontos.png",
            scale=1* OBJECT_SCALE,
            center_x=40,
            center_y=SCREEN_HEIGHT - 100
        )           
        self.pontos = 0
        self.vidas = 3
        self.sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.explosion_sound = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.level_up_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.victory_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.enemy_spawn_timer = 0
        self.enemies_alive = 0
        self.enemies_spawned = 0
        self.dash = False
        self.dash_timer = 0
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.damage = 5
        self.enemy_types = [CobraEnemy, PandaEnemy, KiwiEnemy, AbeiaEnemy, lambda: NovoMacacoEnemy(self), caracol]
        
    def on_update(self, delta_time):
        velocidade = 200
        if not self.game_over:
            self.bullet_list.update()
            self.enemy_list.update()
            self.macaco_bullet_list.update()

            if self.dash:
                self.dash_timer += delta_time
                if self.dash_timer < self.dash_duration:
                    velocidade = self.dash_speed
                else:
                    self.dash = False
                    self.dash_timer = 0

            for enemy in self.enemy_list:
                if enemy is not None:
                    if isinstance(enemy, NovoMacacoEnemy):
                        bullet = enemy.update()
                        if bullet is not None:
                            self.macaco_bullet_list.append(bullet)

            if self.movendo_direita:
                self.jogador.center_x += velocidade * delta_time
            if self.movendo_esquerda:
                self.jogador.center_x -= velocidade * delta_time
            if self.movendo_cima:
                self.jogador.center_y += velocidade * delta_time
            if self.movendo_baixo:
                self.jogador.center_y -= velocidade * delta_time

            if self.jogador.center_x < 0:
                self.jogador.center_x = 0
            if self.jogador.center_x > SCREEN_WIDTH:
                self.jogador.center_x = SCREEN_WIDTH
            if self.jogador.center_y < 0:
                self.jogador.center_y = 0
            if self.jogador.center_y > SCREEN_HEIGHT:
                self.jogador.center_y = SCREEN_HEIGHT

            for enemy in self.enemy_list:
                if enemy is not None:
                    if enemy.center_x < 0 or enemy.center_x > SCREEN_WIDTH:
                        enemy.center_x = random.choice([0, SCREEN_WIDTH])
                    if enemy.center_y < 0 or enemy.center_y > SCREEN_HEIGHT:
                        enemy.center_y = random.choice([0, SCREEN_HEIGHT])

            for bullet in self.bullet_list:
                if bullet.center_x < 0 or bullet.center_x > SCREEN_WIDTH:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y < 0 or bullet.center_y > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()

            for bullet in self.macaco_bullet_list:
                if bullet.center_x < 0 or bullet.center_x > SCREEN_WIDTH:
                    bullet.remove_from_sprite_lists()
                if bullet.center_y < 0 or bullet.center_y > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()

            for enemy in self.enemy_list:
                if enemy is not None:
                    if arcade.check_for_collision(self.jogador, enemy):
                        self.vidas -= 1
                        enemy.remove_from_sprite_lists()
                        self.enemies_alive -= 1
                        if self.vidas == 0:
                            self.game_over = True
                            arcade.play_sound(self.game_over_sound)
            for bullet in self.bullet_list:
                for enemy in self.enemy_list:
                    if enemy is not None:
                        if arcade.check_for_collision(bullet, enemy):
                            bullet.remove_from_sprite_lists()
                            enemy.vida -= self.damage
                            if enemy.vida <= 0:
                                arcade.play_sound(self.explosion_sound)
                                enemy.remove_from_sprite_lists()
                                self.enemies_alive -= 1
                                self.pontos += 10
                                self.experience += 10
                                if self.experience >= self.experience_to_next_level:
                                    self.level_up()

            for bullet in self.macaco_bullet_list:
                if arcade.check_for_collision(self.jogador, bullet):
                    self.vidas -= 1
                    bullet.remove_from_sprite_lists()
                    if self.vidas == 0:
                        self.game_over = True
                        arcade.play_sound(self.game_over_sound)

            if self.enemies_spawned < self.enemy_limit:
                if self.enemy_spawn_timer > 0:
                    self.enemy_spawn_timer -= delta_time
                else:
                    enemy_type = random.choice(self.enemy_types)
                    enemy = enemy_type()
                    if enemy is not None:
                        enemy.player = self.jogador
                        enemy.center_x = random.choice([0, SCREEN_WIDTH])
                        enemy.center_y = random.choice([0, SCREEN_HEIGHT])
                        self.enemy_list.append(enemy)
                        self.enemies_alive += 1
                        self.enemies_spawned += 1
                        self.enemy_spawn_timer = 1

            if self.enemies_alive == 0 and self.enemies_spawned == self.enemy_limit:
                self.wave += 1
                self.enemy_limit += 3
                self.enemies_spawned = 0
                self.enemies_alive = 0

            if self.wave >= 10:
                self.game_over = True
                arcade.play_sound(self.victory_sound)

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.experience_to_next_level += 50
        self.damage += 5
        arcade.play_sound(self.level_up_sound)

    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.jogador.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.macaco_bullet_list.draw()
        if self.game_over:
            self.game_over_texture.draw()
            if self.wave >= 10:
                self.gg_texture.draw()
        self.life.draw()
        self.onda.draw()
        self.ponto.draw()
        arcade.draw_text(f"{self.wave}", 90, SCREEN_HEIGHT - 70, arcade.color.WHITE, 20)  
        arcade.draw_text(f"{self.vidas}", 90, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
        arcade.draw_text(f" {self.pontos}", 90, SCREEN_HEIGHT - 110, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.movendo_cima = True
        if key == arcade.key.S:
            self.movendo_baixo = True
        if key == arcade.key.A:
            self.movendo_esquerda = True
        if key == arcade.key.D:
            self.movendo_direita = True
        if key == arcade.key.SPACE:
            self.dash = True
        if key == arcade.key.R and self.game_over:
            self.game_over = False
            self.vidas = 3
            self.pontos = 0
            self.wave = 1
            self.enemy_limit = 5
            self.bullet_list = arcade.SpriteList()
            self.enemy_list = arcade.SpriteList()
            self.macaco_bullet_list = arcade.SpriteList()
            self.enemies_spawned = 0
            self.enemies_alive = 0
            self.jogador.center_x = SCREEN_WIDTH // 2
            self.jogador.center_y = SCREEN_HEIGHT // 2
            self.level = 1
            self.experience = 0
            self.experience_to_next_level = 100
            self.damage = 5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.movendo_cima = False
        if key == arcade.key.S:
            self.movendo_baixo = False
        if key == arcade.key.A:
            self.movendo_esquerda = False
        if key == arcade.key.D:
            self.movendo_direita = False
        if key == arcade.key.SPACE:
            self.dash = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.angle = math.degrees(math.atan2(y - self.jogador.center_y, x - self.jogador.center_x))
        self.jogador.angle = self.angle

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = arcade.Sprite("./Sprites/laser.png", scale=0.5 * OBJECT_SCALE)
            bullet.angle = self.angle
            bullet.change_x = math.cos(math.radians(bullet.angle)) * BULLET_SPEED
            bullet.change_y = math.sin(math.radians(bullet.angle)) * BULLET_SPEED
            bullet.center_x = self.jogador.center_x
            bullet.center_y = self.jogador.center_y
            self.bullet_list.append(bullet)
            arcade.play_sound(self.sound, volume=0.25)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Jogo", fullscreen=True)
    window.show_view(Personagem())
    arcade.run()

if __name__ == "__main__":
    main()