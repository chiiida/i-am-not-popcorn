import arcade
from models import World, MrCorn

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'I AM NOT POPCORN!'

VIEWPORT_MARGIN = 40

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
    
    def top(self):
        return self.model.y + 100

    def draw(self):
        self.sync_with_model()
        super().draw()

class ImNotPopcorn(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background = arcade.load_texture("images/bg.png")
        self.view_bottom = 0
        
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mrcorn_sprite = ModelSprite('images/mrcorn.png', model=self.world.mrcorn)
        self.world.mrcorn_sprite = self.mrcorn_sprite

    def draw_floor(self, floor_list, level):
        for floor in floor_list:
            f = ModelSprite(f'images/platforms/lv{level}_2.png', model=floor)
            f.draw()
    
    def draw_platforms(self, platforms, level):
        for platform in platforms[1:]:
            for each in platform:
                p = ModelSprite(f'images/platforms/lv{level}_5.png', model=each)
                p.draw()

    def update(self, delta):
        changed = False
        self.world.update(delta)

        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.mrcorn_sprite.top() > top_bndry:
            self.view_bottom += self.mrcorn_sprite.top() - top_bndry
            changed = True

        if changed:
            arcade.set_viewport(0, 0 + SCREEN_WIDTH, self.view_bottom, 
                                SCREEN_HEIGHT + self.view_bottom)
    
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.draw_floor(self.world.floor_list, 1)
        self.draw_platforms(self.world.platforms, 1)
        self.mrcorn_sprite.draw()

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()

arcade.Sprite