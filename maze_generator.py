# coding=utf-8
from random import randint, choice


# 单元格类型
# 0 - 路，1 - 墙
class CellType:
    ROAD = 0
    WALL = 1


# 墙的方向
class Direction:
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3,


# 迷宫地图
class Maze:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[0 for x in range(self.width)] for y in range(self.height)]

    def reset_maze(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.set_maze(x, y, value)

    def set_maze(self, x, y, value):
        self.maze[y][x] = CellType.ROAD if value == CellType.ROAD else CellType.WALL

    def visited(self, x, y):
        return self.maze[y][x] != 1


def check_neighbors(maze, x, y, width, height, checklist):
    directions = []
    if x > 0:
        if not maze.visited(2 * (x - 1) + 1, 2 * y + 1):
            directions.append(Direction.LEFT)
    if y > 0:
        if not maze.visited(2 * x + 1, 2 * (y - 1) + 1):
            directions.append(Direction.UP)
    if x < width - 1:
        if not maze.visited(2 * (x + 1) + 1, 2 * y + 1):
            directions.append(Direction.RIGHT)
    if y < height - 1:
        if not maze.visited(2 * x + 1, 2 * (y + 1) + 1):
            directions.append(Direction.DOWN)
    if len(directions):
        direction = choice(directions)
        if direction == Direction.LEFT:
            maze.set_maze(2 * (x - 1) + 1, 2 * y + 1, CellType.ROAD)
            maze.set_maze(2 * x, 2 * y + 1, CellType.ROAD)
            checklist.append((x - 1, y))
        elif direction == Direction.UP:
            maze.set_maze(2 * x + 1, 2 * (y - 1) + 1, CellType.ROAD)
            maze.set_maze(2 * x + 1, 2 * y, CellType.ROAD)
            checklist.append((x, y - 1))
        elif direction == Direction.RIGHT:
            maze.set_maze(2 * (x + 1) + 1, 2 * y + 1, CellType.ROAD)
            maze.set_maze(2 * x + 2, 2 * y + 1, CellType.ROAD)
            checklist.append((x + 1, y))
        elif direction == Direction.DOWN:
            maze.set_maze(2 * x + 1, 2 * (y + 1) + 1, CellType.ROAD)
            maze.set_maze(2 * x + 1, 2 * y + 2, CellType.ROAD)
            checklist.append((x, y + 1))
        return True
    return False


def random_prime(map, width, height):
    start_x, start_y = (randint(0, width - 1), randint(0, height - 1))
    map.set_maze(2 * start_x + 1, 2 * start_y + 1, CellType.ROAD)
    checklist = [(start_x, start_y)]
    while len(checklist):
        entry = choice(checklist)
        if not check_neighbors(map, entry[0], entry[1], width, height, checklist):
            checklist.remove(entry)


def do_random_prime(map):
    map.reset_maze(CellType.WALL)
    random_prime(map, (map.width - 1) // 2, (map.height - 1) // 2)


def set_entrance_exit(maze):
    entrance = []
    for i in range(maze.height):
        if maze.maze[i][1] == 0:
            maze.set_maze(0, i, 0)
            entrance = [0, i]
            break
    exit = []
    for i in range(maze.height - 1, 0, -1):
        if maze.maze[i][maze.width - 2] == 0:
            maze.set_maze(maze.width - 1, i, 0)
            exit = [maze.width - 1, i]
            break
    return entrance, exit


def generate_maze(width=21, height=21):
    # 初始化迷宫
    maze = Maze(width, height)
    # 生成地图
    do_random_prime(maze)
    # 选择起点和终点
    entrance, exit = set_entrance_exit(maze)
    # 返回地图
    return maze.maze, entrance, exit
