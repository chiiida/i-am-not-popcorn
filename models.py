import arcade.key

MOVEMENT_SPEED = 4

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

KEY_MAP = { arcade.key.UP: DIR_UP,
            arcade.key.DOWN: DIR_DOWN,
            arcade.key.LEFT: DIR_LEFT,
            arcade.key.RIGHT: DIR_RIGHT, }

class MrCorn:
    SPRITE_SCALING = 0.5

    MOVEMENT_SPEED = 5 * SPRITE_SCALING
    JUMP_SPEED = 28 * SPRITE_SCALING
    GRAVITY = .9 * SPRITE_SCALING

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
    
    def update(self, delta):
        pass

class Fire:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
    
    def update(self, delta):
        pass

class Floor:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.floor_list = arcade.SpriteList()
    
    def draw(self):
        for x in range(50, self.y, 50):
            floor = arcade.Sprite('images/platforms/lv1_2.png')
            floor.center_x = x
            floor.center_y = 50
            self.floor_list.append(floor)
        
        self.floor_list.draw()

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.mrcorn = MrCorn(self, 100, 100)
        self.floor = Floor(self, width, height)
    
    def update(self, delta):
        self.mrcorn.update(delta)