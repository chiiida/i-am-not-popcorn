import arcade
from models import World, MrCorn
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'I AM NOT POPCORN!'

SPRITE_SCALING = 0.5
GRAVITY = .9 * SPRITE_SCALING

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()

class ImNotPopcorn(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("images/bg.png")
        
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mrcorn_sprite = ModelSprite('images/mrcorn.png', model=self.world.mrcorn)
        self.floor = self.world.floor

        self.physics_engine = \
            arcade.PhysicsEnginePlatformer(self.mrcorn_sprite,
                                           self.floor,
                                           gravity_constant=GRAVITY)
    
    def update(self, delta):
        self.world.update(delta)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.floor.draw()
        # self.mrcorn_sprite.draw()

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()