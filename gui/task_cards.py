import flet as ft
import solvers


class Task:
    def __init__(self, page_size):
        self.main_col = ft.Column()
        self.card = ft.Card(ft.Container(content=self.main_col, margin=10, padding=10))
        self.title = ft.Text(style=ft.TextStyle(size=20), weight=ft.FontWeight.BOLD, width=float("inf"),
                             text_align=ft.TextAlign.CENTER)
        self.main_col.controls.append(self.title)
        self.page_size = page_size

    def get_card(self) -> ft.Card:
        return self.card

    def add_obj(self, obg) -> None:
        self.main_col.controls.append(obg)

    def evaluate(self, *args, **kwargs) -> None:
        pass


class Task0(Task):
    def __init__(self, page_size):
        super().__init__(page_size)
        self.title.value = "Graph"

        # add elements -------------------------------------------------------------------------------------
        self.img = ft.Image(
            src=".svg", width=0.4 * self.page_size[0],
            height=0.4 * self.page_size[0], fit=ft.ImageFit.CONTAIN
        )
        self.add_obj(ft.Row([self.img], alignment=ft.MainAxisAlignment.CENTER))

    def evaluate(self, journal_num: int):
        solvers.draw_by_issue(journal_num, self.img)


class Task1(Task):
    def __init__(self, page_size):
        super().__init__(page_size)
        self.title.value = "Task 1"
        bold = ft.FontWeight.BOLD

        self.adjacency_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])
        self.incidence_table = ft.DataTable(columns=[ft.DataColumn(ft.Text("."))])

        # add elements -------------------------------------------------------------------------------------
        self.add_obj(ft.Text("Adjacency table", style=ft.TextStyle(size=18), weight=bold))
        self.add_obj(ft.Row([self.adjacency_table], scroll=ft.ScrollMode.AUTO))
        self.add_obj(ft.Text("Incidence table", style=ft.TextStyle(size=18), weight=bold))
        self.add_obj(ft.Row([self.incidence_table], scroll=ft.ScrollMode.AUTO))

    def evaluate(self, journal_num: int):
        ct = self.adjacency_table
        it = self.incidence_table

        ct.columns = [ft.DataColumn(ft.Text("."))]
        it.columns = [ft.DataColumn(ft.Text("."))]
        ct.rows.clear()
        it.rows.clear()

        v, e = solvers.gen_graph(journal_num)

        for vertex in v:
            row_start = [ft.DataCell(ft.Text(str(vertex)))]
            empty_row = [ft.DataCell(ft.Text("0")) for _ in range(len(v))]
            row = ft.DataRow(cells=row_start + empty_row)

            ct.columns.append(ft.DataColumn(ft.Text(str(vertex))))
            ct.rows.append(row)
            self.draw_incidence_table_cells(e, vertex)

        for iex in range(1, len(e) + 1):
            it.columns.append(ft.DataColumn(ft.Text(f"u{iex}")))
            self.draw_adjacency_table_cells(e[iex - 1], v)

    # auxiliary --------------------------------------------------------------------------------------------

    def draw_adjacency_table_cells(self, edge, vertexes) -> None:
        start_index = vertexes.index(edge[0])
        end_index = vertexes.index(edge[1])
        text1 = self.adjacency_table.rows[start_index].cells[end_index + 1].content
        text2 = self.adjacency_table.rows[end_index].cells[start_index + 1].content

        text1.value = "1"
        text2.value = "1"

        text1.style = ft.TextStyle(color=ft.Colors.GREEN)
        text2.style = ft.TextStyle(color=ft.Colors.GREEN)

    def draw_incidence_table_cells(self, edges, vertex) -> None:
        str_vertex = str(vertex)
        row = ft.DataRow(cells=[ft.DataCell(ft.Text(str_vertex))])
        for edge in edges:
            if vertex == edge[0]:
                text = "1"
                style = ft.TextStyle(color=ft.Colors.GREEN)
            elif vertex == edge[1]:
                text = "-1"
                style = ft.TextStyle(color=ft.Colors.RED)
            else:
                text = "0"
                style = ft.TextStyle()
            row.cells.append(ft.DataCell(ft.Text(text, style=style)))
        self.incidence_table.rows.append(row)
