import pygame
import math
from queue import PriorityQueue

# Инициализируем библиотеку Pygame для работы с графикой

# Настройки окна
GRID_SIZE = 10  #Размер сетки 10x10
CELL_SIZE = 50
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

# Класс ячейки
class Cell:
    def __init__(self, row, col):
        self.row = row  # Номер строки ячейки
        self.col = col  # Номер столбца ячейки
        self.x = row * CELL_SIZE  # Координата x для отрисовки
        self.y = col * CELL_SIZE  # Координата y для отрисовки
        self.color = WHITE  # Начальный цвет ячейки (пустая)
        self.neighbors = []  # Список соседних ячеек
        self.g = float("inf")  # Начальная стоимость пути от старта (бесконечность)
        self.h = 0  # Эвристическая оценка до цели
        self.f = float("inf")  # Полная оценка (g + h)
        self.came_from = None  # Родительская ячейка для восстановления пути
        self.is_barrier = False  # Флаг, обозначающий препятствие

    def position(self):
        return self.row, self.col  # Возвращает позицию ячейки (row, col)

    def start(self):
        self.color = ORANGE  # Устанавливает цвет как начальную точку

    def end(self):
        self.color = TURQUOISE  # Устанавливает цвет как конечную точку

    def barrier(self):
        self.color = BLACK  # Устанавливает цвет как препятствие
        self.is_barrier = True  # Помечает ячейку как препятствие

    def make_open(self):
        self.color = GREEN  # Устанавливает цвет для ячеек в очереди

    def make_closed(self):
        self.color = RED  # Устанавливает цвет для посещённых ячеек

    def path(self):
        self.color = PURPLE  # Устанавливает цвет для итогового пути

    def reset(self):
        self.color = WHITE  # Сбрасывает цвет в исходное состояние
        self.is_barrier = False  # Снимает флаг препятствия

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))  # Отрисовка ячейки

    def update_neighbors(self, grid):
        self.neighbors = []  # Очищаем список соседей
        # Проверяем соседей (вверх, вниз, влево, вправо)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc  # Вычисляем координаты соседей
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not grid[r][c].is_barrier:
                self.neighbors.append(grid[r][c])  # Добавляем допустимых соседей

# Создание сетки
def make_grid():
    grid = []  # Инициализируем список для сетки
    for i in range(GRID_SIZE):
        row = []  # Создаём строку
        for j in range(GRID_SIZE):
            cell = Cell(i, j)  # Создаём ячейку
            row.append(cell)  # Добавляем ячейку в строку
        grid.append(row)  # Добавляем строку в сетку
    return grid  # Возвращаем созданную сетку

# Отрисовка линий сетки
def draw_grid_lines(win):
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE))  # Горизонтальные линии
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE))  # Вертикальные линии

# Отрисовка всего
def draw(win, grid):
    win.fill(WHITE)  # Заполняем окно белым фоном
    for row in grid:
        for cell in row:
            cell.draw(win)  # Отрисовываем каждую ячейку
    draw_grid_lines(win)  # Рисуем линии сетки
    pygame.display.update()  # Обновляем дисплей

# Манхэттенское расстояние
def manh(p1, p2):
    x1, y1 = p1  # Координаты первой точки
    x2, y2 = p2  # Координаты второй точки
    return abs(x1 - x2) + abs(y1 - y2)  # Вычисляем манхэттенское расстояние

# Восстановление пути
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:  # Пока есть родительская ячейка
        current = came_from[current]  # Переходим к родителю
        current.path()  # Помечаем ячейку как часть пути
        draw_func()  # Обновляем визуализацию

# A*
def a_STAR(draw_func, grid, start, end):
    count = 0  # Счётчик для разрешения конфликтов в PriorityQueue
    open_set = PriorityQueue()  # Создаём очередь с приоритетом для открытых узлов
    open_set.put((0, count, start))  # Добавляем начальную точку с f=0
    open_set_hash = {start}  # Множество для быстрого поиска узлов в open_set

    start.g = 0  # Устанавливаем стоимость пути от старта до старта
    start.h = manh(start.position(), end.position())  # Вычисляем эвристику до цели
    start.f = start.g + start.h  # Вычисляем полную оценку f

    came_from = {}  # Словарь для хранения родительских узлов

    while not open_set.empty():
        for event in pygame.event.get():  # Проверяем события
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Прерываем алгоритм

        current = open_set.get()[2]  # Извлекаем узел с минимальным f
        open_set_hash.remove(current)  # Удаляем его из множества

        if current == end:  # Если достигли цели
            reconstruct_path(came_from, end, draw_func)  # Восстанавливаем путь
            start.start()  # Восстанавливаем цвет начальной точки
            end.end()  # Восстанавливаем цвет конечной точки
            return True  # Успешное завершение

        current.make_closed()  # Помечаем текущую ячейку как посещённую

        for neighbor in current.neighbors:  # Проверяем всех соседей
            temp_g = current.g + 1  # Увеличиваем стоимость пути на 1
            if temp_g < neighbor.g:  # Если новый путь короче
                came_from[neighbor] = current  # Запоминаем родителя
                neighbor.g = temp_g  # Обновляем стоимость пути
                neighbor.h = manh(neighbor.position(), end.position())  # Обновляем эвристику
                neighbor.f = neighbor.g + neighbor.h  # Обновляем полную оценку

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((neighbor.f, count, neighbor))  # Добавляем в очередь
                    open_set_hash.add(neighbor)  # Добавляем в множество
                    neighbor.make_open()  # Помечаем как открытый

        draw_func()  # Обновляем визуализацию

    return False  # Путь не найден

# Основная функция
def main():
    grid = make_grid()  # Создаём сетку
    obstacles = [
        (8, 0), (9, 0), (8, 1), (9, 1),
        (0, 2), (4, 2), (0, 3), (8, 4),
        (9, 4), (8, 1), (4, 2), (1, 9),
        (8, 4), (9, 4), (0, 5), (7, 9),
        (2, 5), (7, 5), (9, 5), (0, 6),
        (2, 6), (5, 6), (7, 6), (9, 6),
        (0, 7), (1, 7), (3, 7), (4, 8),
        (8, 8), (0, 9)
    ]  # Список координат препятствий
    for row, col in obstacles:
        grid[row][col].barrier()  # Помечаем ячейки как препятствия

    # Установка начальной и конечной точек
    start = grid[0][1]  # Начальная точкв
    end = grid[9][9]    # Конечная точка
    start.start()  # Помечаем начальную точку
    end.end()  # Помечаем конечную точку

    # Обновление соседей для всех ячеек
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid)  # Обновляем список соседей

    run = True  # Флаг для работы основного цикла
    started = False  # Флаг для запуска алгоритма

    while run:  # Основной цикл программы
        draw(WIN, grid)  # Отрисовываем текущее состояние
        for event in pygame.event.get():  # Проверяем события
            if event.type == pygame.QUIT:
                run = False  # Завершаем цикл

            if event.type == pygame.KEYDOWN:  # Обработка нажатий клавиш
                if event.key == pygame.K_SPACE and not started:  # Нажата клавиша пробела
                    started = True
                    a_STAR(lambda: draw(WIN, grid), grid, start, end)
                if event.key == pygame.K_r:  # Нажата клавиша R
                    main()  # Перезапускаем программу

    pygame.quit()

main()