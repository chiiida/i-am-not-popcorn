import arcade

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'I AM NOT POPCORN!'

class ImNotPopcorn(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("images/bg.png")
    
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()