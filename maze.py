# coding = utf-8
import threading

import pygame

from maze_generator import generate_maze
from maze_solver import solve_maze
from utils import stop_thread
import random

pygame.init()

# 定义一些共用属性
# 尺寸
WIDTH = 400
HEADER = 30
HEIGHT = WIDTH + HEADER
WINDOW = (WIDTH, HEIGHT)

# 标题
TITLE = "迷宫"
# 初始化界面与标题
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption(TITLE)
# 刷新相关
FPS = 60
CLOCK = pygame.time.Clock()

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_CYAN = (0, 255, 255)

FONT_SIZE = 16
FONT = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE)

BUTTONS = []

SOLVE_THREAD = None


def draw_rect(x, y, len, color):
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)


def draw_button(x, y, len, height, text):
    pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(text, True, COLOR_BLACK)
    text_len = text.__len__() * FONT_SIZE
    # 文字居中
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


def refresh():
    global MAZE, ENTRANCE, EXIT, SOLVE_THREAD
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    # 生成迷宫与入口
    size = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    SOLVE_THREAD.start()


# 绘制迷宫
def draw_maze(maze, cur_pos):
    SCREEN.fill(COLOR_WHITE)
    draw_button(2, 2, WIDTH - 4, HEADER - 4, '刷新地图')
    if len(BUTTONS) == 0:
        BUTTONS.append({
            'x': 2,
            'y': 2,
            'length': WIDTH - 4,
            'height': HEADER - 4,
            'click': refresh
        })

    size = len(maze)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2
    for y in range(size):
        for x in range(size):
            cell = maze[y][x]
            color = COLOR_BLACK if cell == 1 else COLOR_RED if cell == 3 else COLOR_CYAN if cell == 2 else COLOR_WHITE
            if x == cur_pos[1] and y == cur_pos[2]:
                color = COLOR_GREEN
            draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
    pygame.display.flip()


def dispatcher_click(pos):
    for button in BUTTONS:
        x, y, length, height = button['x'], button['y'], button['length'], button['height']
        pos_x, pos_y = pos
        if x <= pos_x <= x + length and y <= pos_y <= y + height:
            button['click']()


def random_maze_size():
    return random.randint(5, 20) * 2 + 1


if __name__ == '__main__':
    # 生成迷宫与入口
    size = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    SOLVE_THREAD.start()
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            # 检查是否关闭窗口
            if event.type == pygame.QUIT:
                if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
                    stop_thread(SOLVE_THREAD)
                    SOLVE_THREAD = None
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                dispatcher_click(mouse_pos)
