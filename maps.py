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

map_init = ['....##..',
            '.###....',
            '....###.',
            '$$$$$$$$']

def check_platform(pf, p):
    count = 0
    for i in range(8):
        if p[i] == '#' and pf[i] == '#':
            count += 1
    return count == 0

def random_map(lst):
    right = map_pool[:5]
    left = map_pool[5:]
    while len(lst) != 41:
        p = random.choice(map_pool)
        if lst[0] != lst[1] != lst[2] != p:
            if check_platform(lst[0], p):
                if p in right and lst[0] not in right:
                    lst.insert(0, p)
                elif p in left and lst[0] not in left:
                    lst.insert(0, p)
    lst.insert(0, '####....')
    return lst

def random_coin(lst):
    coin_list = []
    while len(coin_list) != 40:
        p = random.choice(lst)
        if p.avaliable == True:
            p.item_on()
            c = [p.x, p.y + 105]
            coin_list.append(c)
    return coin_list