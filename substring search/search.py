"""Модуль для поиска подстроки в строке"""
import logging
from time import time
from typing import Optional, Union

from aho_corasick import Trie

logging.basicConfig(level=logging.INFO, filename="logs.log", filemode='a')


def timing_decorator(func):
    """
    Функция измеряет время работы алгоритма поиска подстроки в строке
    Результат записывает в файл logs.log
    """

    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)  # Вызываем функцию и сохраняем результат
        end = time()
        execution = end - start
        logging.info('Lead time -> %s seconds\n', execution)
        return result

    return wrapper


@timing_decorator
def search(string: str, sub_string: Union[str, list[str]],  # pylint: disable=R0912, R1710
           case_sensitivity: bool, method: str, count: Optional[int] = None) -> \
        Optional[Union[tuple[int, ...], dict[str, tuple[int, ...]]]]:
    """
    Функция реализует поиск подстроки в строке, используя алгоритм Ахо-Корасик
    В качестве результата возвращает кортеж с индексами вхождений, если кол-во подстрок равно 1
    В противном случае возвращает словарь, где ключ - это подстрока, а значение - кортеж с индексами
    """
    if not string:
        return

    if isinstance(sub_string, str):
        sub_string = [sub_string]
    else:
        sub_string = list(sub_string)

    if not case_sensitivity:
        string = string.lower()
        sub_string = [item.lower() for item in
                      sub_string]  # Переводим все элементы в нижний регистр

    if method == 'last':
        if isinstance(sub_string, str):
            sub_string = sub_string[::-1]
        else:
            sub_string = [item[::-1] for item in sub_string]

    # Словарь для хранения найденных подстрок и их позиций
    if method == 'last':
        results = {key[::-1]: None for key in sub_string}
    else:
        results = dict.fromkeys(sub_string)

    trie = Trie()

    for item in sub_string:
        trie.add(item)

    vertex = trie.root

    total_count = 0  # Общее кол-во вхождений

    for i in range(len(string)):  # pylint: disable=C0200
        if method == 'last':
            i = len(string) - 1 - i
        vertex = trie.transition_to_symbol(vertex, string[i])
        if vertex.is_terminal and (count is None or total_count < count):
            if method != 'last':
                substring = string[i - vertex.length + 1:   i + 1]  # подстрока
                index = i - vertex.length + 1  # индекс
            else:
                substring = string[i: i + vertex.length]
                index = i
            if results.get(substring) is not None:
                results[substring] += (index,)
            else:
                results[substring] = (index,)
            total_count += 1

    if not results:
        return None
    if len(results) == 1:
        key = list(results.keys())[0]
        return results[key]

    # Принимает False, значения всех ключей None
    all_values_are_none = all(value is None for value in results.values())
    return None if all_values_are_none else results
