from typing import Dict, Any

from pygame import *
from random import randint
# from pprint import pprint

TEXT_FOOT = "Score: "
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


def init_resources() -> bool:
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

    screen = display.set_mode((400, 440), NOFRAME)
    dirs = {"N": [-1, 0], "E": [0, 1], "S": [1, 0], "W": [0, -1]}
    font_foot = font.SysFont("Segoe ui", 24, False, False)

    rect_legend = Rect(0, 400, 400, 40)
    rect_cage = (16, 16)

    surface_head = Surface(rect_cage)
    surface_head = image.load("../resources/smile.png").convert_alpha()
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


def main():
    global dirs
    print("Initializing game")
    init()
    print("\tCreating resources")

    init_resources()
    screen.blit(surface, (0, 0))
    screen.blit(legend, rect_legend)
    display.flip()
    print("\tCreating game field")
    field = [[0 for _ in range(25)] for _ in range(25)]
    food = [12, 12]
    head = [16, 12]
    tail = [17, 12]
    length = 2
    direction = dirs["N"]
    field[head[0]][head[1]] = 1
    field[tail[0]][tail[1]] = 2
    field[food[0]][food[1]] = -1
    print("Initialization successful!")

    print("Starting game cycle")
    while True:
        # global direction
        dd: list = direction
        for event_it in event.get():
            if event_it.type == KEYDOWN:
                if event_it.key == K_UP or event_it.key == K_w:
                    dd = dirs["N"]
                elif event_it.key == K_RIGHT or event_it.key == K_d:
                    dd = dirs["E"]
                elif event_it.key == K_DOWN or event_it.key == K_s:
                    dd = dirs["S"]
                elif event_it.key == K_LEFT or event_it.key == K_a:
                    dd = dirs["W"]
        if vector_prod(dd, direction) == 0:
            direction = dd

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
                return False
        else:
            return False

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
        legend.blit(font_foot.render(TEXT_FOOT + str(length), True, (255, 0, 0)), (6, 2))
        screen.blit(legend, rect_legend)
        display.flip()
        clock.tick(2)


if __name__ == '__main__':
    main()
