import random

map_pool = ['....#...',
            '.....##.',
            '....##..',
            '......#.',
            '....###.',
            '...#....',
            '..##....',
            '...##...',
            '..###...',
            '.###....',]

def check_platform(pf, p):
    count = 0
    for i in range(len(p)):
        if p[i] == '#' and pf[i] == '#':
            count += 1
    return count == 0

def random_map():
    map_init = ['$$$$$$$$',
                '....###.',
                '.###....',
                '....##..']
    for i in range(42):
        p = random.choice(map_pool)
        while not check_platform(map_init[-1], p):
            p = random.choice(map_pool)
        map_init.append(p)
    map_init.append('####....')
    return map_init

def random_coin(lst):
    coin_list = []
    for i in range(40):
        p = random.choice(lst)
        if p.avaliable == True:
            p.item_on()
            c = [p.x, p.y + 105]
            index = lst.index(p)
            lst.pop(index)
            coin_list.append(c)
    return coin_list