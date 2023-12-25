"""
Модуль содержит функции генерации и решения лабиринта
"""

import random
import heapq


def labyrinth_generation(width: int, height: int) -> list:
    """
    Генерирует лабиринт при помощи метода двоичного дерева
    @:param width: ширина генерируемого лабиринта
    @:param height: высота генерируемого лабиринта
    @:return: созданный лабиринт
    """
    if (width < 1) or (height < 1):
        return None
    # top_limit = 2 ** 32 - 1
    # # Проверка на ограничение по максимальному допустимому размеру
    # if ((top_limit - 1) // 2 <= width) or ((top_limit - 1) // 2 <= height):
    #     return None
    output_height = height * 2 + 1
    output_width = width * 2 + 1
    maze = [['1' for _ in range(output_width)] for _ in range(output_height)]
    for i in range(1, output_height, 2):
        for j in range(1, output_width, 2):
            # Если этот элемент в строке является ячейкой в левом верхнем
            # угле области 2x2 - то это пустая ячейка в лабиринте
            maze[i][j] = ' '
            if i + 2 == output_height and not j + 2 == output_width:
                maze[i][j + 1] = ' '
            elif j + 2 == output_width and not i + 2 == output_height:
                maze[i + 1][j] = ' '
            elif not (i + 2 == output_height or j + 2 == output_width):
                bottom = random.randint(0, 1)
                maze[i + 1][j] = ' ' if bottom else '1'
                maze[i][j + 1] = ' ' if not bottom else '1'
    return maze


def is_valid(x: int, y: int, maze: list) -> bool:
    """
    Функция для проверки валидности следующей позиции
    :param x: координата х
    :param y: координата у
    :param maze: лабиринт
    :return: валидность следующей позиции
    """
    return 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != '1'


def maze_solution(maze: list) -> list:
    """
    Решение лабиринта при помощи алгоритма дейкстры
    :param maze: лабиринт в виде вложенных списков
    :return: список с кортежами, в кортежах точки решения лабиринта
    """
    start = (1, 1)
    end = (len(maze) - 2, len(maze[0]) - 2)
    # Возможные направления движения (вправо, влево, вниз, вверх)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Инициализация расстояний до всех точек
    distances = {pos: float('inf') for pos in [(i, j) for i in range(len(maze)) for j in range(len(maze[0]))]}
    distances[start] = 0

    # Очередь с приоритетами для хранения точек и расстояний до них
    pq = [(0, start)]

    while pq:
        dist, current = heapq.heappop(pq)
        if current == end:
            # Возвращаем кратчайший путь при достижении конечной точки
            path = [end]
            while path[-1] != start:
                for dx, dy in directions:
                    nx, ny = path[-1][0] + dx, path[-1][1] + dy
                    if is_valid(nx, ny, maze) and distances[path[-1]] - 1 == distances[(nx, ny)]:
                        path.append((nx, ny))
                        break
            # Возвращаем кратчайщий путь алгоритма
            return path[::-1]

        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            # Расстояние до соседа (единица, т.к. клетки имеют единичный шаг)
            new_distance = dist + 1

            if is_valid(nx, ny, maze) and new_distance < distances[(nx, ny)]:
                distances[(nx, ny)] = new_distance
                heapq.heappush(pq, (new_distance, (nx, ny)))

    return []
