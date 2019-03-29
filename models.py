import arcade.key
from map_lv1 import *

MOVEMENT_SPEED = 5

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_LEFT = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_LEFT: (-1,0) }

JUMP_SPEED = 20
GRAVITY = -1

COIN_HIT_MARGIN = 30
PLAYER_MARGIN = 50

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

class MrCorn(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)
        self.vx = 0
        self.vy = 0
        self.direction = DIR_STILL
        self.is_jump = False
        self.platform = None
    
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]
    
    def jump(self):
        if not self.is_jump:
            self.is_jump = True
            self.vy = JUMP_SPEED
    
    def top(self):
        return self.y + 100

    def bottom(self):
        return self.y - 100
    
    def left(self):
        return self.x - 25
    
    def right(self):
        return self.x + 25
    
    def set_platform(self, platform):
        self.is_jump = False
        self.platform = platform
        self.y = platform.y + 100

    def is_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False
        
        if abs(platform.y - self.bottom()) <= 50:
            return True

        return False
    
    def is_falling_on_platform(self, platform):
        if not platform.in_top_range(self.x):
            return False
        
        if self.bottom() - self.vy > platform.y > self.bottom():
            return True
        
        return False

    def find_touching_platform(self):
        platforms = self.world.platforms
        for p in platforms:
            if self.is_falling_on_platform(p):
                return p
    
    def check_out_of_world(self):
        if self.x <= PLAYER_MARGIN or self.x - PLAYER_MARGIN >= self.world.width:
            self.direction = DIR_STILL
            if self.x <= 0:
                self.x = PLAYER_MARGIN
            if self.x >= self.world.width:
                self.x = self.world.width - PLAYER_MARGIN
    
    def update(self, delta):
        self.move(self.direction)
        self.check_out_of_world()
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0

class Fire:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def top(self):
        return self.y + self.height//2

    def update(self, delta):
        self.y += 1

class Platform:
    def __init__(self, world, x, y, width, height):
        self.world = world
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def in_top_range(self, x):
        return self.x - self.width//2 <= x <= self.x + self.width//2

    def in_bottom_range(self, x):
        return self.x - self.width//2 <= x <= self.x + self.width//2

class Coin:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.is_collected = False
    
    def collected(self, mrcorn):
        return ((abs(self.x - mrcorn.x) < COIN_HIT_MARGIN) and
                (abs(self.y - mrcorn.y) < COIN_HIT_MARGIN))
    
    def update(self, delta):
        pass

class World:
    START = 0
    DEAD = 1
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = World.START

        self.mrcorn = MrCorn(self, 50, 150)
        self.floor_list = []
        self.fire = Fire(self, self.width//2, -700, 700, 800)
        self.platforms = self.gen_map(map_lv1)
        self.coins = self.gen_coin(lv1_coins)
        self.coin_point = 0
    
    def gen_map(self, map):
        map.reverse()
        self.platforms = []
        for r in range(len(map)):
            for c in range(len(map[0])):
                if map[r][c] == '#':
                    p = Platform(self, (c)*100, (r+1)*100, 100, 100)
                    self.platforms.append(p)
                elif map[r][c] == '$':
                    p = Platform(self, (c)*100, (r+1)*50, 100, 100)
                    self.floor_list.append(p)
                    self.platforms.append(p)
        return self.platforms
    
    def gen_coin(self, coin_array):
        self.coins = []
        for coin in coin_array:
            c = Coin(self, coin[0], coin[1])
            self.coins.append(c)
        return self.coins
    
    def collect_coins(self):
        for c in self.coins:
            if not c.is_collected and c.collected(self.mrcorn):
                c.is_collected = True
                self.coin_point += 100
    
    def kill_coin(self):
        for c in self.coins:
            if c.is_collected == True:
                index = self.coins.index(c)
                self.coins.pop(index)
    
    def is_dead(self):
        if self.mrcorn.bottom()+70 < self.fire.top():
            self.state = World.DEAD

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.mrcorn.jump()
        elif key == arcade.key.LEFT:
            self.mrcorn.direction = DIR_LEFT
        elif key == arcade.key.RIGHT:
            self.mrcorn.direction = DIR_RIGHT
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.mrcorn.direction = DIR_STILL

    def update(self, delta):
        self.is_dead()
        if self.state == World.START:
            self.mrcorn.update(delta)
            self.fire.update(delta)
            self.collect_coins()
            self.kill_coin()