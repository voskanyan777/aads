"""
Модуль для запуска программы
"""
import argparse
from draw import start
from maze import labyrinth_generation, maze_solution
from read_maze import read_txt_maze, save_txt_maze


def main() -> None:
    """
    Функция для запуска программы
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--width', type=int, help="ширина лабиринта")
    parser.add_argument('-ht', '--height', type=int, help="высота лабиринта")
    parser.add_argument('-sl', '--save_labyrinth', action='store_true',
                        help="Флаг для сохранения лабиринта в виде изображения")
    parser.add_argument('-st', '--save_text', action='store_true',
                        help="Флаг для сохранения лабиринта в виде текста")
    parser.add_argument('-fp', '--file_path', type=str, help="Путь для сохранения файла")
    parser.add_argument('-ff', '--from_file', type=str,
                        help="Путь текстового файла, из которого надо загрузить лабиринт")
    parser.add_argument('-fi', '--from_image', type=str,
                        help="Путь изображения, из которого надо загрузить лабиринт")
    parser.add_argument('-po', '--path_output', action='store_true', help='Флаг для вывода кратчайшего пути в консоль ')
    args = parser.parse_args()
    if args.width and args.height:
        maze = labyrinth_generation(args.width, args.height)
        path = maze_solution(maze)
        if args.path_output:
            print(path)
        if args.save_labyrinth and args.file_path:
            if not args.file_path.endswith(('.png', '.jpg')):
                print("Неверное расширение файла")
                return
            start(maze, path, image_path=args.file_path)
        else:
            start(maze, path)
        if args.save_text and args.file_path:
            save_txt_maze(maze, args.file_path)
    if args.from_file:
        maze = read_txt_maze(args.from_file)
        path = maze_solution(maze)
        if args.path_output:
            print(path)
        start(maze, path)


if __name__ == '__main__':
    main()
