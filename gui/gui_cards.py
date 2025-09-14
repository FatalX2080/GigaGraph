import flet as ft
from solvers.nx_core import CuteGraph
from .graph_draftsman import Draftsman
from config import flet_colors_list, colors_list


def get_description_title(text: str) -> ft.Text:
    return ft.Text(text, style=ft.TextStyle(size=16), weight=ft.FontWeight.BOLD)


class Task:
    tasks_list = []
    page_shape = ()

    def __init__(self):
        self.main_col = ft.Column()
        self.card = ft.Card(ft.Container(content=self.main_col, margin=10, padding=10))
        self.title = ft.Text(
            "Template",
            style=ft.TextStyle(size=18),
            weight=ft.FontWeight.BOLD,
            width=float("inf"),
            text_align=ft.TextAlign.CENTER
        )
        self.main_col.controls.append(self.title)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Task.tasks_list.append(cls())

    def get_card(self) -> ft.Card:
        return self.card

    def add_obj(self, obg) -> None:
        self.main_col.controls.append(obg)

    def evaluate(self, *args, **kwargs) -> None:
        pass

    @staticmethod
    def resize_image(img_obj: ft.Image):
        img_obj.width = 0.7 * Task.page_shape[0]

    @staticmethod
    def evaluate_trigger(solver: CuteGraph) -> None:
        for task in Task.tasks_list:
            task.evaluate(solver)

    @staticmethod
    def set_page_size(page_size: tuple) -> None:
        Task.page_shape = page_size


class Task0(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Graph"

        self.img = ft.Image()
        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Row([self.img], expand=True, alignment=ft.MainAxisAlignment.CENTER))

    def evaluate(self, solver):
        v, e = solver.raw_vertices, solver.raw_edges
        gd = Draftsman(v, e)
        img = gd.display_graph("Graph")
        self.img.src_base64 = gd.to_flet_format(img)
        Task.resize_image(self.img)


class Task1(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 1"

        self.adjacency_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])
        self.incidence_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Adjacency table"))
        self.add_obj(ft.Row([self.adjacency_table], scroll=ft.ScrollMode.AUTO))
        self.add_obj(ft.Divider())
        self.add_obj(get_description_title("Incidence table"))
        self.add_obj(ft.Row([self.incidence_table], scroll=ft.ScrollMode.AUTO))

    def evaluate(self, solver: CuteGraph):
        self.adjacency_table.columns = [ft.DataColumn(ft.Text("."))]
        self.incidence_table.columns = [ft.DataColumn(ft.Text("."))]
        self.adjacency_table.rows.clear()
        self.incidence_table.rows.clear()

        self.fill_adj_table(solver)
        self.fill_inc_table(solver)

    def fill_adj_table(self, solver):
        ct = self.adjacency_table

        adj = solver.create_adjacency_matrix().data["matrix"]
        v, e = solver.raw_vertices, solver.raw_edges

        for i, vertex in enumerate(v):
            row_start = [ft.DataCell(ft.Text(str(vertex)))]
            table_row = []
            for j in range(len(v)):
                el = adj[i][j]
                cell = ft.Text(str(el))
                if el: cell.style = ft.TextStyle(color=ft.Colors.GREEN)
                table_row.append(ft.DataCell(cell))

            row = ft.DataRow(cells=row_start + table_row)
            ct.columns.append(ft.DataColumn(ft.Text(str(vertex))))
            ct.rows.append(row)

    def fill_inc_table(self, solver):
        it = self.incidence_table

        inc = solver.create_incidence_matrix().data["matrix"]
        v, e = solver.raw_vertices, solver.raw_edges

        for iex in range(1, len(e) + 1):
            it.columns.append(ft.DataColumn(ft.Text(f"u{iex}")))

        for i, t_row in enumerate(inc):
            row_start = [ft.DataCell(ft.Text(str(v[i])))]
            table_row = []
            for j in range(len(inc[0])):
                el = t_row[j]
                cell = ft.Text(str(el))
                if el == 1:
                    cell.style = ft.TextStyle(color=ft.Colors.GREEN)
                elif el == -1:
                    cell.style = ft.TextStyle(color=ft.Colors.RED)
                table_row.append(ft.DataCell(cell))

            row = ft.DataRow(cells=row_start + table_row)
            it.rows.append(row)


class Task2(Task):
    def __init__(self):
        super().__init__()


class Task3(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 3"

        self.distance_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Distance table"))
        self.add_obj(ft.Row([self.distance_table], scroll=ft.ScrollMode.AUTO))

    def evaluate(self, solver: CuteGraph):
        dt = self.distance_table

        dt.columns = [ft.DataColumn(ft.Text("."))]
        dt.rows.clear()

        answer = solver.create_distance_matrix()
        shape = answer.data["dimensions"][0]
        table = answer.data["matrix"]
        v = [str(_) for _ in solver.raw_vertices]

        for iex, vertex in enumerate(v):
            row_start = [ft.DataCell(ft.Text(vertex))]
            answer_row = []
            for j in range(shape):
                value = table[iex][j]
                st = ft.TextStyle(color=flet_colors_list[value])
                answer_row.append(
                    ft.DataCell(ft.Text(str(value), style=st)),
                )
            row = ft.DataRow(cells=row_start + answer_row)
            dt.columns.append(ft.DataColumn(ft.Text(vertex)))
            dt.rows.append(row)


class Task4(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 4"

        self.radius = ft.Text("Radius: -")
        self.diameter = ft.Text("Diameter: -")

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Radius / Diameter:"))

        self.add_obj(self.radius)
        self.add_obj(self.diameter)

    def evaluate(self, solver: CuteGraph):
        answer = solver.calculate_radius_diameter()
        r, d = answer.data["radius"], answer.data["diameter"]

        self.radius.value = f"Radius: {r}"
        self.diameter.value = f"Diameter: {d}"


class Task5(Task):
    # fixme Походу что-то не так выглядит странно
    def __init__(self):
        super().__init__()

        self.title.value = "Task 5"

        self.edge = ft.Text("Edge state: -")
        self.img = ft.Image()
        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Edge graph:"))

        self.add_obj(self.edge)
        self.add_obj(ft.Row([self.img], expand=True, alignment=ft.MainAxisAlignment.CENTER))

    def evaluate(self, solver: CuteGraph):
        answer = solver.is_line_graph()
        is_line = answer.data["is_line_graph"]
        if is_line:
            self.edge.value = f"Edge state: yes"
            v, e = answer.data["line_graph_nodes"], answer.data["line_graph_edges"]
            gd = Draftsman(v, e)
            img = gd.display_graph("Line graph")
            self.img.src_base64 = gd.to_flet_format(img)
            Task.resize_image(self.img)
        else:
            self.edge.value = f"Edge state: no"


class Task6(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 6"

        self.vc = ft.Text("Vertex connectivity: -")
        self.ec = ft.Text("Edge connectivity: -")

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Connectivity:"))

        self.add_obj(self.vc)
        self.add_obj(self.ec)

    def evaluate(self, solver: CuteGraph):
        answer = solver.calculate_connectivity()
        vc, ec = answer.data["vertex_connectivity"], answer.data["edge_connectivity"]

        self.vc.value = f"Vertex connectivity: {vc}"
        self.ec.value = f"Edge connectivity: {ec}"


class Task7(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 7"

        self.bc = ft.Text("Blocks count: -")
        self.bs = ft.Text("Blocks: -")
        self.img = ft.Image()

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Blocks:"))

        self.add_obj(self.bc)
        self.add_obj(self.bs)
        self.add_obj(ft.Row([self.img], expand=True, alignment=ft.MainAxisAlignment.CENTER))

    def evaluate(self, solver: CuteGraph):
        answer = solver.find_blocks()
        bc = answer.data["block_count"]
        blocks = answer.data["blocks"]
        v, e = solver.raw_vertices, solver.raw_edges
        v_colors = [0 for _ in range(len(v))]

        for iex, block in enumerate(blocks):
            for el in block:
                v_colors[v.index(el)] = colors_list[iex]

        gd = Draftsman(v, e)
        img = gd.display_graph("Blocks graph", v_colors)
        self.img.src_base64 = gd.to_flet_format(img)
        Task.resize_image(self.img)

        self.bc.value = f"Blocks count: {bc}"
        self.bs.value = f"Blocks: {blocks}"


class Task8(Task):
    def __init__(self):
        super().__init__()


class Task9(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 9"

        self.eg = ft.Text("Eulerian graph: -")
        self.odn = ft.Text("Odd degree nodes (?): -")
        self.eta = ft.Text("Edges to add (?): -")
        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Eulerian:"))

        self.add_obj(self.eg)
        self.add_obj(self.odn)
        self.add_obj(self.eta)

    def evaluate(self, solver: CuteGraph):
        answer = solver.check_eulerian()

        is_eulerian = answer.data["is_eulerian"]
        self.eg.value = f"Eulerian graph: {'yes' if is_eulerian else 'no'}"

        if not is_eulerian:
            odd_degree_nodes = answer.data["odd_degree_nodes"]
            odd_degree_count = answer.data["odd_degree_count"]
            edges_to_add = answer.data["edges_to_add"]
            edges_to_add_count = answer.data["edges_to_add_count"]

            self.odn.value = f"Odd degree nodes ({odd_degree_count}): {odd_degree_nodes}"
            self.eta.value = f"Edges to add ({edges_to_add_count}): {edges_to_add}"


class Task10(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 10"

        self.hg = ft.Text("Hamiltonian graph: -")
        self.nc = ft.Text("Nodes count: -")
        self.md = ft.Text("Min degree: -")
        self.dc = ft.Text("Dirac condition: -")
        self.ldn = ft.Text("Low degree nodes: -")
        self.eta = ft.Text("Edges to add: -")

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(get_description_title("Hamiltonian:"))

        self.add_obj(self.hg)
        self.add_obj(self.nc)
        self.add_obj(self.md)
        self.add_obj(self.dc)
        self.add_obj(self.ldn)
        self.add_obj(self.eta)

    def evaluate(self, solver: CuteGraph):
        answer = solver.check_hamiltonian()

        is_hamiltonian = answer.data["is_hamiltonian"]
        self.hg.value = f"Hamiltonian graph: {'yes' if is_hamiltonian else 'no'}"

        if not is_hamiltonian:
            node_count = answer.data["node_count"]
            min_degree = answer.data["min_degree"]
            dirac_condition = answer.data["dirac_condition"]
            dirac_satisfied = answer.data["dirac_satisfied"]
            low_degree_nodes = answer.data["low_degree_nodes"]
            edges_to_add = answer.data["edges_to_add"]

            self.nc.value = f"Nodes count: {node_count}"
            self.md.value = f"Min degree: {min_degree}"
            self.dc.value = f"Dirac condition: ({dirac_condition}) => {str(dirac_satisfied).upper()}"
            self.ldn.value = f"Low degree nodes: {low_degree_nodes}"
            self.eta.value = f"Edges to add: {edges_to_add}"
