# Para la construccion de la interfaz
import tkinter as tk
from tkinter import PanedWindow, PhotoImage, filedialog, ttk

# Para el formato del editor de codigo
import pygments.lexers
from chlorophyll import CodeView

# Para obtener las imagenes
import os
thisdir = os.path.dirname(__file__)
IMG_BASE_DE_DATOS = None
IMG_BASE_DE_DATO = None
IMG_CARPETA = None

# Para atajos del teclado
import keyboard

# Variables generales
TEMA_EDITOR="monokai"
NOMBRE_TAB = 'query'
TABS_ACTUALES = []
ANCHO_VENTANA = 1000
ALTURA_VENTANA = 700

def obtener_contenido_tab(indice_actual):
    # Obtener el widget CodeView del tab seleccionado
    tab_seleccionado = notebook_central.winfo_children()[indice_actual]
    codeview = tab_seleccionado.winfo_children()[0]  # CodeView es el primer widget dentro del tab

    # Obtener el widget Text dentro de CodeView
    text_widget = codeview.winfo_children()[0]  # Text es el primer widget dentro de CodeView

    # Obtener el texto del widget Text
    texto = text_widget.get(1.0, tk.END)

    return texto

def setear_contenido_nuevo_tab(indice_actual, contenido):
    # Obtener el widget CodeView del tab seleccionado
    tab_seleccionado = notebook_central.winfo_children()[indice_actual]
    codeview = tab_seleccionado.winfo_children()[0]  # CodeView es el primer widget dentro del tab

    # Obtener el widget Text dentro de CodeView
    text_widget = codeview.winfo_children()[0]  # Text es el primer widget dentro de CodeView

    # Borrar contenido existente
    text_widget.delete(1.0, tk.END)

    # Insertar nuevo contenido
    text_widget.insert(1.0, contenido)

def ejecutar_query():

    if len(TABS_ACTUALES) <= 0:
        return

    indice_actual = notebook_central.index(notebook_central.select())
    texto = obtener_contenido_tab(indice_actual)

    # Se analiza el query
    print(texto)

    # Se setea la salida
    setear_salida("Texto del tab " + str((indice_actual + 1)) + " analizado correctamente")

def setear_salida(texto):
    # Habilitar el widget Text temporalmente
    text_widget.config(state="normal")
    # Borrar el contenido anterior
    text_widget.delete(1.0, tk.END)
    # Insertar texto al final
    text_widget.insert(tk.END, texto)
    # Deshabilitar el widget Text nuevamente
    text_widget.config(state="disabled")

def mostrar_componentes_del_lenguaje():

    global IMG_BASE_DE_DATOS, IMG_BASE_DE_DATO, IMG_CARPETA

    # Se eliminan los items actuales
    for item in treeview.get_children():
        treeview.delete(item)

    # Se crean nuevamente los items
    IMG_BASE_DE_DATOS = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_bds.png'))
    treeview.insert('', '0', 'item1', text='  Bases de datos', tags=('estilo_negrita'), image=IMG_BASE_DE_DATOS)

    IMG_BASE_DE_DATO = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_bd.png'))
    treeview.insert('item1', 'end', 'Base 1', text='Base 1', image=IMG_BASE_DE_DATO)
    treeview.insert('item1', 'end', 'Base 2', text='Base 2', image=IMG_BASE_DE_DATO)

    IMG_CARPETA = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_folder.png'))
    treeview.insert('Base 1', 'end', '  Tablas', text='Tablas', image=IMG_CARPETA)

# OPCIONES PARA EL MENU DE ARCHIVOS

def crear_tab_nuevo(nombre_archivo=None, path_archivo=None):

    crear_archivo = True
    if nombre_archivo:

        for tab in TABS_ACTUALES:
            if tab["path"] is not None and tab["path"] == path_archivo:
                crear_archivo = False
                break

        if crear_archivo:
            TABS_ACTUALES.append({
                "nativo": False,
                "indice": -1,
                "nombre": nombre_archivo,
                "path": path_archivo
            })
    else:
        indice = 0
        for tab in reversed(TABS_ACTUALES):
            if tab["nativo"]:
                indice = tab["indice"] + 1
                nombre_archivo = NOMBRE_TAB + str(indice) + '.sql'
                break

        if indice <= 0:
            nombre_archivo = NOMBRE_TAB + str(1) + '.sql'
            indice = 1

        TABS_ACTUALES.append({
            "nativo": True,
            "indice": indice,
            "nombre": nombre_archivo,
            "path": None
        })
        nombre_archivo = '*' + nombre_archivo

    if crear_archivo:
        # Agrega un nuevo tab con el nombre del archivo
        nuevo_tab = ttk.Frame(notebook_central)
        notebook_central.add(nuevo_tab, text=nombre_archivo)

        # Panel del codigo dentro del nuevo tab
        codeview = CodeView(nuevo_tab, lexer=pygments.lexers.SqlLexer, color_scheme=TEMA_EDITOR)
        codeview.pack(fill="both", expand=True)

        # Selecciona el tab recien creado
        notebook_central.select(nuevo_tab)

    return crear_archivo

def abrir():

    file_path = filedialog.askopenfilename(filetypes=[("SQL (*.sql)", "*.sql"), ("Todos los archivos", "*.*")])
    if file_path:
        ruta_archivo = file_path
        nombre_archivo = os.path.basename(ruta_archivo)
        with open(ruta_archivo, 'r') as archivo:
            se_creo_archivo = crear_tab_nuevo(nombre_archivo, ruta_archivo)
            if se_creo_archivo:
                contenido = archivo.read()
                indice_actual = notebook_central.index(notebook_central.select())
                setear_contenido_nuevo_tab(indice_actual, contenido)

def guardar():

    if len(TABS_ACTUALES) <= 0:
        return

    # Nombre del archivo
    nombre_archivo = ""

    # Se obtiene el indice actual
    indice_actual = notebook_central.index(notebook_central.select())
    if TABS_ACTUALES[indice_actual]["path"] is None:
        file_path = filedialog.asksaveasfilename(defaultextension=".sql", initialfile=TABS_ACTUALES[indice_actual]["nombre"], filetypes=[("SQL (*.sql)", "*.sql"), ("Todos los archivos", "*.*")])
        if file_path:
            nombre_archivo = os.path.basename(file_path)
            with open(file_path, 'w') as archivo:
                archivo.write(obtener_contenido_tab(indice_actual))
                TABS_ACTUALES[indice_actual]["path"] = file_path
    else:
        nombre_archivo = TABS_ACTUALES[indice_actual]["nombre"]
        with open(TABS_ACTUALES[indice_actual]["path"], 'w') as archivo:
                archivo.write(obtener_contenido_tab(indice_actual))

    if len(nombre_archivo) > 0:
        notebook_central.tab(indice_actual, text=nombre_archivo)

# def guardar_como():

#     if len(TABS_ACTUALES) <= 0:
#         return

#     # Se obtiene el nombre actual del tab
#     indice_actual = notebook_central.index(notebook_central.select())
#     nombre_tab_actual = notebook_central.tab(indice_actual, "text")

#     file_path = filedialog.asksaveasfilename(defaultextension=".sql", initialfile=nombre_tab_actual, filetypes=[("SQL (*.sql)", "*.sql"), ("Todos los archivos", "*.*")])
#     if file_path:
#         with open(file_path, 'w') as archivo:
#             archivo.write(obtener_contenido_tab(indice_actual))

def cerrar_tab_actual():

    if len(TABS_ACTUALES) <= 0:
        return

    indice_actual = notebook_central.index(notebook_central.select())
    TABS_ACTUALES.pop(indice_actual)
    notebook_central.forget(indice_actual)

    # Obtener el widget Frame del tab seleccionado
    tab_frame = notebook_central.winfo_children()[indice_actual]

    # Destruir el frame para liberar recursos
    tab_frame.destroy()

def salir():
    root.destroy()

keyboard.add_hotkey('F6', ejecutar_query)
keyboard.add_hotkey('ctrl+n', crear_tab_nuevo)
keyboard.add_hotkey('ctrl+o', abrir)
keyboard.add_hotkey('ctrl+s', guardar)
# Creacion de ventana principal
root = tk.Tk()
root.title("MiSQL")
root.geometry(str(ANCHO_VENTANA) + "x" + str(ALTURA_VENTANA))
root.option_add("*tearOff", 0)

#  Obtenemos el largo y  ancho de la pantalla
wtotal = root.winfo_screenwidth()
htotal = root.winfo_screenheight()

#  Aplicamos la siguiente formula para calcular donde debería posicionarse
pwidth = round(wtotal/2-ANCHO_VENTANA/2)
pheight = round(htotal/2-ALTURA_VENTANA/2)

#  Se lo aplicamos a la geometría de la ventana
root.geometry(str(ANCHO_VENTANA)+"x"+str(ALTURA_VENTANA)+"+"+str(pwidth)+"+"+str(pheight))

# Menu en barra
menubar = tk.Menu(root)

# Menu de archivos
file_menu = tk.Menu(menubar)
file_menu.add_command(label="Nuevo (Ctrl+N)", command=crear_tab_nuevo)
file_menu.add_command(label="Abrir (Ctrl+O)", command=abrir)
file_menu.add_command(label="Guardar", command=guardar)
# file_menu.add_command(label="Guardar como", command=guardar_como)
file_menu.add_command(label="Cerrar", command=cerrar_tab_actual)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=salir)

# Menu de herramientas
tool_menu = tk.Menu(menubar)

# Submenu 'Bases de datos'
submenu_bd = tk.Menu(tool_menu)
submenu_bd.add_command(label="Crear nuevo")
submenu_bd.add_command(label="Eliminar")
submenu_bd.add_command(label="Crear DUMP")
submenu_bd.add_command(label="Seleccionar uno")
submenu_bd.add_separator()
submenu_bd.add_command(label="Actualizar", command=mostrar_componentes_del_lenguaje)
tool_menu.add_cascade(label="Base de datos", menu=submenu_bd)

submenu_sql = tk.Menu(tool_menu)
submenu_sql.add_command(label="Nuevo query", command=crear_tab_nuevo)
submenu_sql.add_command(label="Ejecutar query (F6)", command=ejecutar_query)
tool_menu.add_cascade(label="SQL", menu=submenu_sql)

tool_menu.add_command(label="Exportar")
tool_menu.add_command(label="Importar")

menubar.add_cascade(menu=file_menu, label="Archivo")
menubar.add_cascade(menu=tool_menu, label="Herramientas")

root.config(menu=menubar)

# Panel principal
panel_1 = PanedWindow(bd=4, relief="raised", bg="red")
panel_1.pack(fill="both", expand=1)

# -------------------------------------------
# Panel izquierdo dentro del panel principal
treeview = ttk.Treeview()
treeview.tag_configure('estilo_negrita', font=('TkDefaultFont', 10, 'bold'))
treeview.pack()
panel_1.add(treeview)
# Se agrega un sub panel dentro del panel principal
panel_2 = PanedWindow(panel_1, orient="vertical", bd=4, relief="raised", bg="blue")
panel_1.add(panel_2)
# -------------------------------------------

# -------------------------------------------
# Panel central dentro del sub panel
notebook_central = ttk.Notebook(panel_2, height=550)
notebook_central.pack(fill="both", expand=True)
panel_2.add(notebook_central)
# -------------------------------------------

# -------------------------------------------
# Panel inferior dentro del sub panel
notebook_inferior = ttk.Notebook(panel_2)
tab_salida = ttk.Frame(notebook_inferior)
notebook_inferior.add(tab_salida, text="Salida de datos")
notebook_inferior.pack(fill="both", expand=True)
panel_2.add(notebook_inferior)

# Agregar un widget Text al tab para mostrar texto
text_widget = tk.Text(tab_salida, wrap="word", height=10, width=50, state="disabled")
text_widget.pack(fill="both", expand=True)
# -------------------------------------------

root.update()
root.mainloop()