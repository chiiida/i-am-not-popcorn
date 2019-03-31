import arcade
from models import World, MrCorn
import random
import time

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

        self.background = arcade.load_texture("images/bg3.png")
        self.view_bottom = 0
        
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mrcorn_sprite = ModelSprite('images/mrcorn.png', model=self.world.mrcorn)
        self.fire_sprite = ModelSprite('images/fire.png', model=self.world.fire)
        self.fire_sprite.append_texture(arcade.load_texture('images/fire2.png'))
        self.coin_list = self.init_coin(self.world.coins)
        self.checkpoint = self.init_checkpoint(self.world.checkpoint)
        self.heart_sprite = ModelSprite('images/heart.png', model=self.world.heart)
        
        self.timeCount = time.time()
        self.cur_texture = 0

    def draw_floor(self, floor_list, level):
        for floor in floor_list:
            f = ModelSprite(f'images/platforms/lv{level}_2.png', model=floor)
            f.draw()
    
    def draw_platforms(self, platforms, level):
        for platform in platforms[1:]:
                p = ModelSprite(f'images/platforms/lv{level}_5.png', model=platform)
                p.draw()
    
    def init_coin(self, coins):
        self.coins = []
        for coin in coins:
            c = ModelSprite('images/coin/coin1.png', model=coin)
            c.append_texture(arcade.load_texture('images/coin/coin2.png'))
            c.append_texture(arcade.load_texture('images/coin/coin3.png'))
            c.append_texture(arcade.load_texture('images/coin/coin4.png'))
            self.coins.append(c)
        return self.coins

    def draw_coin(self):
        for c in self.coin_list:
            if not c.model.is_collected:
                c.draw()
    
    def init_checkpoint(self, checkpoint):
        cp = ModelSprite('images/flags/lv1_flag1.png', model=checkpoint)
        cp.append_texture(arcade.load_texture('images/flags/lv1_flag2.png'))
        cp.append_texture(arcade.load_texture('images/flags/lv1_flag3.png'))
        return cp

    def sprite_move(self):
        if self.cur_texture == 0:
            self.fire_sprite.set_texture(1)
            self.checkpoint.set_texture(2)
            for c in self.coin_list:
                c.set_texture(3)
            self.cur_texture = 1
        else:
            self.fire_sprite.set_texture(0)
            self.checkpoint.set_texture(0)
            for c in self.coin_list:
                c.set_texture(0)
            self.cur_texture = 0
        self.timeCount = time.time()      

    def update(self, delta):
        changed = False
        self.world.update(delta)
        if time.time() - self.timeCount > 0.2:
            self.sprite_move()

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
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 4000 // 2,
                                      SCREEN_WIDTH, 4000, self.background)
        self.draw_platforms(self.world.platforms, 1)
        self.draw_floor(self.world.floor_list, 1)
        self.checkpoint.draw()
        self.draw_coin()
        self.heart_sprite.draw()
        self.mrcorn_sprite.draw()
        self.fire_sprite.draw()

        arcade.draw_text(str(self.world.coin_point), SCREEN_WIDTH - 50, SCREEN_HEIGHT - 20, arcade.color.AMERICAN_ROSE, 20)

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()
