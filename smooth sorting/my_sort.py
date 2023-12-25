"""
Модуль алгоритма плавной сортировки
"""

from typing import List, Tuple, Callable


def getting_leonardo_numbers(max_element: int) -> List[int]:
    """
    Получение чисел Леонардо
    Числа Леонардо — последовательность чисел, задаваемая зависимостью:
    1, если n == 0 или 1
    L(n-1) + L(n-2) + 1, если n > 1
    :param max_element: Число, до которого нужно посчитать числа
    :return: Список с числами Леонардо
    """
    current, next_item = 1, 1
    numbers = []
    while current <= max_element:
        numbers.append(current)
        current, next_item = next_item, current + next_item + 1
    return numbers


def restore_heap(lst: List[int], i: int, heap: List[int], leo_nums: List[int], key: Callable,
                 # pylint: disable=R0913
                 cmp: Callable, ) -> None:
    """
    Восстанавливает кучу для плавной сортировки.

    Переупорядочивает элементы массива, чтобы поддерживать
    структуру кучи для алгоритма плавной сортировки.

    Аргументы:
    lst (List[int]): Исходный массив.
    i (int): Индекс текущего элемента.
    heap (List[int]): Куча для плавной сортировки.
    leo_nums (List[int]): Список чисел Леонардо.
    key (Callable): Функция-ключ для сравнения элементов.
    cmp (Callable): Функция для сравнения элементов.
    reverse (bool): Флаг, указывающий направление сортировки.

    Возвращает:
    None
    """
    current_heap_size = len(heap) - 1
    current_heap_index = heap[current_heap_size]

    while current_heap_size > 0:
        jump = i - leo_nums[current_heap_index]
        if cmp(key(lst[jump]), key(lst[i])) and (
                current_heap_index < 2 or
                cmp(key(lst[jump]), key(lst[i - 1])) and cmp(key(lst[jump]), key(lst[i - 2]))
        ):
            lst[i], lst[jump] = lst[jump], lst[i]
            i = jump
            current_heap_size -= 1
            current_heap_index = heap[current_heap_size]
        else:
            break

    while current_heap_index >= 2:
        right_child_index, right_child_heap_index, left_child_index, left_child_heap_index = \
            get_child_trees(
                i, current_heap_index, leo_nums
            )
        if not cmp(key(lst[i]), key(lst[right_child_index])) or not cmp(key(lst[i]),
                                                                        key(lst[left_child_index])):
            if cmp(key(lst[right_child_index]), key(lst[left_child_index])):
                lst[i], lst[right_child_index] = lst[right_child_index], lst[i]
                i, current_heap_index = right_child_index, right_child_heap_index
            else:
                lst[i], lst[left_child_index] = lst[left_child_index], lst[i]
                i, current_heap_index = left_child_index, left_child_heap_index
        else:
            break


def get_child_trees(i: int, k: int, leo_nums: List[int]) -> Tuple[int, int, int, int]:
    """
    Получает индексы потомков в куче для плавной сортировки.

    Аргументы:
    i (int): Индекс текущего элемента.
    k (int): Индекс текущего элемента в куче.
    leo_nums (List[int]): Список чисел Леонардо.

    Возвращает:
    Tuple[int, int, int, int]: Индексы правого и левого потомков и их индексы в куче.
    """
    right_child_index = i - 1
    right_child_heap_index = k - 2
    left_child_index = right_child_index - leo_nums[right_child_heap_index]
    left_child_heap_index = k - 1
    return right_child_index, right_child_heap_index, left_child_index, left_child_heap_index


def my_sort(array: list, reverse=False, key=lambda x: x, cmp=lambda x, y: x < y) -> List:
    """
    Функция реализует сортировку списка методом плавной сортировки
    :param array: Список, который надо отсортировать
    :param reverse: Флаг, определяющий вариант сортировки
    :param key: Функция, вычисляющая значение, на основе которого будет производится сортировка
    :param cmp: Функция сравнения
    :return: Отсортированный список
    """
    if not array:
        return []
    if cmp(1, 2) == (lambda x, y: x < y)(1, 2):  # pylint: disable=C3002
        cmp = lambda x, y: x > y  # pylint: disable=C3001
    else:
        cmp = lambda x, y: x < y  # pylint: disable=C3001
    leo_nums = getting_leonardo_numbers(len(array))
    heap = []

    for i in range(len(array)):
        if len(heap) >= 2 and heap[-2] == heap[-1] + 1:
            heap.pop()
            heap[-1] += 1
        else:
            if len(heap) >= 1 and heap[-1] == 1:
                heap.append(0)
            else:
                heap.append(1)
        restore_heap(array, i, heap, leo_nums, key, cmp)

    for i in reversed(range(len(array))):
        if heap[-1] < 2:
            heap.pop()
        else:
            k = heap.pop()
            t_r, k_r, t_l, k_l = get_child_trees(i, k, leo_nums)
            heap.append(k_l)
            restore_heap(array, t_l, heap, leo_nums, key, cmp)
            heap.append(k_r)
            restore_heap(array, t_r, heap, leo_nums, key, cmp)

    return array if not reverse else array[::-1]
