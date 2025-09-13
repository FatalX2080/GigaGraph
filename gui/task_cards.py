import flet as ft
from solvers.nx_core import CuteGraph


class Task:
    def __init__(self):
        self.main_col = ft.Column()
        self.card = ft.Card(ft.Container(content=self.main_col, margin=10, padding=10))
        self.title = ft.Text(style=ft.TextStyle(size=18), weight=ft.FontWeight.BOLD, width=float("inf"),
                             text_align=ft.TextAlign.CENTER)
        self.main_col.controls.append(self.title)

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

        # add elements -------------------------------------------------------------------------------------
        # self.add_obj()


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
        self.colors = [
            ft.Colors.WHITE,
            ft.Colors.BLUE,
            ft.Colors.CYAN,
            ft.Colors.GREEN,
            ft.Colors.YELLOW,
            ft.Colors.PINK,
            ft.Colors.ORANGE,
            ft.Colors.RED,
            ft.Colors.PURPLE,
            ft.Colors.BROWN,
        ]
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
                st = ft.TextStyle(color=self.colors[value])
                answer_row.append(
                    ft.DataCell(ft.Text(str(value), style=st)),
                )
            row = ft.DataRow(cells=row_start + answer_row)
            dt.columns.append(ft.DataColumn(ft.Text(vertex)))
            dt.rows.append(row)
