"""
Модуль для запуска программы
"""
import os
import argparse
from compress import image_compression


def main() -> None:
    """
    В этой функции происходит запусмк программы
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", '--image_path', type=str,
                        help="Путь к изображению", required=True)
    parser.add_argument("-cr", '--compression_ratio', type=int,
                        help="Степень сжатия")
    parser.add_argument("-b", '--borders', action="store_true",
                        help="Отображение границ")
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print("Указан неверный путь")
        return
    else:
        image_compression(args.image_path, args.compression_ratio, args.borders)


if __name__ == "__main__":
    main()
