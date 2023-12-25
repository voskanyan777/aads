"""
Модуль алгоритма Ахо-Корасик
"""


class Vertex:  # pylint: disable=R0903
    """
    Узел бора
    """

    def __init__(self, parent, parent_char) -> None:
        self.next = {}  # Словарь с переходами
        self.is_terminal = False  # Заканчивается ли в этой вершине какая-то строка
        self.parent = parent  # Родитель
        self.parent_char = parent_char  # По какому символу пришли из родителя
        self.sufflink = None
        self.transitions = {}  # Переходы
        self.length = 0  # Длина подстроки


class Trie:
    """
    Класс бора
    """

    def __init__(self) -> None:
        self.vertices = {}  # Словарь с узлами {'номер узла': 'узел'}
        self.root = Vertex(None, None)  # Вершина бора

    def size(self) -> int:
        """
        Количество узлов в боре
        """

        return len(self.vertices)

    def add(self, string) -> None:
        """
        Добавление строки в бор
        Args:
            string: Строка, которую нужно добавить в бор
        returns: None
        """
        vertex = self.root
        for i in range(len(string)):  # pylint: disable=C0200:
            if vertex.next.get(ord(string[i])) is None:
                new_vertex = Vertex(vertex, string[i])
                new_vertex.length = vertex.length + 1
                self.vertices[self.size() + 1] = new_vertex
                vertex.next[ord(string[i])] = new_vertex
            vertex = vertex.next[ord(string[i])]
        vertex.is_terminal = True

    def get_link(self, vertex: Vertex) -> Vertex:
        """
        Метод вычисляет суффиксную ссылку из вершины бора
        Args:
            vertex: Вершина бора
        returns: Суффиксная ссылка
        """
        if vertex.sufflink is None:
            if self.root in (vertex, vertex.parent):
                vertex.sufflink = self.root
            else:
                vertex.sufflink = self.transition_to_symbol(self.get_link(vertex.parent),
                                                            vertex.parent_char)
        return vertex.sufflink

    def transition_to_symbol(self, vertex: Vertex, symbol: str) -> Vertex:
        """
        Метод реализует переход из вершины бора к символу
        Args:
            vertex: Вершина бора
            symbol: Символ, к которому переходим
        returns: Vertex
        """
        if vertex.transitions.get(ord(symbol)) is None:
            if vertex.next.get(ord(symbol)) is not None:
                vertex.transitions[ord(symbol)] = vertex.next[ord(symbol)]
            elif vertex == self.root:
                vertex.transitions[ord(symbol)] = self.root
            else:
                vertex.transitions[ord(symbol)] = self.transition_to_symbol(self.get_link(vertex),
                                                                            symbol)
        return vertex.transitions.get(ord(symbol))
