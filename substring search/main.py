"""
Главный модуль, именно в нем происходит запуск поиска
"""


import argparse
import os

from search import search


def read_file(file_path: str) -> list:
    """
    Функция считывает содержимое из файла,
    и возвращает результат в виде списка
    Args:
        file_path: Путь к файлу
    returns: Список со словами в файле
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def main():
    """
    Главый метод всей программы
    В нем происходит считывание параметров из консоли и запуск поиска
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--string', help='Исходная строка, в которой будет происходить поиск')
    parser.add_argument('-sb', '--sub_string', nargs='+',
                        help='Одна или несколько подстрок, которые необходимо найти')
    parser.add_argument('-cs', '--case_sensitivity', action='store_true',
                        help='Флаг чувствительности к регистру')
    parser.add_argument('-m', '--method',
                        help="Метод поиска. first -> поиск идет в прямом порядке, "
                             "last -> поиск идет в обратном порядке")
    parser.add_argument('-c', '--count', type=int, default=None,
                        help='Количество совпадений k, которые нужно найти. '
                             'Если его не передать, то будут искаться все вхождения')
    parser.add_argument('-fp', '--file_path', help='Путь к файлу, в котором будет проходить поиск')

    args = parser.parse_args()

    if args.string:
        string = args.string
        print(search(string, args.sub_string, args.case_sensitivity, args.method, args.count))

    elif args.file_path:
        if not os.path.isfile(args.file_path):
            print("Указан неверный путь к файлу")
            return
        string = read_file(args.file_path)
        string = ''.join(string)
        if not string:
            print("Пустой файл")
            return
        print(search(string, args.sub_string, args.case_sensitivity, args.method, args.count))

    else:
        print("Не указана строка для поиска")
        return


if __name__ == '__main__':
    main()
