import flet as ft
from gui import gui


# if __name__ == "__main__":
#     win = gui.Gui()
#     win.mainloop()

if __name__ == '__main__':
    gui = gui.Gui()
    ft.app(target=gui.mainloop)  # Flet сам передаст `page` в `mainloop`