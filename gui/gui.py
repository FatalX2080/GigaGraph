import flet as ft
from gui.gui_cards import Task
from solvers.nx_core import CuteGraph
from solvers.graph_gen import gen_graph

from config import max_journal_num, rejection_message


def close_dlg(e):
    dlg_modal.open = False
    e.control.page.update()


dlg_modal = ft.AlertDialog(
    modal=True, title=ft.Text("Allert"),
    content=ft.Text(rejection_message),
    actions=[ft.TextButton("Yes", on_click=close_dlg), ],
    actions_alignment=ft.MainAxisAlignment.END, on_dismiss=close_dlg
)


class Gui:
    def __init__(self, size: tuple = (1280, 720)):
        self.page = None
        self.page_size = size
        self.language_core = None
        self.issue_in_magazine = None
        self.task_manager = None

        self.main_column = ft.Column(scroll=ft.ScrollMode.AUTO)
        self.page_objects = ft.Container(content=self.main_column, expand=True)

        self.init_page()

    def init_page(self):
        column_control = self.main_column.controls
        column_control.append(self.gen_settings_card())
        column_control.append(ft.Divider())

        self.task_manager = Task
        self.task_manager.set_page_size(self.page_size)

        for card in self.task_manager.tasks_list:
            self.main_column.controls.append(card.get_card())

    def check_data(self, data: dict) -> bool:
        try:
            if not (0 <= int(data["num"]) <= max_journal_num):
                self.issue_in_magazine.value = ""
                self.issue_in_magazine.update()
                return False
        except ValueError:
            self.issue_in_magazine.value = ""
            self.issue_in_magazine.update()
            return False

        if data["core"] != "Python":
            self.page.overlay.append(dlg_modal)
            dlg_modal.open = True
            self.language_core.value = "Python"
            self.page.update()
            return False

        return True

    def evaluate(self, event):
        data = {"num": self.issue_in_magazine.value, "core": self.language_core.value}

        accept = self.check_data(data)
        if accept:
            data["num"] = int(data["num"])
            v, e = gen_graph(data["num"])
            solver = CuteGraph(v, e)
            solver.build_coverage_graph()

            self.task_manager.evaluate_trigger(solver)
            event.page.update()

    def gen_settings_card(self):
        main_row = ft.Row()
        title = ft.Text("Settings: ", weight=ft.FontWeight.BOLD, style=ft.TextStyle(size=18))
        self.language_core = ft.Dropdown(label="Solver core", width=200, options=[
            ft.DropdownOption("C"),
            ft.DropdownOption("Python"),
        ], value="Python")
        self.issue_in_magazine = ft.TextField(label="Issue in the magazine")
        evaluate_button = ft.Button("Evaluate", on_click=self.evaluate)

        main_row.controls.append(title)
        main_row.controls.append(self.language_core)
        main_row.controls.append(self.issue_in_magazine)

        return ft.Card(ft.Container(
            content=ft.Row(
                [main_row, evaluate_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ), margin=10, padding=10
        ))

    def mainloop(self, page: ft.Page):
        self.page = page
        page.window.width = self.page_size[0]
        page.window.height = self.page_size[1]
        page.add(self.page_objects)


if __name__ == '__main__':
    gui = Gui()
    ft.app(gui.mainloop)
