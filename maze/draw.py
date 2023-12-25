"""
Модуль содержит функции для реализации отображения
кратчайшего пути в лабиринте
"""

import pygame

WALL = (0, 0, 0)
PASSAGE = (255, 255, 255)
PATH_COLOR = (3, 61, 252)


def maze_init(window, maze, scale):
    """
    Метод инициализирует лабиринт, т.е рисует его стены
    @:param window: главный экран
    @:param maze: сгенерированный лабиринт
    @:param scale: размер одной ячейки лабиринта
    """
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '1':
                pygame.draw.rect(window, WALL, (j * scale, i * scale, scale, scale))
            else:
                pygame.draw.rect(window, PASSAGE, (j * scale, i * scale, scale, scale))

    pygame.display.flip()


# def draw_path(window, solution, scale):
#     """
#     Пошагово отображает решение лабиринта
#     @:param window: главный экран
#     @:param solution: Список с решением лабиринта
#     @:param scale: размер одной ячейки лабиринта
#     """
#     if not solution:
#         return
#     prev = None
#     # Рисуем решение лабиринта
#     for point in solution:
#         pygame.draw.circle(window, PATH_COLOR,
#                            (int(point[1] * scale + scale / 2), int(point[0] * scale + scale / 2)),
#                            scale // 4)  # Радиус точки задан как четверть размера ячейки
#         if prev:
#             pygame.draw.circle(window, PATH_COLOR,
#                                (int(prev[1] * scale + scale / 2), int(prev[0] * scale + scale / 2)),
#                                scale // 4)
#         pygame.display.flip()
#         pygame.time.wait(80)
#         prev = point
def draw_path(window, solution, scale):
    """
    Пошагово отображает решение лабиринта
    @:param window: главный экран
    @:param solution: Список с решением лабиринта
    @:param scale: размер одной ячейки лабиринта
    """
    if not solution:
        return
    # Рисуем решение лабиринта
    for point in solution:
        pygame.draw.circle(window, PATH_COLOR,
                           (int(point[1] * scale + scale / 2), int(point[0] * scale + scale / 2)), scale // 3)
        pygame.display.flip()
        pygame.time.wait(120)


def start(maze: list, solution: list = None, image_path: str = None) -> None:
    """
    Функция запускает графическое отображение лабиринта
    @:param maze: сгенерированный лабиринт
    @:param solution: решение лабиринта
    @:param img_path: путь сохраняемого изображения
    """
    pygame.init()
    pygame.display.set_caption('Лабиринт')
    width = len(maze[0])
    height = len(maze)
    scale = 800 // height if height >= width else 900 // width

    # Создаем окно
    screen = pygame.display.set_mode((width * scale, height * scale))
    maze_init(screen, maze, scale)
    draw_path(screen, solution, scale)

    # Ожидание закрытия окна
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    if image_path is not None:
        screenshot = pygame.Surface((width * scale, height * scale))
        screenshot.blit(screen, (0, 0))
        pygame.image.save(screenshot, image_path)

    pygame.quit()
