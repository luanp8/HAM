import arcade 
import pyautogui
from personagem import Personagem    
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
class inicio(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.Sprite("./Sprites/unnamed.png",
                                           scale=1,  
                                           center_x=self.window.width / 2,
                                           center_y=self.window.height /2)
        self.botao_iniciar = arcade.Sprite("./Sprites/botao.png",
                                           scale=3,  
                                           center_x=self.window.width / 2,
                                           center_y=self.window.height /4)
        self.background.width = SCREEN_WIDTH
        self.background.height = SCREEN_HEIGHT
     
    def on_draw(self):
        arcade.start_render()
        self.background.draw()
        self.botao_iniciar.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.botao_iniciar.collides_with_point((x, y)):
            t2 = Personagem()
            self.window.show_view(t2)

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "game" , fullscreen=True)
    menu_view = inicio()
    window.show_view(menu_view)
    arcade.run()
