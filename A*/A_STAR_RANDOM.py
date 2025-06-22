import pygame
import math
import random
from queue import PriorityQueue


pygame.init()


GRID_SIZE = 30
CELL_SIZE = 20
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
WIN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("A*")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)


# Класс ячейки с весами
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.came_from = None
        self.is_barrier = False
        self.weight = 1
        self.font = pygame.font.SysFont('Arial', 12)

    def position(self):
        return self.row, self.col

    def start(self):
        self.color = ORANGE

    def end(self):
        self.color = TURQUOISE

    def barrier(self):
        self.color = BLACK
        self.is_barrier = True

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def path(self):
        self.color = PURPLE

    def reset(self):
        self.color = WHITE
        self.is_barrier = False
        self.weight = 1

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        if self.weight > 1 and not self.is_barrier and self.color not in [ORANGE, TURQUOISE]:
            text = self.font.render(str(self.weight), True, BLUE)
            win.blit(text, (self.x + CELL_SIZE // 2 - 5, self.y + CELL_SIZE // 2 - 5))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not grid[r][c].is_barrier:
                self.neighbors.append(grid[r][c])


# Создание сетки
def make_grid(random_map=False):
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            row.append(cell)
        grid.append(row)

    if random_map:
        generate_random_map(grid)

    return grid



def generate_random_map(grid):
    for row in grid:
        for cell in row:
            if random.random() < 0.2:
                cell.barrier()
            elif random.random() < 0.3:
                cell.weight = random.randint(2, 5)


# Отрисовка линий сетки
def draw_grid_lines(win):
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))


# Основная отрисовка
def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)
    draw_grid_lines(win)
    pygame.display.update()


# Манхэттенское расстояние
def manh(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Восстановление пути
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        current.path()
        draw_func()


# Алгоритм A*
def a_STAR(draw_func, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_hash = {start}

    start.g = 0
    start.h = manh(start.position(), end.position())
    start.f = start.g + start.h

    came_from = {}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw_func)
            start.start()
            end.end()
            return True

        current.make_closed()

        for neighbor in current.neighbors:
            temp_g = current.g + neighbor.weight

            if temp_g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = temp_g
                neighbor.h = manh(neighbor.position(), end.position())
                neighbor.f = neighbor.g + neighbor.h

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw_func()

    return False


# Основная функция
def main():
    grid = make_grid(random_map=True)

    start = grid[0][0]
    end = grid[GRID_SIZE - 1][GRID_SIZE - 1]
    start.reset()
    end.reset()
    start.start()
    end.end()

    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)

    run = True
    started = False

    while run:
        draw(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    a_STAR(lambda: draw(WIN, grid), grid, start, end)
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_n:
                    grid = make_grid(random_map=True)
                    start = grid[0][0]
                    end = grid[GRID_SIZE - 1][GRID_SIZE - 1]
                    start.reset()
                    end.reset()
                    start.start()
                    end.end()
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    started = False

    pygame.quit()


main()