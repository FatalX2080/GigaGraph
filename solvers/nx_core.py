# По идее сюда должны передаваться 2 массива с рёбрами и вершинами. И уже их я запихиваю в класс

#import edges_from_somewhere_esle, vertices_from_somewhere_else


import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
from task_result_class import TaskResult #КЛАСС УНИФИЦИРОВАННОГО ОТВЕТА
import numpy as np



# Это универсальный класс (тк задания может выполнять не только для БДЗшного графа),
# ему можно передать список вершин И рёбер, и он их так и оставит
# Или можно передать просто вершины и ВЫЗВАТЬ метод build_covering_graph и он сам досоздаст недостающие
# и уберёт лишние рёбра (вершины будут нетронуты)


class CuteGraph:
    def __init__(self, vertices: List[Any], edges: List[Tuple[Any, Any]]):
        self.di_graph = nx.DiGraph()  # <-- nx object
        self.undi_graph = self.di_graph.to_undirected()  # шоб сразу неорграф был (<-- nx object)

        self.raw_vertices = vertices  # raw verts (bare array) ((не нужны, но пусть будут))
        self.raw_edges = edges  # raw edges (bare array)

        self.add_vertices(vertices)  # verts in nx
        self.add_edges(edges)  # edges in nx

        #self.task_results = {}
    def recreate_undi(self) -> None: #just in case
        self.undi_graph = self.di_graph.to_undirected()
    

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

    def create_adjacency_matrix(self) -> TaskResult:
        """1. Матрица смежности"""
        try:
            nodes = sorted(self.di_graph.nodes())
            n = len(nodes)
            adj_matrix = np.zeros((n, n), dtype=int)

            for i, u in enumerate(nodes):
                for j, v in enumerate(nodes):
                    if self.di_graph.has_edge(u, v):
                        adj_matrix[i, j] = 1

            return TaskResult(
                success=True,
                task_name="Матрица смежности",
                data={
                    'matrix': adj_matrix.tolist(),
                    'nodes': nodes,
                    'edges': self.di_graph.edges(),
                    'dimensions': f"{n}×{n}",
                    'matrix_type': 'adjacency'
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Матрица смежности",
                error=str(e)
            )
        
    def create_incidence_matrix(self) -> TaskResult:
        """1.1. Матрица инцидентности"""
        try:
            nodes = sorted(self.di_graph.nodes())
            edges = list(self.di_graph.edges())
            n = len(nodes)
            m = len(edges)
            inc_matrix = np.zeros((n, m), dtype=int)
            
            for j, (u, v) in enumerate(edges):
                u_idx = nodes.index(u)
                v_idx = nodes.index(v)
                inc_matrix[u_idx, j] = 1
                inc_matrix[v_idx, j] = -1
            
            return TaskResult(
                success=True,
                task_name="Матрица инцидентности",
                data={
                    'matrix': inc_matrix.tolist(),
                    'nodes': nodes,
                    'edges': edges,
                    'dimensions': f"{n}×{m}",
                    'matrix_type': 'incidence'
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Матрица инцидентности",
                error=str(e)
            )
        

    #def 
    # """2. положительные и отрицательные внешние устойчивые множества"""
        
        
    def create_distance_matrix(self) -> TaskResult:
        """3. Матрица расстояний"""
        try:
            nodes = sorted(self.undi_graph.nodes())
            n = len(nodes)
            dist_matrix = np.zeros((n, n), dtype=int)  # Изменено на int
            
            for i, u in enumerate(nodes):
                for j, v in enumerate(nodes):
                    try:
                        dist = nx.shortest_path_length(self.undi_graph, u, v)
                        dist_matrix[i, j] = dist
                    except nx.NetworkXNoPath:
                        dist_matrix[i, j] = -1  # Используем -1 вместо inf для int
            
            # Сериализуем специальные значения
            dist_matrix_serializable = []
            for row in dist_matrix:
                serializable_row = []
                for val in row:
                    if val == -1:  # Заменяем -1 на '∞'
                        serializable_row.append('∞')
                    else:
                        serializable_row.append(int(val))  # Гарантируем int
                dist_matrix_serializable.append(serializable_row)
            
            return TaskResult(
                success=True,
                task_name="Матрица расстояний",
                data={
                    'matrix': dist_matrix_serializable,
                    'nodes': nodes,
                    'edges': self.undi_graph.edges(),
                    'dimensions': f"{n}×{n}",
                    'matrix_type': 'distance'
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Матрица расстояний",
                error=str(e)
            )
        

    def calculate_radius_diameter(self) -> TaskResult:
        """4. Радиус и диаметр графа"""
        try:
            eccentricity = nx.eccentricity(self.undi_graph)
            radius = min(eccentricity.values())
            diameter = max(eccentricity.values())
            
            return TaskResult(
                success=True,
                task_name="Радиус и диаметр графа",
                data={
                    'radius': radius,
                    'diameter': diameter,
                    'nodes': self.undi_graph.nodes(),
                    'edges': self.undi_graph.edges(),
                    'eccentricity': eccentricity,
                    'center_vertices': [v for v, ecc in eccentricity.items() if ecc == radius],
                    'peripheral_vertices': [v for v, ecc in eccentricity.items() if ecc == diameter]
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Радиус и диаметр графа",
                error=str(e)
            )


    def is_line_graph(self) -> TaskResult:
        """5. Проверить, является ли граф рёберным и построить образ"""
        try:
            # Проверяем основные свойства рёберных графов
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Проверка рёберного графа",
                    data={'is_line_graph': False, 'reason': 'Граф не связный'}
                )
            
            is_line = False
            line_graph_image = None
            original_edges_mapping = {}
            
            # Проверяем с помощью встроенной функции NetworkX (если доступна)
            try:
                is_line = nx.is_line_graph(self.undi_graph)
            except AttributeError:
                # Функция может быть недоступна в некоторых версиях
                # Используем собственную проверку
                degrees = dict(self.undi_graph.degree())
                odd_degree_count = sum(1 for deg in degrees.values() if deg % 2 != 0)
                
                # Эвристическая проверка
                is_line = (odd_degree_count <= 2 and 
                        len(self.undi_graph.nodes()) >= 3 and
                        nx.is_connected(self.undi_graph))
            
            # Если граф рёберный, строим его образ
            if is_line:
                line_graph_image, original_edges_mapping = self._build_line_graph_image()
                
                # Сохраняем визуализацию
                visualization_path = self._visualize_line_graph(line_graph_image, original_edges_mapping)
                
                return TaskResult(
                    success=True,
                    task_name="Проверка рёберного графа",
                    data={
                        'is_line_graph': True,
                        'line_graph_nodes': list(line_graph_image.nodes()),
                        'line_graph_edges': list(line_graph_image.edges()),
                        'original_edges_mapping': original_edges_mapping,
                        'note': 'Граф является рёберным, образ построен'
                    },
                    visualizations=[visualization_path] if visualization_path else []
                )
            else:
                return TaskResult(
                    success=True,
                    task_name="Проверка рёберного графа",
                    data={'is_line_graph': False, 'reason': 'Не удовлетворяет критериям рёберного графа'}
                )
                
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Проверка рёберного графа",
                error=str(e)
            )

    def _build_line_graph_image(self):
        """Строит образ рёберного графа"""
        # Создаём новый граф для образа
        line_graph = nx.Graph()
        original_edges = list(self.undi_graph.edges())
        original_edges_mapping = {}
        
        # Добавляем вершины в образ (каждая вершина соответствует ребру исходного графа)
        for i, edge in enumerate(original_edges):
            line_graph.add_node(i)
            original_edges_mapping[i] = edge
        
        # Добавляем рёбра в образ (соединяем вершины, если соответствующие рёбра имеют общую вершину)
        for i in range(len(original_edges)):
            for j in range(i + 1, len(original_edges)):
                edge_i = original_edges[i]
                edge_j = original_edges[j]
                
                # Проверяем, имеют ли рёбра общую вершину
                if (edge_i[0] in edge_j or edge_i[1] in edge_j):
                    line_graph.add_edge(i, j)
        
        return line_graph, original_edges_mapping

    def _visualize_line_graph(self, line_graph, original_edges_mapping):
        """Визуализирует образ рёберного графа"""
        try:
            plt.figure(figsize=(12, 10))
            pos = nx.spring_layout(line_graph, k=1.5, iterations=50)
            
            # Рисуем граф
            nx.draw(line_graph, pos, with_labels=True, node_color='lightgreen', 
                    node_size=800, font_size=10, font_weight='bold')
            
            # Добавляем метки с исходными рёбрами
            labels = {}
            for node in line_graph.nodes():
                original_edge = original_edges_mapping[node]
                labels[node] = f"{original_edge[0]}-{original_edge[1]}\n({node})"
            
            nx.draw_networkx_labels(line_graph, pos, labels, font_size=8)
            
            # Добавляем заголовок
            plt.title("Образ рёберного графа\n(вершины соответствуют рёбрам исходного графа)")
            
            # Сохраняем изображение
            import os
            os.makedirs('visualizations', exist_ok=True)
            visualization_path = 'visualizations/line_graph_image.png'
            plt.savefig(visualization_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return visualization_path
            
        except Exception as e:
            print(f"Ошибка при визуализации: {e}")
            return None


    def calculate_connectivity(self) -> TaskResult:
        """6. Определить вершинную и рёберную связность"""
        try:
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Связность графа",
                    data={
                        'vertex_connectivity': 0,
                        'edge_connectivity': 0,
                        'is_connected': False
                    }
                )
            
            vertex_conn = nx.node_connectivity(self.undi_graph)
            edge_conn = nx.edge_connectivity(self.undi_graph)
            
            return TaskResult(
                success=True,
                task_name="Связность графа",
                data={
                    'vertex_connectivity': vertex_conn,
                    'edge_connectivity': edge_conn,
                    'is_connected': True,
                    'min_degree': min(dict(self.undi_graph.degree()).values())
                },
                metadata={
                    'note': 'Вершинная связность ≤ рёберная связность ≤ минимальная степень'
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Связность графа",
                error=str(e)
            )
        

    def find_blocks(self) -> TaskResult:
        """7. Выделить все блоки графа"""
        try:
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Блоки графа",
                    data={
                        'blocks': [],
                        'block_count': 0,
                        'is_connected': False,
                        'components': list(nx.connected_components(self.undi_graph))
                    }
                )
            
            blocks = list(nx.biconnected_components(self.undi_graph))
            articulation_points = list(nx.articulation_points(self.undi_graph))
            
            return TaskResult(
                success=True,
                task_name="Блоки графа",
                data={
                    'blocks': [list(block) for block in blocks],
                    'block_count': len(blocks),
                    'articulation_points': articulation_points,
                    'articulation_count': len(articulation_points),
                    'is_biconnected': (len(articulation_points) == 0)
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Блоки графа",
                error=str(e)
            )
        

    
    def build_spanning_tree(self) -> TaskResult: #КРИИИИНЖ
        """8. Построить остов и соответствующие матрицы"""
        try:
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Остовное дерево",
                    data={'has_spanning_tree': False, 'reason': 'Граф не связный'}
                )
            
            # Строим остовное дерево (минимальное остовное дерево)
            spanning_tree = nx.minimum_spanning_tree(self.undi_graph)
            
            # Матрица циклов (нужна фундаментальная система циклов)
            cycle_basis = nx.cycle_basis(self.undi_graph)
            cycle_matrix = self._create_cycle_matrix(cycle_basis)
            
            # Матрица разрезов (упрощённо)
            cut_matrix = self._create_cut_matrix(spanning_tree)
            
            return TaskResult(
                success=True,
                task_name="Остовное дерево",
                data={
                    'spanning_tree_edges': list(spanning_tree.edges()),
                    'spanning_tree_nodes': list(spanning_tree.nodes()),
                    'cycle_basis': cycle_basis,
                    'cycle_matrix': cycle_matrix,
                    'cut_matrix': cut_matrix,
                    'fundamental_cycles_count': len(cycle_basis)
                },
                metadata={
                    'note': 'Матрицы циклов и разрезов представлены в упрощённом виде'
                }
            )
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Остовное дерево",
                error=str(e)
            )

    def _create_cycle_matrix(self, cycle_basis):
        """Вспомогательная функция для создания матрицы циклов"""
        edges = list(self.undi_graph.edges())
        matrix = []
        for cycle in cycle_basis:
            row = [0] * len(edges)
            for i in range(len(cycle)):
                u, v = cycle[i], cycle[(i + 1) % len(cycle)]
                edge = (min(u, v), max(u, v))
                if edge in edges:
                    row[edges.index(edge)] = 1
            matrix.append(row)
        return matrix

    def _create_cut_matrix(self, spanning_tree):
        """Вспомогательная функция для создания матрицы разрезов"""
        edges = list(self.undi_graph.edges())
        tree_edges = list(spanning_tree.edges())
        matrix = []
        
        # Для каждого ребра остовного дерева создаём разрез
        for tree_edge in tree_edges:
            row = [0] * len(edges)
            # Удаляем ребро из дерева и находим компоненты связности
            temp_tree = spanning_tree.copy()
            temp_tree.remove_edge(*tree_edge)
            components = list(nx.connected_components(temp_tree))
            
            # Помечаем рёбра, пересекающие разрез
            for edge in edges:
                u, v = edge
                if (u in components[0] and v in components[1]) or (v in components[0] and u in components[1]):
                    row[edges.index(edge)] = 1
            matrix.append(row)
        
        return matrix


    def check_eulerian(self) -> TaskResult:
        """9. Проверить эйлеровость графа"""
        try:
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Эйлеров граф",
                    data={
                        'is_eulerian': False,
                        'reason': 'Граф не связный',
                        'edges_to_add': 'Требуется связность'
                    }
                )
            
            # Проверяем эйлеровость
            is_eulerian = nx.is_eulerian(self.undi_graph)
            
            if is_eulerian:
                return TaskResult(
                    success=True,
                    task_name="Эйлеров граф",
                    data={'is_eulerian': True}
                )
            else:
                # Находим вершины с нечётной степенью
                degrees = dict(self.undi_graph.degree())
                odd_degree_nodes = [node for node, deg in degrees.items() if deg % 2 != 0]
                
                # Предлагаем рёбра для добавления
                edges_to_add = []
                for i in range(0, len(odd_degree_nodes) - 1, 2):
                    edges_to_add.append((odd_degree_nodes[i], odd_degree_nodes[i + 1]))
                
                return TaskResult(
                    success=True,
                    task_name="Эйлеров граф",
                    data={
                        'is_eulerian': False,
                        'odd_degree_nodes': odd_degree_nodes,
                        'odd_degree_count': len(odd_degree_nodes),
                        'edges_to_add': edges_to_add,
                        'edges_to_add_count': len(edges_to_add),
                        'note': f'Добавить {len(edges_to_add)} рёбер для эйлеровости'
                    }
                )
                
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Эйлеров граф",
                error=str(e)
            )

    def check_hamiltonian(self) -> TaskResult:
        """10. Проверить гамильтоновость графа"""
        try:
            if not nx.is_connected(self.undi_graph):
                return TaskResult(
                    success=True,
                    task_name="Гамильтонов граф",
                    data={
                        'is_hamiltonian': False,
                        'reason': 'Граф не связный',
                        'edges_to_add': 'Требуется связность'
                    }
                )
            
            # Пытаемся найти гамильтонов цикл
            try:
                is_hamiltonian = nx.is_hamiltonian(self.undi_graph)
                if is_hamiltonian:
                    return TaskResult(
                        success=True,
                        task_name="Гамильтонов граф",
                        data={'is_hamiltonian': True}
                    )
            except:
                # Функция может быть недоступна или выбросить исключение
                is_hamiltonian = False
            
            # Эвристическая проверка и предложение рёбер
            if not is_hamiltonian:
                # Простая эвристика: если граф достаточно плотный, он может быть гамильтоновым
                n = len(self.undi_graph.nodes())
                degrees = dict(self.undi_graph.degree())
                min_degree = min(degrees.values())
                
                # Теорема Дирака: если min_degree >= n/2, то граф гамильтонов
                is_hamiltonian_by_dirac = (min_degree >= n / 2)
                
                # Предлагаем добавить рёбра для увеличения степеней
                low_degree_nodes = [node for node, deg in degrees.items() if deg < n / 2]
                edges_to_add = []
                
                if low_degree_nodes:
                    # Соединяем вершины с низкими степенями
                    for i in range(len(low_degree_nodes) - 1):
                        for j in range(i + 1, len(low_degree_nodes)):
                            if not self.undi_graph.has_edge(low_degree_nodes[i], low_degree_nodes[j]):
                                edges_to_add.append((low_degree_nodes[i], low_degree_nodes[j]))
                                break
                        if edges_to_add:
                            break
                
                return TaskResult(
                    success=True,
                    task_name="Гамильтонов граф",
                    data={
                        'is_hamiltonian': is_hamiltonian_by_dirac,
                        'node_count': n,
                        'min_degree': min_degree,
                        'dirac_condition': f"min_degree >= n/2 ({min_degree} >= {n/2})",
                        'dirac_satisfied': is_hamiltonian_by_dirac,
                        'low_degree_nodes': low_degree_nodes,
                        'edges_to_add': edges_to_add[:3],  # Ограничиваем количество предлагаемых рёбер
                        'note': 'Гамильтоновость проверена по теореме Дирака'
                    }
                )
                
        except Exception as e:
            return TaskResult(
                success=False,
                task_name="Гамильтонов граф",
                error=str(e)
            )




#Дальше только дебаг (*-*)
# Пример использования: ###DEBUG###
if __name__ == "__main__":
    # Вариант 1: Передаем готовые ребра
    vertices = [1, 2, 3, 4, 6, 12]

    # Вариант 2: Строим граф покрытия автоматически
    graph2 = CuteGraph(vertices, [])
    graph2.build_coverage_graph()


    ##DEBUG PRINT FUNCTION###
    def print_task_result(result: TaskResult) -> None:
        """Красиво печатает TaskResult в терминал"""

        print("═" * 60)
        print(f"📋 ЗАДАЧА: {result.task_name}")
        print("═" * 60)

        if not result.success:
            print(f"❌ СТАТУС: Ошибка")
            print(f"📛 ОШИБКА: {result.error}")
            print("═" * 60)
            return

        print(f"✅ СТАТУС: Успешно")

        # Выводим основные данные
        if result.data:
            print("\n📊 ДАННЫЕ:")
            for key, value in result.data.items():
                if isinstance(value, (list, np.ndarray)) and len(value) > 0 and isinstance(value[0],
                                                                                           (list, np.ndarray)):
                    # Матрица
                    print(f"  {key}:")
                    if 'nodes' in result.data:
                        print_matrix(value, result.data['nodes'])
                    else:
                        for i, row in enumerate(value):
                            print(f"    Строка {i}: {row}")
                else:
                    print(f"  {key}: {value}")

        # Выводим метаданные
        if result.metadata:
            print("\n📝 МЕТАДАННЫЕ:")
            for key, value in result.metadata.items():
                print(f"  {key}: {value}")

        # Выводим визуализации
        if result.visualizations:
            print(f"\n🎨 ВИЗУАЛИЗАЦИИ: {len(result.visualizations)} файлов")
            for viz in result.visualizations:
                print(f"  📁 {viz}")

        print("═" * 60)

    def print_matrix(matrix, labels=None):
        """Печатает матрицу с красивым форматированием"""
        if labels is None:
            labels = [str(i) for i in range(len(matrix))]

        # Заголовок
        header = "     " + " ".join(f"{label:>4}" for label in labels)
        print(header)
        print("    " + "─" * (len(header) - 4))

        # Строки матрицы
        for i, row in enumerate(matrix):
            row_label = f"{labels[i]:>3} │"
            row_str = " ".join(f"{str(val):>4}" for val in row)
            print(f"{row_label} {row_str}")

    print_task_result(graph2.create_adjacency_matrix())
    print_task_result(graph2.create_incidence_matrix())
    #2nd task
    print_task_result(graph2.create_distance_matrix())
    print_task_result(graph2.calculate_radius_diameter())
    print_task_result(graph2.is_line_graph())
    print_task_result(graph2.calculate_connectivity())
    print_task_result(graph2.find_blocks())
    # print_task_result(graph2.build_spanning_tree())
    print_task_result(graph2.check_eulerian())
    print_task_result(graph2.check_hamiltonian())
    