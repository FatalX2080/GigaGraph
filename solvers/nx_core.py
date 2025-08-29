# По идее сюда должны передаваться 2 массива с рёбрами и вершинами. И уже их я запихиваю в класс

#import edges_from_somewhere_esle, vertices_from_somewhere_else


import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any


# Это универсальный класс (тк задания может выполнять не только для БДЗшного графа),
# ему можно передать список вершин И рёбер, и он их так и оставит
# Или можно передать просто вершины и ВЫЗВАТЬ метод build_covering_graph и он сам досоздаст недостающие
# и уберёт лишние рёбра (вершины будут нетронуты)

class CuteGraph:
    def __init__(self, vertices: List[Any], edges: List[Tuple[Any, Any]]):
        self.di_graph = nx.DiGraph()  # <-- nx object
        self.undi_graph = self.di_graph.to_undirected()  # шоб сразу неорграф был (<-- nx object)

        self.raw_vertices = vertices  # raw verts (bare array)
        self.raw_edges = edges  # raw edges (bare array)

        self.add_vertices(vertices)  # verts in nx
        self.add_edges(edges)  # edges in nx

    def add_vertices(self, vertices: List[Any]) -> None:
        # add vertices
        self.di_graph.add_nodes_from(vertices)

    def add_edges(self, edges: List[Tuple[Any, Any]]) -> None:
        # add edges directed
        self.di_graph.add_edges_from(edges)

    # Функция для проверки отношения покрытия
    def is_covering(self, a: Any, b: Any, vertices: List[Any]) -> bool:
        """
        Проверяет, покрывает ли a элемент b в решетке делителей
        """
        if b % a != 0:  # b должно делиться на a
            return False

        # Проверяем, существует ли c такое, что a < c < b
        for c in vertices:
            if c != a and c != b and a < c < b and b % c == 0 and c % a == 0:
                return False
        return True

    # Метод для построения графа покрытия на основе вершин
    def build_coverage_graph(self):
        """
        Строит граф отношений покрытия на основе self.raw_vertices
        """
        vertices = sorted(self.raw_vertices)
        self.di_graph.clear()   # Очищаем предыдущий граф
        self.raw_edges.clear()  # Очищаем предыдущие рёбра
        self.add_vertices(vertices)

        for i in range(len(vertices)):
            for j in range(len(vertices)):
                if i != j and self.is_covering(vertices[i], vertices[j], vertices):
                    self.di_graph.add_edge(vertices[i], vertices[j])
                    self.raw_edges.append((vertices[i], vertices[j]))
                    self.undi_graph = self.di_graph.to_undirected()

    #----------- BHW TASKS (AS CLASS METHODS)












# Пример использования: ###DEBUG###
if __name__ == "__main__":
    # Вариант 1: Передаем готовые ребра
    vertices = [1, 2, 3, 4, 6, 12]
    edges = [(1, 2), (1, 3), (2, 4), (2, 6), (3, 6), (4, 12), (6, 12)]

    graph1 = CuteGraph(vertices, edges)
    print("Граф с готовыми ребрами:", list(graph1.di_graph.edges()))

    # Вариант 2: Строим граф покрытия автоматически
    graph2 = CuteGraph(vertices, [])
    graph2.build_coverage_graph()
    print("Граф покрытия:", list(graph2.di_graph.edges()))
    print("LALALLA:", list(graph2.raw_edges))

    print("HELLLO", graph2.di_graph.edges())
    print("HELLLO again", graph2.undi_graph.nodes())


