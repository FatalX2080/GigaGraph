import flet as ft
from gui import gui
from config import win_size

if __name__ == '__main__':
    gui = gui.Gui(win_size)
    ft.app(target=gui.mainloop)  # Flet сам передаст `page` в `mainloop`
