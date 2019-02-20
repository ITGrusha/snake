from random import randint
from neuro_solver import solve
from typing import Dict, Any
import getopt, sys
from timeit import default_timer as timer

from pygame import *

# from pprint import pprint

TEXT_FOOT = 'Score: '
font_foot = font.Font
clock = time.Clock()
screen = Surface
dirs: Dict[Any, Any] = {}


def vector_sum(a: list, b: list) -> list:
    return [int(a[i]) + int(b[i]) for i in range(a.__len__())]


def vector_prod(a: list, b: list) -> int:
    res = 0
    for i in range(a.__len__()):
        res += int(a[i]) * int(b[i])
    return res


surface = Surface
legend = Surface
surface_head = Surface
surface_body = Surface
surface_tail = Surface
surface_food = Surface
rect_legend = Rect
head = list()
food = list()
tail = list()
direction_str = ''
length = 0


def init_resources(gui_enable: bool) -> bool:
    global clock
    global screen
    global surface
    global legend
    global surface_head
    global surface_body
    global surface_tail
    global surface_food
    global rect_legend
    global dirs
    global font_foot

    if gui_enable:
        screen = display.set_mode((400, 440), NOFRAME)
    dirs = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}

    if gui_enable:
        font_foot = font.SysFont('Segoe ui', 24, False, False)

        rect_legend = Rect(0, 400, 400, 40)
        rect_cage = (16, 16)

        surface_head = Surface(rect_cage)
        surface_head = image.load('../resources/smile.png').convert_alpha()
        # surface_head.fill((0, 0, 0))
        # ts = Surface((14, 14))
        # ts.fill((255, 0, 0))
        # surface_head.blit(ts, (1, 1))

        surface_body = Surface(rect_cage)
        surface_body.fill((0, 0, 0))
        ts = Surface((14, 14))
        ts.fill((0, 0, 255))
        surface_body.blit(ts, (1, 1))

        surface_tail = Surface(rect_cage)
        surface_tail.fill((0, 0, 0))
        ts = Surface((14, 14))
        ts.fill((0, 255, 0))
        surface_tail.blit(ts, (1, 1))

        surface_food = Surface(rect_cage)
        surface_food.fill((0, 0, 0))
        ts = Surface((14, 14))
        ts.fill((255, 0, 0))
        surface_food.blit(ts, (1, 1))

        surface = Surface(screen.get_size()).convert()
        surface.fill((220, 220, 220))

        legend = surface.subsurface(rect_legend).convert_alpha()
        legend.fill((0, 255, 128, 128))
    return True


def main(argv):
    gui_enable = False
    ai_enable = False
    model = None
    # print(argv)
    try:
        opts, args = getopt.getopt(argv, 'hg:m:a:', ['gui-enable=', 'model=', 'ai='])
    except getopt.GetoptError:
        print('test.py -gui <Bool>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -g   <Bool>')
            sys.exit()
        elif opt in ('-g', '--gui-enable'):
            gui_enable = arg.lower() in ['true', '1', 't', 'y', 'yes']
        elif opt in ('-m', '--model'):
            model = arg
        elif opt in ('-a', '--ai'):
            ai_enable = arg.lower() in ['true', '1', 't', 'y', 'yes']
        # print(opt, arg)

    global dirs
    global direction_str
    global length
    global head
    global tail
    global food
    # print('Initializing game')
    if gui_enable:
        init()
        # print('\tCreating resources')

    init_resources(gui_enable)
    if gui_enable:
        screen.blit(surface, (0, 0))
        screen.blit(legend, rect_legend)
        display.flip()

    # print('\tCreating game field')
    field = [[0 for _ in range(25)] for _ in range(25)]
    food = [12, 12]
    head = [16, 12]
    tail = [17, 12]
    length = 2
    direction_str = 'N'
    direction = dirs[direction_str]
    field[head[0]][head[1]] = 1
    field[tail[0]][tail[1]] = 2
    field[food[0]][food[1]] = -1

    # print('Initialization successful!')
    #
    # print('Starting game cycle')
    # print('\tTimer started')
    start = timer()
    while True:
        # global direction
        if ai_enable and not gui_enable and timer() - start >= 0.3:
            break
        dd: str = direction_str
        if ai_enable:
            dd = solve(data=summary(1), model=model)
        if (dd == 'F' and direction_str == 'N') or \
                (dd == 'R' and direction_str == 'W') or \
                (dd == 'L' and direction_str == 'E'):
            dd = 'N'
        elif (dd == 'F' and direction_str == 'E') or \
                (dd == 'R' and direction_str == 'N') or \
                (dd == 'L' and direction_str == 'S'):
            dd = 'E'
        elif (dd == 'F' and direction_str == 'W') or \
                (dd == 'R' and direction_str == 'S') or \
                (dd == 'L' and direction_str == 'N'):
            dd = 'W'
        elif (dd == 'F' and direction_str == 'S') or \
                (dd == 'R' and direction_str == 'E') or \
                (dd == 'L' and direction_str == 'W'):
            dd = 'S'
        if gui_enable:
            for event_it in event.get():
                if event_it.type == KEYDOWN:
                    if event_it.key == K_UP or event_it.key == K_w:
                        dd = 'N'
                    elif event_it.key == K_RIGHT or event_it.key == K_d:
                        dd = 'E'
                    elif event_it.key == K_DOWN or event_it.key == K_s:
                        dd = 'S'
                    elif event_it.key == K_LEFT or event_it.key == K_a:
                        dd = 'W'

        if vector_prod(dirs[dd], direction) == 0:
            direction_str = dd
            direction = dirs[direction_str]

        if gui_enable:
            screen.blit(surface, (0, 0))
            screen.blit(legend, rect_legend)
        was_ate = False
        head = vector_sum(head, direction)

        if 0 <= head[0] <= 24 and 0 <= head[1] <= 24:
            if field[head[0]][head[1]] == 0:
                field[head[0]][head[1]] = 1
            elif field[head[0]][head[1]] == -1:
                was_ate = True
                length += 1
            else:
                break
        else:
            break

        if head == food:
            was_ate = True
            while True:
                a: int = randint(0, 24)
                b: int = randint(0, 24)
                if field[a][b] == 0:
                    break
            food = [a, b]
            field[a][b] = -1

        if not was_ate:
            field[tail[0]][tail[1]] = 0
            if tail[0] + 1 <= 24 and field[tail[0] + 1][tail[1]] == length - 1:
                tail = vector_sum(tail, [1, 0])
            elif tail[0] - 1 >= 0 and field[tail[0] - 1][tail[1]] == length - 1:
                tail = vector_sum(tail, [-1, 0])
            elif tail[1] + 1 <= 24 and field[tail[0]][tail[1] + 1] == length - 1:
                tail = vector_sum(tail, [0, 1])
            elif tail[1] - 1 >= 0 and field[tail[0]][tail[1] - 1] == length - 1:
                tail = vector_sum(tail, [0, -1])

        for i in range(0, 25):
            for j in range(0, 25):
                if field[i][j] > 0:
                    field[i][j] = int(field[i][j]) + 1
        field[head[0]][head[1]] = 1
        if gui_enable:
            for i in range(0, 25):
                for j in range(0, 25):
                    t_rect = (16 * j, 16 * i, 16, 16)
                    if field[i][j] == 1:
                        screen.blit(surface_head, t_rect)
                        # print((j, i))
                    elif 2 <= field[i][j] < length:
                        screen.blit(surface_body, t_rect)
                    elif field[i][j] == length:
                        screen.blit(surface_tail, t_rect)
                    elif field[i][j] == -1:
                        screen.blit(surface_food, t_rect)
            # print(head)
            legend.fill((0, 255, 128, 128))
            legend.blit(font_foot.render(TEXT_FOOT + str(length), False, (255, 0, 0)), (6, 2))
            screen.blit(legend, rect_legend)
            display.flip()
            clock.tick(2)
        # summary(1)

    end = timer()
    if length >= 4:
        print(model)
        print('Time: {}s'.format(end - start))
        print('Length: {}'.format(length))
    return [length, end-start]


def only_pos(a: int) -> int:
    if a >= 0:
        return bool(a) * 8
    else:
        return 0


def summary(cont: bool) -> list:
    global head
    global food
    bound_front, bound_right, bound_left = 0, 0, 0
    bound_north = head[0]
    bound_west = head[1]
    bound_east = 24 - bound_west
    bound_south = 24 - bound_north
    food_right = head[1] - food[0]
    if direction_str == 'N':
        food_front = head[0] - food[0]
        food_right = - head[1] + food[1]
        bound_front = bound_north
        bound_right = bound_east
        bound_left = bound_west
    elif direction_str == 'S':
        food_front = - head[0] + food[0]
        food_right = head[1] - food[1]
        bound_front = bound_south
        bound_right = bound_west
        bound_left = bound_east
    elif direction_str == 'E':
        food_front = - head[1] + food[1]
        food_right = - head[0] + food[0]
        bound_front = bound_east
        bound_right = bound_south
        bound_left = bound_north
    elif direction_str == 'W':
        food_front = head[1] - food[1]
        food_right = head[0] - food[0]
        bound_front = bound_west
        bound_right = bound_north
        bound_left = bound_south

    food_left = - food_right
    food_back = - food_front

    result = [cont, bound_front - 23, bound_right - 23, bound_left - 23, only_pos(food_front), only_pos(food_right),
              only_pos(food_back), only_pos(food_left), length]
    # print(result)
    return result


if __name__ == '__main__':
    main(sys.argv[1:])
