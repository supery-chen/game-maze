import time


# 单元格类型
# 0 - 路，1 - 墙，2-走过的路，4-死胡同
class CellType:
    ROAD = 0
    WALL = 1
    WALKED = 2
    DEAD = 3


# 墙的方向
class Direction:
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3,


def valid(maze, x, y):
    if x < 0 or y < 0:
        return False
    if x >= len(maze) or y >= len(maze):
        return False
    val = maze[y][x]
    if val == CellType.WALL or val == CellType.DEAD:
        return False
    return val, x, y


def neighbors(maze, pos):
    x, y = pos
    t, r, d, l = valid(maze, x, y - 1), valid(maze, x + 1, y), valid(maze, x, y + 1), valid(maze, x - 1, y)
    return t, r, d, l


def mark_walked(maze, pos):
    maze[pos[1]][pos[0]] = CellType.WALKED


def mark_dead(maze, pos):
    maze[pos[1]][pos[0]] = CellType.DEAD


def suggest_pos(cells):
    arr = []
    for cell in cells:
        if cell:
            arr.append(cell[0])
        else:
            arr.append(CellType.DEAD)
    return cells[arr.index(min(arr))]


def solve_maze(maze, pos, end, callback):
    time.sleep(0.05)
    # 到达出口
    if pos[0] == end[0] and pos[1] == end[1]:
        mark_walked(maze, pos)
        return True
    # 获取相邻4个位置
    t, r, d, l = neighbors(maze, pos)
    next_pos = suggest_pos((t, r, d, l))
    if next_pos:
        if next_pos[0] == CellType.WALKED:
            mark_dead(maze, pos)
        else:
            mark_walked(maze, pos)
        callback(maze, next_pos)
        return solve_maze(maze, (next_pos[1], next_pos[2]), end, callback)
    else:
        mark_dead(maze, pos)
        callback(maze, next_pos)
        return False
