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

class WalkingSprite(arcade.AnimatedWalkingSprite):
    def __init__(self, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(**kwargs)
        self.stand_right_textures = []
        self.stand_left_textures = []
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_up_textures = []
        self.texture_change_distance = 20
        self.scale = 0.8
    
    def sync_with_model(self):
        if self.model:
            self.center_x = self.model.x
            self.center_y = self.model.y
    
    def set_stand(self, png_right):
        self.stand_right_textures.append(arcade.load_texture(png_right, scale=0.75))
        self.stand_left_textures.append(arcade.load_texture(png_right,scale=0.75 , mirrored=True))
    
    def set_walk(self, png_list):
        for p in png_list:
            self.walk_left_textures.append(arcade.load_texture(p, scale=0.75))
            self.walk_right_textures.append(arcade.load_texture(p, scale=0.75, mirrored=True))
    
    def top(self):
        return self.model.y + 100

    def draw(self):
        self.sync_with_model()
        self.update_animation()

class ImNotPopcorn(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.background = arcade.load_texture("images/bg3.png")
        self.view_bottom = 0
        
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mrcorn_sprite = ModelSprite('images/mrcorn.png', model=self.world.mrcorn)
        # self.init_level(self.world.lv1)
        self.fire_sprite = ModelSprite('images/fire.png', model=self.world.lv1.fire)
        self.fire_sprite.append_texture(arcade.load_texture('images/fire2.png'))
        self.coin_list = self.init_coin(self.world.lv1.coins)
        self.checkpoint = self.init_checkpoint(self.world.lv1.checkpoint)
        self.coin_score = arcade.Sprite('images/score/coin1.png')

        self.timeCount = time.time()
        self.cur_texture = 0
    
    def init_level(self, lv):
        self.fire_sprite = ModelSprite('images/fire.png', model=lv.fire)
        self.fire_sprite.append_texture(arcade.load_texture('images/fire2.png'))
        self.coin_list = self.init_coin(lv.coins)
        self.checkpoint = self.init_checkpoint(lv.checkpoint)

    def draw_platforms(self, platforms):
        for platform in platforms:
            if platform.y > 3000:
                level = 3
            else:
                level = 1
            p = ModelSprite(f'images/platforms/lv{level}_5.png', model=platform)
            p.draw()
        for floor in platforms[:8]:
            f = ModelSprite(f'images/platforms/lv1_2.png', model=floor)
            f.draw()
    
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
    
    def draw_score(self):
        self.coin_score.append_texture(arcade.load_texture('images/score/coin2.png'))
        self.coin_score.append_texture(arcade.load_texture('images/score/coin3.png'))
        self.coin_score.append_texture(arcade.load_texture('images/score/coin4.png'))
        self.coin_score.set_position(50, SCREEN_HEIGHT + self.view_bottom - 50)
        x = arcade.Sprite('images/score/times.png')
        x.set_position(90, SCREEN_HEIGHT + self.view_bottom - 50)
        score = str(self.world.mrcorn.score)
        for i in range(len(score)):
            char = arcade.Sprite(f'images/score/{int(score[i])}.png')
            char.set_position(100+(i+1)*20, SCREEN_HEIGHT + self.view_bottom - 50)
            char.draw()
        x.draw()
        self.coin_score.draw()

    def draw_heart_bar(self):
        sp1 = ['images/score/heart.png', 'images/score/heart_empty.png', 'images/score/heart_empty.png']
        sp2 = ['images/score/heart.png', 'images/score/heart.png', 'images/score/heart_empty.png']
        sp3 = ['images/score/heart.png', 'images/score/heart.png', 'images/score/heart.png']
        n = 0
        for i in range(50, 151, 45):
            if self.world.mrcorn.heart_count == 1:
                h = arcade.Sprite(sp1[n])
            elif self.world.mrcorn.heart_count == 2:
                h = arcade.Sprite(sp2[n])
            else:
                h = arcade.Sprite(sp3[n])
            h.center_x = i
            h.center_y = SCREEN_HEIGHT + self.view_bottom - 90
            h.draw()
            n += 1

    def sprite_move(self):
        if self.cur_texture == 0:
            self.fire_sprite.set_texture(1)
            self.checkpoint.set_texture(2)
            self.coin_score.set_texture(3)
            for c in self.coin_list:
                c.set_texture(3)
            self.cur_texture = 1
        else:
            self.fire_sprite.set_texture(0)
            self.checkpoint.set_texture(0)
            self.coin_score.set_texture(0)
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
            if self.fire_sprite.model.top() < self.view_bottom:
                self.fire_sprite.model.y = self.view_bottom - 200
            if self.world.mrcorn.y > 3000:
                self.world.lv1.fire.level = 2
            self.world.lv1.update_map()
    
    def draw_game_over(self):
        self.view_bottom = 0
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 4000 // 2,
                                      SCREEN_WIDTH, 4000, self.background)
        score = str(self.world.mrcorn.score)
        for i in range(len(score)):
            char = arcade.Sprite(f'images/score/{int(score[i])}.png')
            char.set_position(SCREEN_WIDTH//2+(i+1)*20, SCREEN_HEIGHT//2)
            char.draw()
    
    def draw_game(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, SCREEN_HEIGHT + self.view_bottom//2, SCREEN_WIDTH, SCREEN_HEIGHT + self.view_bottom, arcade.color.BABY_BLUE)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 4000 // 2,
                                      SCREEN_WIDTH, 4000, self.background)
        self.draw_platforms(self.world.lv1.platforms)
        self.checkpoint.draw()
        self.draw_coin()
        for i in self.world.lv1.heart:
            h = ModelSprite('images/heart.png', model=i)
            h.draw()
        self.fire_sprite.draw()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def on_draw(self):
        arcade.start_render()
        if self.world.state == World.GAME_OVER:
            self.draw_game_over()
        else:
            #if not self.world.lv1.at_check_point():
            self.draw_game()
            self.mrcorn_sprite.draw()
            self.draw_score()
            self.draw_heart_bar()

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()
