import flet as ft
from solvers.nx_core import CuteGraph
from solvers.graph_gen import display_graph
from base64 import b64encode
from config import flet_colors_list, colors_list


class Task:
    tasks_list = []

    def __init__(self):
        self.main_col = ft.Column()
        self.card = ft.Card(ft.Container(content=self.main_col, margin=10, padding=10))
        self.title = ft.Text(style=ft.TextStyle(size=18), weight=ft.FontWeight.BOLD, width=float("inf"),
                             text_align=ft.TextAlign.CENTER)
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


class Task0(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Graph"

        self.img = ft.Image()
        # add elements -------------------------------------------------------------------------------------
        self.add_obj(self.img)

    def evaluate(self, solver):
        v, e = solver.raw_vertices, solver.raw_edges
        img = display_graph(v, e, "Graph")
        base64_image = b64encode(img).decode('utf-8')
        self.img.src_base64 = base64_image


class Task1(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 1"
        bold = ft.FontWeight.BOLD

        self.adjacency_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])
        self.incidence_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Adjacency table", style=ft.TextStyle(size=16), weight=bold))
        self.add_obj(ft.Row([self.adjacency_table], scroll=ft.ScrollMode.AUTO))
        self.add_obj(ft.Divider())
        self.add_obj(ft.Text("Incidence table", style=ft.TextStyle(size=16), weight=bold))
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


class Task3(Task):
    def __init__(self):
        super().__init__()
        self.title.value = "Task 3"
        bold = ft.FontWeight.BOLD

        self.distance_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Distance table", style=ft.TextStyle(size=16), weight=bold))
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
        bold = ft.FontWeight.BOLD

        self.radius = ft.Text("Radius: -")
        self.diameter = ft.Text("Diameter: -")

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Radius / Diameter:", style=ft.TextStyle(size=16), weight=bold))

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
        bold = ft.FontWeight.BOLD

        self.edge = ft.Text("Edge state: -")
        self.img = ft.Image()
        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Edge graph:", style=ft.TextStyle(size=16), weight=bold))

        self.add_obj(self.edge)
        self.add_obj(self.img)

    def evaluate(self, solver: CuteGraph):
        answer = solver.is_line_graph()
        is_line = answer.data["is_line_graph"]
        if is_line:
            self.edge.value = f"Edge state: yes"
            v, e = answer.data["line_graph_nodes"], answer.data["line_graph_edges"]
            img = display_graph(v, e, "line graph")
            base64_image = b64encode(img).decode('utf-8')
            self.img.src_base64 = base64_image
        else:
            self.edge.value = f"Edge state: no"


class Task6(Task):
    def __init__(self):
        super().__init__()

        self.title.value = "Task 6"
        bold = ft.FontWeight.BOLD

        self.vc = ft.Text("Vertex connectivity: -")
        self.ec = ft.Text("Edge connectivity: -")

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("connectivity:", style=ft.TextStyle(size=16), weight=bold))

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
        bold = ft.FontWeight.BOLD

        self.bc = ft.Text("Blocks count: -")
        self.img = ft.Image()

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Blocks:", style=ft.TextStyle(size=16), weight=bold))

        self.add_obj(self.bc)
        self.add_obj(self.img)

    def evaluate(self, solver: CuteGraph):
        answer = solver.find_blocks()
        bc = answer.data["block_count"]
        v, e = solver.raw_vertices, solver.raw_edges
        v_colors = [0 for _ in range(len(v))]
        for iex, block in enumerate(answer.data["blocks"]):
            for el in block:
                v_colors[v.index(el)] = colors_list[iex]

        img = display_graph(v, e, "line graph", v_colors)
        base64_image = b64encode(img).decode('utf-8')
        self.img.src_base64 = base64_image

        self.bc.value = f"Blocks count: {bc}"
