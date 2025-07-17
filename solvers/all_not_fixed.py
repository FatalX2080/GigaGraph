import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from math import gcd
from functools import reduce

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(numbers):
    return reduce(lcm, numbers)

# Определяем вершины
M1 = {10, 12, 15, 18, 20}
M2 = {1, 2, 3, 5, 6}
vertices = sorted(list(M1.union(M2)))
vertices.append(lcm_list(vertices))

# Функция для проверки отношения покрытия
def is_covering(a, b, vertices):
    if b % a != 0:  # b должно делиться на a
        return False
    
    # Проверяем, существует ли c такое, что a < c < b
    for c in vertices:
        if c != a and c != b and b % c == 0 and c % a == 0:
            return False
    return True

# Создаем ориентированный граф для диаграммы Хассе
G = nx.DiGraph()
G.add_nodes_from(vertices)

# Добавляем ребра на основе отношения покрытия
for i in range(len(vertices)):
    for j in range(len(vertices)):
        if i != j and is_covering(vertices[i], vertices[j], vertices):
            G.add_edge(vertices[i], vertices[j])

# Функция для создания матрицы смежности
def create_adjacency_matrix(graph):
    nodes = sorted(graph.nodes())
    n = len(nodes)
    adj_matrix = np.zeros((n, n), dtype=int)
    
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if graph.has_edge(u, v):
                adj_matrix[i, j] = 1
                
    return adj_matrix, nodes

# Функция для создания матрицы инцидентности
def create_incidence_matrix(graph):
    nodes = sorted(graph.nodes())
    edges = list(graph.edges())
    n = len(nodes)
    m = len(edges)
    inc_matrix = np.zeros((n, m), dtype=int)
    
    for j, (u, v) in enumerate(edges):
        u_idx = nodes.index(u)
        v_idx = nodes.index(v)
        inc_matrix[u_idx, j] = 1  # Начало ребра
        inc_matrix[v_idx, j] = -1  # Конец ребра
        
    return inc_matrix, nodes, edges

# Функция для создания матрицы расстояний
def create_distance_matrix(graph):
    nodes = sorted(graph.nodes())
    n = len(nodes)
    dist_matrix = np.zeros((n, n), dtype=float)
    
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            try:
                dist = nx.shortest_path_length(graph, u, v)
                dist_matrix[i, j] = dist
            except nx.NetworkXNoPath:
                dist_matrix[i, j] = float('inf')
                
    return dist_matrix, nodes

# Функция для вывода матрицы расстояний с метками
def print_distance_matrix(dist_matrix, nodes):
    n = len(nodes)
    # Выводим заголовок
    print("\nМатрица расстояний:")
    print("    ", end="")
    for node in nodes:
        print(f"{node:4}", end=" ")
    print("\n" + "-" * (5 * (n + 1)))
    
    # Выводим строки с метками
    for i, node in enumerate(nodes):
        print(f"{node:2} |", end=" ")
        for j in range(n):
            if dist_matrix[i,j] == float('inf'):
                print("  ∞ ", end=" ")
            else:
                print(f"{int(dist_matrix[i,j]):3} ", end=" ")
        print()

# Создаем неориентированную версию графа
G_undirected = G.to_undirected()

# Функция для вычисления радиуса и диаметра графа
def calculate_radius_diameter(graph):
    try:
        # Вычисляем эксцентриситет для каждой вершины
        eccentricity = nx.eccentricity(graph)
        radius = min(eccentricity.values())
        diameter = max(eccentricity.values())
        
        # Выводим эксцентриситет для каждой вершины
        print("\nЭксцентриситет вершин:")
        for node, ecc in eccentricity.items():
            print(f"Вершина {node}: {ecc}")
            
        return radius, diameter
    except nx.NetworkXError:
        return float('inf'), float('inf')

def draw_hasse_diagram(graph):
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph, k=2, iterations=50)
    
    # Рисуем вершины
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', 
            node_size=1000, font_size=12, font_weight='bold',
            arrows=True, arrowstyle='->', arrowsize=20)
    
    # Создаем словарь для хранения номеров рёбер
    edge_labels = {}
    for i, edge in enumerate(graph.edges()):
        edge_labels[edge] = f"e{i+1}"
    
    # Рисуем метки рёбер
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels,
                                font_color='red', font_size=10)
    
    plt.title("Диаграмма Хассе")
    plt.savefig('hasse_diagram.png')
    plt.close()

# Функция для проверки, является ли граф рёберным
def is_line_graph(graph):
    # Проверяем основные свойства рёберных графов
    
    # 1. Проверяем, что граф связный
    if not nx.is_connected(graph):
        return False
    
    # 2. Проверяем степени вершин
    degrees = dict(graph.degree())
    for degree in degrees.values():
        if degree < 1:  # В рёберном графе не может быть изолированных вершин
            return False
    
    # 3. Проверяем окрестности вершин
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        degree = len(neighbors)
        
        if degree == 2:
            # Для вершин степени 2 окрестность должна быть полным подграфом
            if not graph.has_edge(neighbors[0], neighbors[1]):
                return False
        elif degree > 2:
            # Для вершин степени > 2 окрестность должна быть разбита на полные подграфы
            # Каждая вершина должна принадлежать ровно двум таким подграфам
            
            # Находим все клики в окрестности
            subgraph = graph.subgraph(neighbors)
            cliques = list(nx.find_cliques(subgraph))
            
            # Проверяем, что каждая вершина входит ровно в две клики
            vertex_clique_count = {v: 0 for v in neighbors}
            for clique in cliques:
                for v in clique:
                    vertex_clique_count[v] += 1
            
            # Проверяем, что каждая вершина входит ровно в две клики
            for count in vertex_clique_count.values():
                if count != 2:
                    return False
            
            # Проверяем, что клики пересекаются не более чем по одной вершине
            for i in range(len(cliques)):
                for j in range(i+1, len(cliques)):
                    intersection = set(cliques[i]) & set(cliques[j])
                    if len(intersection) > 1:
                        return False
    
    # 4. Проверяем отсутствие запрещённых подграфов Краутерса
    # (упрощённая проверка)
    forbidden_subgraphs = [
        # K_{1,3} - "звезда" с тремя лучами
        nx.Graph([(0,1), (0,2), (0,3)]),
        # Граф с вершиной степени 3, соединённой с тремя вершинами степени 1
        nx.Graph([(0,1), (0,2), (0,3), (1,2)]),
        # Граф с вершиной степени 4, соединённой с четырьмя вершинами степени 1
        nx.Graph([(0,1), (0,2), (0,3), (0,4), (1,2), (3,4)])
    ]
    
    for forbidden in forbidden_subgraphs:
        if nx.is_isomorphic(graph, forbidden):
            return False
    
    return True

# Функция для вычисления вершинной и рёберной связности
def calculate_connectivity(graph):
    try:
        vertex_conn = nx.node_connectivity(graph)
        edge_conn = nx.edge_connectivity(graph)
        return vertex_conn, edge_conn
    except nx.NetworkXError:
        return 0, 0

# Функция для поиска всех блоков графа
def find_blocks(graph):
    return list(nx.biconnected_components(graph))

# Функция для проверки эйлеровости и нахождения необходимых рёбер

def check_eulerian(graph):
    """
    Проверяет, является ли граф эйлеровым, и возвращает рекомендации по его преобразованию.
    
    Аргументы:
        graph (nx.Graph или nx.DiGraph): Граф для анализа.
    
    Возвращает:
        tuple (bool, list, str): 
            - Флаг эйлеровости (True/False).
            - Список рёбер для добавления/удаления (если граф не эйлеров).
            - Пояснение (для неэйлеровых графов).
    """
    is_directed = isinstance(graph, nx.DiGraph)
    result = {
        "is_eulerian": False,
        "edges_to_add": [],
        "edges_to_remove": [],
        "message": ""
    }
    
    # Проверка связности
    if is_directed:
        is_weakly_connected = nx.is_weakly_connected(graph)
    else:
        is_weakly_connected = nx.is_connected(graph)
    
    if not is_weakly_connected:
        result["message"] = "Граф не связный. Эйлеров цикл невозможен."
        return (False, [], result["message"])
    
    # Проверка степеней вершин
    if is_directed:
        in_degree = dict(graph.in_degree())
        out_degree = dict(graph.out_degree())
        unbalanced = []
        
        for node in graph.nodes():
            if in_degree[node] != out_degree[node]:
                unbalanced.append(node)
        
        if not unbalanced:
            result["is_eulerian"] = True
            result["message"] = "Ориентированный граф эйлеров (все вершины сбалансированы)."
            return (True, [], result["message"])
        else:
            # Попытка сбалансировать вершины
            deficit_nodes = []
            surplus_nodes = []
            
            for node in unbalanced:
                diff = out_degree[node] - in_degree[node]
                if diff > 0:
                    surplus_nodes.append((node, diff))
                elif diff < 0:
                    deficit_nodes.append((node, -diff))
            
            # Предлагаем добавить рёбра для балансировки
            edges_to_add = []
            
            for (u, u_diff), (v, v_diff) in zip(surplus_nodes, deficit_nodes):
                edges_to_add.append((u, v))
            
            result["edges_to_add"] = edges_to_add
            result["message"] = (
                f"Ориентированный граф не эйлеров. Несбалансированные вершины: {unbalanced}. "
                f"Добавьте рёбра: {edges_to_add}."
            )
            return (False, edges_to_add, result["message"])
    
    else:  # Неориентированный граф
        degree = dict(graph.degree())
        odd_degree_nodes = [node for node, deg in degree.items() if deg % 2 != 0]
        
        if not odd_degree_nodes:
            result["is_eulerian"] = True
            result["message"] = "Неориентированный граф эйлеров (все степени чётные)."
            return (True, [], result["message"])
        else:
            # Предлагаем добавить рёбра, чтобы сделать степени чётными
            edges_to_add = []
            
            # Соединяем вершины с нечётными степенями попарно
            for i in range(0, len(odd_degree_nodes), 2):
                if i + 1 < len(odd_degree_nodes):
                    u = odd_degree_nodes[i]
                    v = odd_degree_nodes[i + 1]
                    edges_to_add.append((u, v))
            
            result["edges_to_add"] = edges_to_add
            result["message"] = (
                f"Неориентированный граф не эйлеров. Вершины с нечётной степенью: {odd_degree_nodes}. "
                f"Добавьте рёбра: {edges_to_add}."
            )
            return (False, edges_to_add, result["message"])

# Функция для проверки гамильтоновости и нахождения необходимых рёбер
from itertools import combinations

def check_hamiltonian(graph, max_edges_to_add=7):
    """
    Проверяет гамильтоновость графа перебором рёбер.
    
    Аргументы:
        graph (nx.Graph): Исходный граф.
        max_edges_to_add (int): Максимальное количество рёбер для добавления (по умолчанию 5).
    
    Возвращает:
        tuple (bool, list, str): 
            - Флаг гамильтоновости (True/False).
            - Список рёбер для добавления (если нужно).
            - Пояснение.
    """
    if not isinstance(graph, nx.Graph):
        raise ValueError("Функция работает только с неориентированными графами (nx.Graph).")
    
    # Проверка связности
    if not nx.is_connected(graph):
        return (False, [], "Граф не связный. Гамильтонов цикл невозможен.")
    
    # Если граф уже гамильтонов
    try:
        if nx.is_hamiltonian(graph):
            return (True, [], "Граф уже гамильтонов.")
    except:
        pass
    
    # Все возможные рёбра, которых нет в графе
    all_possible_edges = [
        (u, v) for u in graph.nodes() 
        for v in graph.nodes() 
        if u < v and not graph.has_edge(u, v)
    ]
    
    # Перебор комбинаций рёбер (от 1 до max_edges_to_add)
    for k in range(1, max_edges_to_add + 1):
        for edges_to_add in combinations(all_possible_edges, k):
            G_temp = graph.copy()
            G_temp.add_edges_from(edges_to_add)
            
            try:
                if nx.is_hamiltonian(G_temp):
                    return (
                        False, 
                        list(edges_to_add), 
                        f"Граф станет гамильтоновым, если добавить {k} рёбер: {list(edges_to_add)}."
                    )
            except:
                continue
    
    return (
        False, 
        [], 
        f"Не удалось сделать граф гамильтоновым, добавив до {max_edges_to_add} рёбер."
    )

# Функция для вывода матрицы смежности с метками
def print_adjacency_matrix(adj_matrix, nodes):
    n = len(nodes)
    # Выводим заголовок
    print("\nМатрица смежности:")
    print("    ", end="")
    for node in nodes:
        print(f"{node:4}", end=" ")
    print("\n" + "-" * (5 * (n + 1)))
    
    # Выводим строки с метками
    for i, node in enumerate(nodes):
        print(f"{node:2} |", end=" ")
        for j in range(n):
            print(f"{int(adj_matrix[i,j]):3} ", end=" ")
        print()

# Функция для вывода матрицы инцидентности с метками
def print_incidence_matrix(inc_matrix, nodes, edges):
    n = len(nodes)
    m = len(edges)
    # Выводим заголовок
    print("\nМатрица инцидентности:")
    print("    ", end="")
    for i in range(m):
        print(f"   ", end=" ")
    print("\n" + "-" * (5 * (m + 1)))
    
    # Выводим строки с метками
    for i, node in enumerate(nodes):
        print(f"{node:2} |", end=" ")
        for j in range(m):
            print(f"{int(inc_matrix[i,j]):3} ", end=" ")
        print()

# Функция для проверки, является ли граф рёберным, и построения его образа
def is_line_graph_and_build_image(graph):
    # Проверяем, является ли граф рёберным
    is_line = is_line_graph(graph)
    
    if is_line:
        # Строим образ графа
        # Для каждой вершины в исходном графе создаем ребро в образе
        image = nx.Graph()
        edges = list(graph.edges())
        
        # Добавляем вершины в образ (каждая вершина соответствует ребру исходного графа)
        for i, edge in enumerate(edges):
            image.add_node(i, original_edge=edge)
        
        # Добавляем рёбра в образ (соединяем вершины, если соответствующие рёбра имеют общую вершину)
        for i in range(len(edges)):
            for j in range(i+1, len(edges)):
                # Проверяем, имеют ли рёбра общую вершину
                if (edges[i][0] in edges[j] or edges[i][1] in edges[j]):
                    image.add_edge(i, j)
        
        # Рисуем образ графа
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(image)
        nx.draw(image, pos, with_labels=True, node_color='lightgreen', 
                node_size=1000, font_size=12, font_weight='bold')
        
        # Добавляем метки с исходными рёбрами
        labels = {i: f"{edges[i][0]}-{edges[i][1]}" for i in range(len(edges))}
        nx.draw_networkx_labels(image, pos, labels)
        
        plt.title("Образ рёберного графа")
        plt.savefig('line_graph_image.png')
        plt.close()
        
        return True, image
    return False, None

def visualize_cliques(graph):
    # Находим все клики в графе
    cliques = list(nx.find_cliques(graph))
    
    # Создаем новую фигуру
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(graph, k=2, iterations=50)
    
    # Рисуем исходный граф
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', 
            node_size=1000, font_size=12, font_weight='bold')
    
    # Рисуем каждую клику своим цветом
    colors = plt.cm.rainbow(np.linspace(0, 1, len(cliques)))
    for i, (clique, color) in enumerate(zip(cliques, colors)):
        # Создаем подграф для клики
        subgraph = graph.subgraph(clique)
        # Рисуем рёбра клики
        nx.draw_networkx_edges(subgraph, pos, edge_color=color, 
                             width=3, alpha=0.7)
        # Добавляем метку с номером клики
        plt.text(0.02, 0.98 - i*0.03, f"Клика {i+1}: {sorted(clique)}", 
                transform=plt.gca().transAxes, color=color)
    
    plt.title("Полные подграфы (клики) в графе")
    plt.savefig('cliques.png')
    plt.close()
    
    # Выводим информацию о кликах
    print("\nНайденные полные подграфы (клики):")
    for i, clique in enumerate(cliques, 1):
        print(f"Клика {i}: {sorted(clique)}")

def analyze_vertex_clique_membership(graph):
    # Находим все клики в графе
    cliques = list(nx.find_cliques(graph))
    
    # Создаем словарь для подсчета количества клик, в которые входит каждая вершина
    vertex_clique_count = {}
    for node in graph.nodes():
        vertex_clique_count[node] = 0
    
    # Подсчитываем количество клик для каждой вершины
    for clique in cliques:
        for node in clique:
            vertex_clique_count[node] += 1
    
    # Находим вершины, которые входят в более чем два полных подграфа
    problematic_vertices = {node: count for node, count in vertex_clique_count.items() if count > 2}
    
    if problematic_vertices:
        print("\nВершины, входящие в более чем два полных подграфа:")
        for node, count in problematic_vertices.items():
            print(f"Вершина {node} входит в {count} полных подграфа")
            
            # Находим все клики, содержащие эту вершину
            containing_cliques = [clique for clique in cliques if node in clique]
            print(f"Полные подграфы, содержащие вершину {node}:")
            for i, clique in enumerate(containing_cliques, 1):
                print(f"  Подграф {i}: {sorted(clique)}")
    else:
        print("\nНет вершин, входящих в более чем два полных подграфа")
    
    return problematic_vertices

def main():
    # 1. Создаем матрицы
    adj_matrix, nodes = create_adjacency_matrix(G)
    inc_matrix, nodes, edges = create_incidence_matrix(G)
    
    # Создаем и выводим матрицу расстояний
    dist_matrix, nodes = create_distance_matrix(G)
    print_distance_matrix(dist_matrix, nodes)
    
    # 2. Рисуем диаграмму Хассе
    draw_hasse_diagram(G)
    print("\nДиаграмма Хассе сохранена как 'hasse_diagram.png'")
    
    # 3. Визуализируем полные подграфы
    visualize_cliques(G_undirected)
    print("\nВизуализация полных подграфов сохранена как 'cliques.png'")
    
    # 4. Анализируем принадлежность вершин полным подграфам
    problematic_vertices = analyze_vertex_clique_membership(G_undirected)
    
    # 5. Вычисляем радиус и диаметр неориентированного графа
    radius, diameter = calculate_radius_diameter(G_undirected)
    print(f"\nРадиус графа: {radius}")
    print(f"Диаметр графа: {diameter}")
    
    # 6. Проверяем, является ли граф рёберным и строим его образ
    is_line, line_image = is_line_graph_and_build_image(G_undirected)
    print(f"\nГраф является рёберным: {'Да' if is_line else 'Нет'}")
    if is_line:
        print("Образ рёберного графа сохранен как 'line_graph_image.png'")
    
    # 7. Вычисляем вершинную и рёберную связность
    vertex_conn, edge_conn = calculate_connectivity(G_undirected)
    print(f"\nВершинная связность: {vertex_conn}")
    print(f"Рёберная связность: {edge_conn}")
    
    # 8. Находим все блоки графа
    blocks = find_blocks(G_undirected)
    print(f"\nКоличество блоков: {len(blocks)}")
    print("Блоки графа:")
    for i, block in enumerate(blocks, 1):
        print(f"Блок {i}: {sorted(block)}")
    
    # 9. Проверяем эйлеровость
    print(check_eulerian(G_undirected))
    
    # 10. Проверяем гамильтоновость
    print(check_hamiltonian(G_undirected))

if __name__ == "__main__":
    main()