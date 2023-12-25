"""
Модуль для запуска алгоритма
"""
import argparse

from my_sort import my_sort


def main() -> None:
    """
    Метод, в котором запускается алгоритм
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--array', nargs="+", help="Элементы списка,вводятся через пробел")
    parser.add_argument('-t', '--type', choices=['int', 'str'],
                        help="Тип элементов списка: 'int' или 'str'")

    parser.add_argument('-r', '--reverse', action='store_true',
                        help="Флаг, определяющий вариант сортировки")
    parser.add_argument('-l', '--length', action='store_true',
                        help="Флаг, для сортировки строк по их длине")

    args = parser.parse_args()
    if args.array is None:
        print("Введите список")
        return
    array = []
    if args.type.lower() == 'int':
        array = list(map(int, args.array))
    else:
        array = args.array
    if args.type.lower() == 'int':
        print(f"Отсортированный список: {my_sort(array, reverse=args.reverse)}")
        return
    if args.length:
        print(f"Отсортированный список: {my_sort(array,key=len,reverse=args.reverse)}")
        return
    print(f"Отсортированный список: {my_sort(array, reverse=args.reverse)}")


if __name__ == '__main__':
    main()
