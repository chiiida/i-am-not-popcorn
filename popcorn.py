import arcade
from models import *
import random
import time

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'I AM NOT POPCORN!'
SCALE = 0.5

VIEWPORT_MARGIN = 40

GAME_OVER = 0
INSTRUCTION_0 = 1
INSTRUCTION_1 = 2
RUNNING = 3

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

class Player(arcade.Sprite):

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)

        self.x_lst = [self.center_x]
        texture = arcade.load_texture("images/mrcorn1.png", mirrored=True, scale=SCALE)
        self.textures.append(texture)
        texture = arcade.load_texture("images/mrcorn2.png", mirrored=True, scale=SCALE)
        self.textures.append(texture)
        texture = arcade.load_texture("images/mrcorn1.png", scale=SCALE)
        self.textures.append(texture)
        texture = arcade.load_texture("images/mrcorn2.png", scale=SCALE)
        self.textures.append(texture)

        self.set_texture(0)
        self.timeCount = time.time()
        self.cur_texture = 0

    def top(self):
        return self.model.y + 100
    
    def bottom(self):
        return self.model.y - 100

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
    
    def draw(self):
        self.sync_with_model()
        super().draw()
    
    def sprite_move(self, n):
        if self.cur_texture == 0:
            self.set_texture(n)
            self.cur_texture = 1
        else:
            self.set_texture(n - 1)
            self.cur_texture = 0
        self.timeCount = time.time()

    def update(self, delta):
        if self.center_x != self.x_lst[0]:
            self.x_lst.append(self.center_x)
        
        if time.time() - self.timeCount > 0.4:
            if len(self.x_lst) > 1:
                if self.x_lst[-1] < self.x_lst[-2]:
                    self.set_texture(0)
                    self.sprite_move(1)
                if self.x_lst[-1] > self.x_lst[-2]:
                    self.set_texture(2)
                    self.sprite_move(3)
                self.x_lst.remove(self.x_lst[0])

class ImNotPopcorn(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.setup()
        self.cur_page = INSTRUCTION_0
    
    def setup(self):
        self.background = arcade.load_texture("images/bg1.png")
        self.start_page = arcade.Sprite('images/start.png', scale=SCALE)
        self.start_page.append_texture(arcade.load_texture('images/start2.png', scale=SCALE))
        self.instr = arcade.Sprite('images/instr1.png', scale=SCALE)
        self.instr.append_texture(arcade.load_texture('images/instr2.png', scale=SCALE))
        self.dead_scene = arcade.Sprite('images/gameover/die3.png', scale=SCALE)
        self.dead_scene.append_texture(arcade.load_texture(f'images/gameover/die4.png', scale=SCALE))
        self.view_bottom = 0
        self.n = 1
    
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.mrcorn_sprite = Player(model=self.world.mrcorn)
        
        self.fire_sprite = ModelSprite('images/fire2.png', model=self.world.fire, scale=SCALE)
        self.fire_sprite.append_texture(arcade.load_texture('images/fire21.png', scale=SCALE))
        
        self.coin_list = self.init_coin()
        self.checkpoint = self.init_checkpoint()
        self.wingmans = self.init_wingman()
        
        self.coin_score = arcade.Sprite('images/score/coin_1.png', scale=0.4)
        for i in range(2, 5):
            self.coin_score.append_texture(arcade.load_texture(f'images/score/coin_{i}.png', scale=0.4))

        self.timeCount = time.time()
        self.cur_texture = 0

    def init_level(self, lv):
        self.fire_sprite = ModelSprite('images/fire1.png', model=lv.fire, scale=SCALE)
        self.fire_sprite.append_texture(arcade.load_texture('images/fire21.png', scale=SCALE))
        self.coin_list = self.init_coin(lv.coins)
        self.checkpoint = self.init_checkpoint(lv.checkpoint)

    def draw_platforms(self, platforms):
        i = 1
        for platform in platforms:
            if i < 9:
                p = ModelSprite(f'images/platforms/lv{self.n}_1.png', model=platform, scale=SCALE)
            else:
                p = ModelSprite(f'images/platforms/lv{self.n}_2.png', model=platform, scale=SCALE)
            i += 1
            p.draw()
    
    def init_coin(self):
        coins_lst = []
        for coin in self.world.lv1.coins:
            c = ModelSprite('images/coin/coin_1.png', model=coin, scale=SCALE)
            for i in range(2, 5):
                c.append_texture(arcade.load_texture(f'images/coin/coin_{i}.png', scale=SCALE))
            coins_lst.append(c)
        return coins_lst

    def draw_coin(self):
        for c in self.coin_list:
            if not c.model.is_collected:
                c.draw()
    
    def init_checkpoint(self):
        cp = ModelSprite('images/flags/lv1_flag1.png', model=self.world.lv1.checkpoint)
        cp.append_texture(arcade.load_texture('images/flags/lv1_flag2.png'))
        cp.append_texture(arcade.load_texture('images/flags/lv1_flag3.png'))
        return cp
    
    def draw_score(self):
        self.coin_score.set_position(50, SCREEN_HEIGHT + self.view_bottom - 50)
        x = arcade.Sprite('images/score/times.png', scale=0.3)
        x.set_position(90, SCREEN_HEIGHT + self.view_bottom - 50)
        score = str(self.world.mrcorn.score)
        for i in range(len(score)):
            char = arcade.Sprite(f'images/score/{int(score[i])}.png', scale=0.3)
            char.set_position(100+(i+1)*20, SCREEN_HEIGHT + self.view_bottom - 50)
            char.draw()
        x.draw()
        self.coin_score.draw()

    def draw_heart_bar(self):
        sp1 = ['images/heart1.png', 'images/heart_empty1.png', 'images/heart_empty1.png']
        sp2 = ['images/heart1.png', 'images/heart1.png', 'images/heart_empty1.png']
        sp3 = ['images/heart1.png', 'images/heart1.png', 'images/heart1.png']
        n = 0
        for i in range(50, 151, 45):
            if self.world.mrcorn.heart_count == 1:
                h = arcade.Sprite(sp1[n], scale=0.4)
            elif self.world.mrcorn.heart_count == 2:
                h = arcade.Sprite(sp2[n], scale=0.4)
            else:
                h = arcade.Sprite(sp3[n], scale=0.4)
            h.center_x = i
            h.center_y = SCREEN_HEIGHT + self.view_bottom - 90
            h.draw()
            n += 1
    
    def draw_label(self):
        label = arcade.Sprite('images/label/label.png', scale=0.2)
        label.set_position(SCREEN_WIDTH - 60, SCREEN_HEIGHT + self.view_bottom - 50)
        label.draw()
        for i in range(len(str(self.world.level))):
            char = arcade.Sprite(f'images/label/{str(self.world.level)[i-1]}.png', scale=0.2)
            if self.world.level > 9:
                char.set_position(SCREEN_WIDTH - (62+((i-1)*11)), SCREEN_HEIGHT + self.view_bottom - 50)
            else:
                char.set_position(SCREEN_WIDTH - 60, SCREEN_HEIGHT + self.view_bottom - 50)
            char.draw()

    def draw_spikes(self):
        for sp in self.world.lv1.spikes:
            sp = ModelSprite('images/spikes.png', model=sp, scale=0.25)
            sp.draw()
    
    def init_wingman(self):
        wingmans = []
        for e in self.world.lv1.wingman:
            wm = ModelSprite('images/enemy/red1.png', model=e, scale=SCALE)
            wm.append_texture(arcade.load_texture(f'images/enemy/red2.png', scale=SCALE))
            wingmans.append(wm)
        return wingmans
    
    def draw_item(self):
        items = self.world.lv1.items
        n = self.world.lv1.item_no
        if n%2 == 0:
            t = ModelSprite('images/jetpack1.png', model=items[0], scale=SCALE)
        elif n%2 != 0:
            t = ModelSprite('images/star1.png', model=items[0], scale=SCALE)
        t.draw()  

    def sprite_move(self):
        if self.cur_texture == 0:
            self.fire_sprite.set_texture(1)
            self.checkpoint.set_texture(2)
            self.coin_score.set_texture(3)
            self.start_page.set_texture(1)
            self.instr.set_texture(1)
            self.dead_scene.set_texture(1)
            for c in self.coin_list:
                c.set_texture(3)
            for wm in self.wingmans:
                wm.set_texture(1)
            self.cur_texture = 1
        else:
            self.fire_sprite.set_texture(0)
            self.checkpoint.set_texture(0)
            self.coin_score.set_texture(0)
            self.start_page.set_texture(0)
            self.instr.set_texture(0)
            self.dead_scene.set_texture(0)
            for c in self.coin_list:
                c.set_texture(0)
            for wm in self.wingmans:
                wm.set_texture(0)
            self.cur_texture = 0
        self.timeCount = time.time()
    
    def draw_start(self):
        self.start_page.set_position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.start_page.draw()
    
    def draw_instruction(self):
        self.instr.set_position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.instr.draw()

    def draw_game_over(self):
        self.view_bottom = 0
        arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, 
                        SCREEN_HEIGHT + self.view_bottom)
        bg = arcade.Sprite('images/gameover/gameover_page.png', scale=SCALE)
        bg.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        bg.draw()
        self.dead_scene.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.dead_scene.draw()

        self.coin_score.scale = 0.5
        self.coin_score.set_position(SCREEN_WIDTH//2 + 15, SCREEN_HEIGHT//2 + 140)
        self.coin_score.draw()

        score = str(self.world.mrcorn.score)
        for i in range(len(score)):
            char = arcade.Sprite(f'images/gameover/scorenum{int(score[i])}.png', scale=SCALE)
            char.set_position(SCREEN_WIDTH//2+(i)*35, (SCREEN_HEIGHT + self.view_bottom)//2)
            char.draw()

        level = str(self.world.level)
        for i in range(len(level)):
            char = arcade.Sprite(f'images/gameover/levelnum{str(level[i])}.png', scale=SCALE)
            if self.world.level > 9:
                char.set_position(SCREEN_WIDTH//2 + (i)*35, SCREEN_HEIGHT//2)
            else:
                char.set_position(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            char.draw()
    
    def draw_game(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, SCREEN_HEIGHT + self.view_bottom//2, 
                                     SCREEN_WIDTH, SCREEN_HEIGHT + self.view_bottom, arcade.color.BABY_BLUE)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 6000 // 2,
                                      SCREEN_WIDTH, 6000, self.background)
        self.draw_platforms(self.world.lv1.platforms)
        self.checkpoint.draw()
        self.draw_coin()
        self.draw_spikes()
        for wm in self.wingmans:
            wm.draw()
        self.draw_item()
        for i in self.world.lv1.heart:
            h = ModelSprite('images/heart1.png', model=i, scale=SCALE)
            h.draw()
        self.mrcorn_sprite.draw()
        self.fire_sprite.draw()
    
    def next_level(self):
        if self.n >= 6:
            self.n = 1
        else:
            self.n += 1
        self.view_bottom = 0
        arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, 
                        SCREEN_HEIGHT + self.view_bottom)
        self.coin_list = self.init_coin()
        self.checkpoint = self.init_checkpoint()
        self.wingmans = self.init_wingman()

    def change_viewport(self):
        changed = False

        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.mrcorn_sprite.top() > top_bndry:
            self.view_bottom += self.mrcorn_sprite.top() - top_bndry
            changed = True

        if changed:
            arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, 
                                SCREEN_HEIGHT + self.view_bottom)
            if self.fire_sprite.model.top() < self.view_bottom:
                self.fire_sprite.model.y = self.view_bottom - 200

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if key == arcade.key.ENTER and self.cur_page == INSTRUCTION_0:
            self.cur_page = RUNNING
            self.world.state = World.START
        elif key == arcade.key.RIGHT and self.cur_page == INSTRUCTION_0:
            self.cur_page = INSTRUCTION_1
        elif key == arcade.key.ENTER and self.cur_page == INSTRUCTION_1:
            self.cur_page = RUNNING
            self.world.state = World.START
        elif key == arcade.key.ENTER and self.world.state == World.GAME_OVER:
            self.world.restart()
            self.n = 1
            self.coin_list = self.init_coin()
            self.checkpoint = self.init_checkpoint()
            self.wingmans = self.init_wingman()
            self.view_bottom = 0
            arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, 
                            SCREEN_HEIGHT + self.view_bottom)
            self.world.state = World.START
    
    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)
    
    def update(self, delta):
        self.world.update(delta)
        self.mrcorn_sprite.update(delta)
        self.change_viewport()

        if time.time() - self.timeCount > 0.4:
            self.sprite_move()

    def on_draw(self):
        arcade.start_render()
        if self.cur_page == INSTRUCTION_0:
            self.draw_start()   
        elif self.cur_page == INSTRUCTION_1:
            self.draw_instruction()
        elif self.world.state == World.GAME_OVER:
            self.draw_game_over()
        elif self.cur_page == RUNNING:
            if self.world.state == World.PASS:
                self.next_level()
            self.draw_game()
            self.draw_score()
            self.draw_label()
            self.draw_heart_bar()

def main():
    window = ImNotPopcorn(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.set_window(window)
    arcade.run()

if __name__ == '__main__':
    main()
