"""Тесты для модуля maze"""
import pytest
from pytest_mock import MockerFixture
from maze import *


@pytest.mark.parametrize(
    argnames=[
        "height",
        "width",
        "maze",
        "solution",
    ],
    argvalues=[
        [
            3,  #
            3,
            [
                ['1', '1', '1', '1', '1', '1', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', ' ', ' ', ' ', ' ', '1'],
                ['1', '1', '1', '1', '1', '1', '1']
            ],
            (
                    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (5, 2),
                     (5, 3), (5, 4), (5, 5)]
            )
        ],
        [
            2,
            4,
            [
                ['1', '1', '1', '1', '1', '1', '1', '1', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', '1', ' ', '1', ' ', '1', ' ', '1'],
                ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
                ['1', '1', '1', '1', '1', '1', '1', '1', '1']
            ],
            (
                    [(1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
                     (3, 6), (3, 7)]
            )
        ],
        [
            1,
            1,
            [
                ['1', '1', '1'],
                ['1', ' ', '1'],
                ['1', '1', '1']
            ],
            (
                    [(1, 1)]
            ),
        ],
    ]
)
def test_generation_and_solution(mocker: MockerFixture, height: int, width: int,
                                 maze: list, solution: list) -> None:
    """
    Функция для тестирования генерации и решения лабиринта.
    :param mocker: Позволяет подменять результаты других функций на фиктивные
    :param height: Высота
    :param width: Ширина
    :param maze: Ожидаемый лабиринт
    :param solution: Ожидаемое решение
    :return: None
    """
    mocker.patch(
        "random.randint",
        side_effect=lambda a, b: b
    )
    actual_maze = labyrinth_generation(width, height)
    actual_solution = maze_solution(actual_maze)
    assert all([maze == actual_maze, solution == actual_solution])
