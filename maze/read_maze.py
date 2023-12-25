"""
Модуль содержит функции для работы с текстовыми данными
"""


def read_txt_maze(file_path: str) -> list:
    """
    Функция считывает лабиринт из текстового файла
    :param file_path: Путь текстового файла
    :return: Лабиринт в виде вложенных списков
    """
    maze = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                maze.append(list(line.strip()))
    return maze


def save_txt_maze(maze_path: list, file_path: str) -> None:
    """
    Функция сохраняет лабиринт в виде текста
    :param maze_path: Лабиринт
    :param file_path: путь для сохранения
    :return:
    """
    maze = ''
    for index, item in enumerate(maze_path):
        if index != 0:
            maze += '\n'
        for j in item:
            maze += j
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(maze)
