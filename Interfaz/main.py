# Para realizar el analisis
from Parser.parser import parser

# Para la construccion de la interfaz
import tkinter as tk
from tkinter import PanedWindow, PhotoImage, filedialog, simpledialog, messagebox, ttk

# Para el formato del editor de codigo
import pygments.lexers
from chlorophyll import CodeView

# Para obtener las imagenes
import os
thisdir = os.path.dirname(__file__)
IMG_BASE_DE_DATOS = None
IMG_BASE_DE_DATO = None
IMG_PROCEDIMIENTO = None
IMG_FUNCION = None
IMG_CARPETA = None
IMG_TABLA = None

# Para atajos del teclado
import keyboard

# Para variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Funciones DDL
import re
from Funcionalidad.ddl import crear_base_de_datos, eliminar_base_de_datos

# Variables generales
TEMA_EDITOR="monokai"
NOMBRE_TAB = 'query'
TABS_ACTUALES = []
ANCHO_VENTANA = 1000
ALTURA_VENTANA = 700
CARPETA_PARA_BASES_DE_DATOS = str(os.environ.get("CARPETA_PARA_BASES_DE_DATOS"))
CARPETA_PARA_TABLAS = str(os.environ.get("CARPETA_PARA_TABLAS"))
CARPETA_PARA_FUNCIONES = str(os.environ.get("CARPETA_PARA_FUNCIONES"))
CARPETA_PARA_PROCEDIMIENTOS = str(os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))
BD_SELECCIONADA=""

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

    # Parse an expression
    salida = parser.parse(texto)

    # Se setea la salida
    if salida is not None:        
        if isinstance(salida, list):
            mostrar_salida_como_tabla(salida)
        else:
            mostrar_salida_como_texto(salida)

def mostrar_componentes_del_lenguaje():

    global IMG_BASE_DE_DATOS, IMG_BASE_DE_DATO, IMG_CARPETA, IMG_TABLA, IMG_PROCEDIMIENTO, IMG_FUNCION, BD_SELECCIONADA

    if os.path.exists(CARPETA_PARA_BASES_DE_DATOS): # Se valida que exista la base de datos

        # Se eliminan los items actuales del treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Se definen las rutas de los iconos
        IMG_BASE_DE_DATOS = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_bds.png'))
        IMG_BASE_DE_DATO = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_bd.png'))
        IMG_CARPETA = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_folder.png'))
        IMG_TABLA = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_table.png'))
        IMG_PROCEDIMIENTO = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_procedure.png'))
        IMG_FUNCION = PhotoImage(file=os.path.join(thisdir, 'images', 'icon_function.png'))

        # Se crea el item principal que contiene todas las bases de datos
        treeview.insert('', '0', 'principal', text='  Bases de datos', image=IMG_BASE_DE_DATOS, open=True, tags=('estilo_titulos' if len(BD_SELECCIONADA) > 0 else ''))

        # Obtiene las bases de datos
        bases_de_datos = os.listdir(CARPETA_PARA_BASES_DE_DATOS)

        # Dibuja cada base de datos
        for nombre_bd in bases_de_datos:
            treeview.insert('principal', 'end', nombre_bd, text=nombre_bd, image=IMG_BASE_DE_DATO, open= (True if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else False), tags=('estilo_titulos' if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else ''))

            # Obtiene las carpetas de esa base de datos
            carpetas = os.listdir(CARPETA_PARA_BASES_DE_DATOS + nombre_bd)

            # Dibuja cada carpeta de esa base de datos
            for nombre_carpeta in carpetas:

                treeview.insert(nombre_bd, 'end', nombre_bd + nombre_carpeta, text=nombre_carpeta, image=IMG_CARPETA, tags=('estilo_carpetas' if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else ''))

                # Obtiene cada archivo de esa carpeta
                contenido_carpeta = os.listdir(CARPETA_PARA_BASES_DE_DATOS + nombre_bd + "/" + nombre_carpeta)

                if ("/" + nombre_carpeta + "/") == CARPETA_PARA_TABLAS:
                    for nombre_archivo in contenido_carpeta:
                        treeview.insert(nombre_bd + nombre_carpeta, 'end', nombre_bd + nombre_carpeta + nombre_archivo, text=nombre_archivo.rsplit('.', 1)[0], image=IMG_TABLA, tags=('estilo_carpetas' if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else ''))
                elif ("/" + nombre_carpeta + "/") == CARPETA_PARA_FUNCIONES:
                    for nombre_archivo in contenido_carpeta:
                        treeview.insert(nombre_bd + nombre_carpeta, 'end', nombre_bd + nombre_carpeta + nombre_archivo, text=nombre_archivo.rsplit('.', 1)[0], image=IMG_FUNCION, tags=('estilo_carpetas' if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else ''))
                elif ("/" + nombre_carpeta + "/") == CARPETA_PARA_PROCEDIMIENTOS:
                    for nombre_archivo in contenido_carpeta:
                        treeview.insert(nombre_bd + nombre_carpeta, 'end', nombre_bd + nombre_carpeta + nombre_archivo, text=nombre_archivo.rsplit('.', 1)[0], image=IMG_PROCEDIMIENTO, tags=('estilo_carpetas' if len(BD_SELECCIONADA) > 0 and nombre_bd == BD_SELECCIONADA else ''))

def oyente_cambio_texto_tab(codeview, indice_actual, event):
    # Obtener el código de la tecla presionada
    keycode = event.keycode

    # Evitar teclas especiales como FIN, INICIO, REPAG, AVEPAG, etc.
    if event.keysym in ['End', 'Home', 'Next', 'Prior']:
        return

    # Evitar las teclas de flechas, Mayúsculas, Shift y Alt
    if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R']:
        return

    # Evita reconocer la combinacion ctrl+s
    if (event.keysym.lower() == 's' or event.keysym.lower() == 'n' or event.keysym.lower() == 'o') and event.state & 0x4:
        return

    # Evita reconocer una tecla de funcion (F1, F2, ..., F12)
    if 112 <= keycode <= 123:
        return  # No hacer nada si es una tecla de funcion

    # Se obtiene el nombre del archivo
    nombre_archivo = notebook_central.tab(indice_actual, "text")

    # Se setea el nombre y se elimina un listener
    notebook_central.tab(indice_actual, text="*" + nombre_archivo)
    codeview.unbind("<KeyRelease>")

def comando_eliminar_bd(variable, ventana_eliminar):
    seleccion = variable.get()
    respuesta = eliminar_base_de_datos(seleccion)
    messagebox.showinfo("Informacion", respuesta)
    mostrar_componentes_del_lenguaje()
    ventana_eliminar.destroy()

def comando_seleccionar_bd(variable, ventana_seleccionar):

    global BD_SELECCIONADA

    seleccion = variable.get()
    BD_SELECCIONADA = seleccion
    messagebox.showinfo("Informacion", "Base de datos seleccionada correctamente")
    mostrar_componentes_del_lenguaje()
    ventana_seleccionar.destroy()

def mostrar_salida_como_texto(texto):
    # Destruir todos los elementos del tab_salida
    for widget in tab_salida.winfo_children():
        widget.destroy()

    # Crea un widget Text y lo agrega al panel para mostrar texto
    text_widget = tk.Text(tab_salida, wrap="word", height=10, width=50, state="disabled")
    text_widget.pack(fill="both", expand=True)

    # Habilitar el widget Text temporalmente
    text_widget.config(state="normal")
    # Insertar texto al final
    text_widget.insert(tk.END, texto)
    # Deshabilitar el widget Text nuevamente
    text_widget.config(state="disabled")

def mostrar_salida_como_tabla(data: dict):

    if len(data) <= 0:
        mostrar_salida_como_texto("No hay registros por mostrar")
        return

    # Destruir todos los elementos del tab_salida
    for widget in tab_salida.winfo_children():
        widget.destroy()

    encabezados = list(data[0].keys())
    columnas = encabezados.copy()
    columnas.pop()

    # Crear el Treeview (tabla) y lo agrega al tab_salida
    tree = ttk.Treeview(tab_salida, columns=(columnas))

    # Configurar las columnas
    for indice, encabezado in enumerate(encabezados):
        tree.heading("#" + str(indice), text=encabezado)

    # Agregar datos
    for d in data:
        # Obtener la primera posición
        primera_posicion = next(iter(d.values()))
        # Obtener el resto de los valores
        resto_valores = list(d.values())[1:]
        # Se agrega la linea a la tabla
        tree.insert("", "end", text=primera_posicion, values=resto_valores)

    # Configurar Scrollbar vertical
    yscrollbar = ttk.Scrollbar(tab_salida, orient="vertical", command=tree.yview)
    tree.configure(yscroll=yscrollbar.set)
    yscrollbar.pack(side="right", fill="y")

    # Configurar Scrollbar horizontal
    xscrollbar = ttk.Scrollbar(tab_salida, orient="horizontal", command=tree.xview)
    tree.configure(xscroll=xscrollbar.set)
    xscrollbar.pack(side="bottom", fill="x")

    # Empaquetar la tabla
    tree.pack(expand=True, fill="both")

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

                # Se agrega un escucha para verificar si ha modificado o no el archivo
                tab_actual = notebook_central.winfo_children()[indice_actual].winfo_children()[0]
                codeview = tab_actual.winfo_children()[0]
                codeview.bind("<KeyRelease>", lambda e: oyente_cambio_texto_tab(codeview, indice_actual, e))

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

        # Se agrega un escucha para verificar si a modificado o no el archivo
        tab_actual = notebook_central.winfo_children()[indice_actual].winfo_children()[0]
        codeview = tab_actual.winfo_children()[0]
        codeview.bind("<KeyRelease>", lambda e: oyente_cambio_texto_tab(codeview, indice_actual, e))

def guardar_como():

    if len(TABS_ACTUALES) <= 0:
        return

    # Se obtiene el indice actual del tab
    indice_actual = notebook_central.index(notebook_central.select())

    file_path = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL (*.sql)", "*.sql"), ("Todos los archivos", "*.*")])
    if file_path:
        nombre_archivo = os.path.basename(file_path)
        with open(file_path, 'w') as archivo:
            archivo.write(obtener_contenido_tab(indice_actual))

            # Se actualiza la metada del archivo
            TABS_ACTUALES[indice_actual]["nativo"] = False
            TABS_ACTUALES[indice_actual]["indice"] = -1
            TABS_ACTUALES[indice_actual]["nombre"] = nombre_archivo
            TABS_ACTUALES[indice_actual]["path"] = file_path

            # Se actualiza el nombre del tab
            notebook_central.tab(indice_actual, text=nombre_archivo)

            # Se agrega un escucha para verificar si a modificado o no el archivo
            tab_actual = notebook_central.winfo_children()[indice_actual].winfo_children()[0]
            codeview = tab_actual.winfo_children()[0]
            codeview.bind("<KeyRelease>", lambda e: oyente_cambio_texto_tab(codeview, indice_actual, e))

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

# OPCIONES PARA EL MENU DE HERRAMIENTAS

def crear_bd():
    nombre = simpledialog.askstring("Nueva BD", "Ingresa el nombre de la nueva base de datos")

    if nombre:
        if re.match(r'^[a-zA-Z0-9_]+$', nombre) is not None:
            respuesta = crear_base_de_datos(nombre)
            messagebox.showinfo("Informacion", respuesta)
            mostrar_componentes_del_lenguaje()
        else:
            messagebox.showerror("Error", "Nombre no valido.")

def eliminar_bd():

    if os.path.exists(CARPETA_PARA_BASES_DE_DATOS): # Se valida que exista la base de datos

        # Crear la ventana_eliminar
        ventana_eliminar = tk.Toplevel(root)
        ventana_eliminar.title("Eliminar BD")

        # Obtiene todas las bases de datos
        opciones = os.listdir(CARPETA_PARA_BASES_DE_DATOS)

        # Variable para almacenar la opción seleccionada
        variable = tk.StringVar(ventana_eliminar)
        variable.set(opciones[0])  # Establecer el valor predeterminado

        # Crear el DropDown List
        dropdown = ttk.Combobox(ventana_eliminar, values=opciones, textvariable=variable)
        dropdown.pack(pady=10)

        # Crear el botón OK
        boton_ok = tk.Button(ventana_eliminar, text="OK", command=lambda: comando_eliminar_bd(variable, ventana_eliminar))
        boton_ok.pack()

        # Ajustar el tamaño de la ventana_eliminar
        ventana_eliminar.geometry("300x80")  # Ajusta según tus necesidades

        # Centrar la ventana_eliminar en la pantalla
        ancho_ventana = ventana_eliminar.winfo_reqwidth()
        alto_ventana = ventana_eliminar.winfo_reqheight()
        posicion_x = int((ventana_eliminar.winfo_screenwidth() - ancho_ventana) / 2)
        posicion_y = int((ventana_eliminar.winfo_screenheight() - alto_ventana) / 2)
        ventana_eliminar.geometry(f"+{posicion_x}+{posicion_y}")

        # Iniciar el bucle principal
        ventana_eliminar.mainloop()

def seleccionar_bd():

    if os.path.exists(CARPETA_PARA_BASES_DE_DATOS): # Se valida que exista la base de datos

        # Crear la ventana_seleccionar
        ventana_seleccionar = tk.Toplevel(root)
        ventana_seleccionar.title("Seleccionar BD")

        # Obtiene todas las bases de datos
        opciones = os.listdir(CARPETA_PARA_BASES_DE_DATOS)

        # Variable para almacenar la opción seleccionada
        variable = tk.StringVar(ventana_seleccionar)
        variable.set(opciones[0])  # Establecer el valor predeterminado

        # Crear el DropDown List
        dropdown = ttk.Combobox(ventana_seleccionar, values=opciones, textvariable=variable)
        dropdown.pack(pady=10)

        # Crear el botón OK
        boton_ok = tk.Button(ventana_seleccionar, text="OK", command=lambda: comando_seleccionar_bd(variable, ventana_seleccionar))
        boton_ok.pack()

        # Ajustar el tamaño de la ventana_seleccionar
        ventana_seleccionar.geometry("300x80")  # Ajusta según tus necesidades

        # Centrar la ventana_seleccionar en la pantalla
        ancho_ventana = ventana_seleccionar.winfo_reqwidth()
        alto_ventana = ventana_seleccionar.winfo_reqheight()
        posicion_x = int((ventana_seleccionar.winfo_screenwidth() - ancho_ventana) / 2)
        posicion_y = int((ventana_seleccionar.winfo_screenheight() - alto_ventana) / 2)
        ventana_seleccionar.geometry(f"+{posicion_x}+{posicion_y}")

        # Iniciar el bucle principal
        ventana_seleccionar.mainloop()

keyboard.add_hotkey('F6', ejecutar_query)
keyboard.add_hotkey('ctrl+n', crear_tab_nuevo)
keyboard.add_hotkey('ctrl+o', abrir)
keyboard.add_hotkey('ctrl+s', guardar)

# Creacion de ventana principal
root = tk.Tk()
root.title("MiSQL")
root.geometry(str(ANCHO_VENTANA) + "x" + str(ALTURA_VENTANA))
root.option_add("*tearOff", 0)

style = ttk.Style()
style.theme_use("default")

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
file_menu.add_command(label="Nuevo (Ctrl+n)", command=crear_tab_nuevo)
file_menu.add_command(label="Abrir (Ctrl+o)", command=abrir)
file_menu.add_command(label="Guardar (Ctrl+s)", command=guardar)
file_menu.add_command(label="Guardar como", command=guardar_como)
file_menu.add_command(label="Cerrar", command=cerrar_tab_actual)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=salir)

# Menu de herramientas
tool_menu = tk.Menu(menubar)

# Submenu 'Bases de datos'
submenu_bd = tk.Menu(tool_menu)
submenu_bd.add_command(label="Crear nuevo", command=crear_bd)
submenu_bd.add_command(label="Eliminar", command=eliminar_bd)
submenu_bd.add_command(label="Crear DUMP")
submenu_bd.add_command(label="Seleccionar", command=seleccionar_bd)
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
panel_1 = PanedWindow(bd=2, relief="flat", bg="#5D6D7E")
panel_1.pack(fill="both", expand=1)

# -------------------------------------------
# Panel izquierdo dentro del panel principal
treeview = ttk.Treeview()
treeview.tag_configure('estilo_titulos', font=('TkDefaultFont', 10, 'bold'))
treeview.tag_configure('estilo_carpetas', font=('TkDefaultFont', 8, 'bold'))
treeview.pack()
panel_1.add(treeview)
# Se agrega un sub panel dentro del panel principal
panel_2 = PanedWindow(panel_1, orient="vertical", bd=1, relief="flat", bg="#5D6D7E")
panel_1.add(panel_2)
mostrar_componentes_del_lenguaje()
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

mostrar_salida_como_texto("")
# -------------------------------------------

root.update()
root.mainloop()