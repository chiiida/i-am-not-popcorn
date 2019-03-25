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

    def update(self, delta):
        self.move(self.direction)
        
        if self.is_jump:
            self.y += self.vy
            self.vy += GRAVITY

            new_platform = self.find_touching_platform()
            if new_platform:
                self.vy = 0
                self.set_platform(new_platform)
        else:
            if (self.platform) and (not self.is_on_platform(self.platform)) and (not self.top_touch_platform(self.platform)):
                self.platform = None
                self.is_jump = True
                self.vy = 0
    
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
        for platform in platforms:
            for p in platform:
                if self.is_falling_on_platform(p):
                    return p

    def top_touch_platform(self, platform):
        if not platform.in_bottom_range(self.x):
            return False
        
        if self.top() - self.vy < platform.y < self.top():
            return True
        
        return False
    
    def find_top_touching(self):
        platforms = self.world.platforms
        for platform in platforms:
            for p in platform:
                if self.top_touch_platform(p):
                    return p

class Fire:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

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
        return self.x <= x <= self.x + self.width

    def in_bottom_range(self, x):
        return self.x >= x >= self.x + self.width

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.mrcorn = MrCorn(self, 50, 150)
        self.init_floor()
        self.fire = Fire(self, width//2, -700)
        self.platforms = self.gen_platform(lv1_platform)
        self.platforms.insert(0, self.floor_list)

    def init_floor(self):
        self.floor_list = []
        for x in range(50, self.width, 100):
            floor = Platform(self, x, 50, 100, 100)
            self.floor_list.append(floor)

    def gen_platform(self, platforms_array):
        self.platforms = []
        for platform_list in platforms_array:
            platform = []
            for x in range(platform_list[1], (100+platform_list[1])+1, 100):
                each = Platform(self, x, platform_list[2], 100, 100)
                platform.append(each)
            self.platforms.append(platform[:platform_list[0]])
        return self.platforms
    
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
        self.mrcorn.update(delta)
        self.fire.update(delta)

        if self.mrcorn.left() <= 0:
            self.mrcorn.direction = DIR_STILL
        elif self.mrcorn.right() >= 700:
            self.mrcorn.direction = DIR_STILL