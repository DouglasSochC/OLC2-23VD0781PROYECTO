import tkinter as tk
from tkinter import Label, PanedWindow, ttk

import pygments.lexers
from chlorophyll import CodeView

NAME_TAB = 'query'
CURRENT_TABS = []

def crear_tab_nuevo():
    
    indice_nuevo_tab = (CURRENT_TABS[-1] + 1) if len(CURRENT_TABS) > 0 else 1
    nuevo_tab = ttk.Frame(notebook)
    CURRENT_TABS.append(indice_nuevo_tab)
    notebook.add(nuevo_tab, text=NAME_TAB + str(indice_nuevo_tab) + '.sql')

    # Panel del codigo dentro del panel central
    codeview = CodeView(nuevo_tab, lexer=pygments.lexers.SqlLexer, color_scheme="monokai")
    codeview.pack(fill="both", expand=True)

    # Seleciona notebok
    notebook.select(nuevo_tab)

def cerrar_tab_actual():
    current_tab = notebook.index(notebook.select())
    CURRENT_TABS.pop(current_tab)
    notebook.forget(current_tab)

root = tk.Tk()
root.title("MiSQL")
root.geometry("1000x800")
root.option_add("*tearOff", 0)

menubar = tk.Menu(root)

file_menu = tk.Menu(menubar)
file_menu.add_command(label="Nuevo", command=crear_tab_nuevo)
file_menu.add_command(label="Abrir")
file_menu.add_command(label="Guardar")
file_menu.add_command(label="Guardar como")
file_menu.add_command(label="Cerrar", command=cerrar_tab_actual)
file_menu.add_separator()
file_menu.add_command(label="Salir")

tool_menu = tk.Menu(menubar)
tool_menu.add_command(label="Crear BD")
tool_menu.add_command(label="Eliminar BD")
tool_menu.add_command(label="Crear DUMP")
tool_menu.add_command(label="Seleccionar BD")

menubar.add_cascade(menu=file_menu, label="Archivo")
menubar.add_cascade(menu=tool_menu, label="Herramientas")

root.config(menu=menubar)

# Panel principal
panel_1 = PanedWindow(bd=4, relief="raised", bg="red")
panel_1.pack(fill="both", expand=1)

# Panel izquierdo dentro del panel principal
left_label = Label(panel_1, text="Left Panel")
panel_1.add(left_label)

# Se agrega un sub panel dentro del panel principal
panel_2 = PanedWindow(panel_1, orient="vertical", bd=4, relief="raised", bg="blue")
panel_1.add(panel_2)

# Panel superior dentro del sub panel
top = Label(panel_2, text="Top Panel", height=2)
panel_2.add(top)

# Panel central dentro del sub panel
notebook = ttk.Notebook(panel_2, height=600)
notebook.pack(fill="both", expand=True)
panel_2.add(notebook)

# Panel inferior dentro del sub panel
bottom = Label(panel_2, text="Bottom panel")
panel_2.add(bottom)

root.update()
root.mainloop()