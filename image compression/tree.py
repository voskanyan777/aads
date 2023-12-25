"""
Модуль содержит классы для реализации квадродерева
"""

import average_color
import threading
from PIL import Image


class Point:
    """Класс точки"""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y


class QuadtreeNode:
    """
    Класс узла квадродерева
    """

    def __init__(self, image: Image, coordinate_region: tuple, depth: int) -> None:
        """
        Конструктор узла квадродерева
        :param image: Изображение
        :param coordinate_region: Координатная область
        :param depth: Глубина
        """
        # дочерние узлы
        self.children = None
        # Узел является листом?
        self.is_leaf = False
        # точки узла
        self.node_points = []
        # координаты граничных точек
        self.coordinate_region = coordinate_region
        # глубина
        self.depth = depth

        left_right = self.coordinate_region[0] + (
                self.coordinate_region[2] - self.coordinate_region[0]) / 2
        top_bottom = self.coordinate_region[1] + (
                self.coordinate_region[3] - self.coordinate_region[1]) / 2

        # координаты центральной точки
        self.node_center_point = Point(left_right, top_bottom)

        # Обрезка части изображения по координатам
        image = image.crop(coordinate_region)
        # histogram возвращает список количества пикселей
        # для каждого диапазона на изображении

        # цвет и ошибка
        self.average_color, self.error = average_color.color_average(
            image.histogram())

    def split_image(self, image: Image) -> None:
        """
        Метод разбивает изображения на четыре части
        :param image: Изображение
        """

        left, top, right, bottom = self.coordinate_region

        top_left = QuadtreeNode(image, (
            left, top, self.node_center_point.x,
            self.node_center_point.y),
                                self.depth + 1)
        top_right = QuadtreeNode(image, (
            self.node_center_point.x, top, right,
            self.node_center_point.y),
                                 self.depth + 1)
        bottom_left = QuadtreeNode(image,
                                   (left,
                                    self.node_center_point.y,
                                    self.node_center_point.x,
                                    bottom),
                                   self.depth + 1)
        bottom_right = QuadtreeNode(image,
                                    (self.node_center_point.x,
                                     self.node_center_point.y,
                                     right, bottom),
                                    self.depth + 1)

        self.children = [top_left, top_right, bottom_left, bottom_right]

    def find_node(self, point, search_list: list = None) -> tuple:
        """
        Возвращает узел, содержащий точку и путь до точки
        :param point: Искомая точка
        :param search_list: Cписок узлов
        :return: Узел и список узлов
        """
        if not search_list:
            search_list = []

        search_list.append(self)

        if self.children is not None:
            if point.x_coordinate < self.node_center_point.x:
                if point.y_coordinate < self.node_center_point.y:
                    if self.children[0] is not None:
                        return self.children[0].find_node(point, search_list)
                else:
                    if self.children[2] is not None:
                        return self.children[2].find_node(point, search_list)

            else:
                if point.y_coordinate < self.node_center_point.y:
                    if self.children[1] is not None:
                        return self.children[1].find_node(point, search_list)
                else:
                    if self.children[3] is not None:
                        return self.children[3].find_node(point, search_list)

        return self, search_list

    def find_node_by_point(self, search_point: Point) -> "QuadtreeNode":
        """
        Возвращает узел, который содержит точку
        :param search_point: точка
        :return: узел
        """
        return self.find_node(search_point)[0]

    def insert_point(self, point: Point):
        """
        Вставляет точку в узел
        :param point: Точка, которая должна быть вставлена
        :return: Рекурсия
        """
        if self.children is not None:
            if point.x < self.node_center_point.x:
                if point.y < self.node_center_point.y:
                    return self.children[0].insert_point(point)
                else:
                    self.children[2].insert_point(point)

            else:
                if point.y < self.node_center_point.y:
                    return self.children[1].insert_point(point)
                else:
                    self.children[3].insert_point(point)

        self.node_points.append(point)

    def remove_point(self, delete_point: Point) -> None:
        """
        Удаляет точку
        :param delete_point: Удаляемая точка
        """
        current_node, _ = self.find_node(delete_point)

        if current_node is not None:
            for point in current_node.node_points:
                if point == delete_point:
                    current_node.node_points.remove(point)


class QuadTree:
    """Класс реализации квадродерева"""

    def __init__(self, image: Image) -> None:
        # ширина и высота
        self.width, self.height = image.size
        # корневой узел
        self.root = QuadtreeNode(image, image.getbbox(), 0)
        # максимальная глубина
        self.max_depth = 0

        self.build_tree(image, self.root)

    def build_tree(self, image: Image, node: QuadtreeNode) -> None:
        """
        Метод рекурсивно добавляет узлы
        :param image: Исходное изображение
        :param node: Узел
        """

        if (node.depth >= 8) or (node.error <= 13):
            if node.depth > self.max_depth:
                self.max_depth = node.depth
            node.is_leaf = True
            return None

        threads_for_compression = []
        node.split_image(image)

        for child in node.children:
            thread = threading.Thread(target=self.build_tree,
                                      args=(image, child))
            thread.start()
            threads_for_compression.append(thread)

        for process in threads_for_compression:
            process.join()

    def get_rec_nodes(self, node: QuadtreeNode, depth: int, leaf_nodes: list) -> None:
        """
        Рекурсивно получает листовые узлы в зависимости от того, является ли
        узел листом или достигнута ли заданная глубина
        :param node: Узел
        :param depth: Значение глубины
        :param leaf_nodes: Список листьев
        """
        if node.is_leaf or node.depth == depth:
            leaf_nodes.append(node)
        elif node.children:
            for child in node.children:
                self.get_rec_nodes(child, depth, leaf_nodes)

    def get_leaf_nodes(self, depth: int) -> list:
        """
        Метод возвращает листья квадродерева
        :param depth: Значение глубины
        :return: Список листьев
        """

        if self.max_depth < depth:
            raise ValueError('Указана глубина больше, чем высота дерева')

        leaf_nodes = []
        self.get_rec_nodes(self.root, depth, leaf_nodes)
        return leaf_nodes
