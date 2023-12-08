import os
import shutil
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
__CARPETA_PARA_BASES_DE_DATOS = str(os.environ.get("CARPETA_PARA_BASES_DE_DATOS"))
__CARPETA_PARA_TABLAS = str(os.environ.get("CARPETA_PARA_TABLAS"))
__CARPETA_PARA_FUNCIONES = str(os.environ.get("CARPETA_PARA_FUNCIONES"))
__CARPETA_PARA_PROCEDIMIENTOS = str(os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

def crear_base_de_datos(nombre_bd: str):
    '''
    Crea una base de datos nueva

    Parameters:
        nombre_bd (str): Nombre de la base de datos

    Returns:
        respuesta (str)
    '''

    # Se valida que se asigne un nombre a la base de datos
    if nombre_bd is None:
        return "Por favor, indique el nombre de la base de datos"

    # Se valida la existencia de la base de datos
    path_bd = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd
    if not os.path.exists(path_bd):
        os.makedirs(path_bd)
        path_tablas = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_TABLAS
        os.makedirs(path_tablas)
        path_funciones = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_FUNCIONES
        os.makedirs(path_funciones)
        path_procedimiento = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_PROCEDIMIENTOS
        os.makedirs(path_procedimiento)
        return "La base de datos creada correctamente."
    else:
        return "La base de datos ya existe."

def crear_tabla(nombre_bd:str, nombre_tabla: str, parametros: list):
    '''
    Crea una tabla nueva

    Parameters:
        nombre_bd (str): Nombre de la base de datos en la que realizara alguna funcionalidad
        nombre_tabla (str): Nombre de la tabla
        parametros (list): Este es un diccionario que debe llevar la siguiente estructura [{name (*), type (*), length (o), nullable (*): true|false, primary_key (o)}]

    Returns:
        respuesta (str)
    '''

    if nombre_bd is None: # Se valida que haya seleccionado una base de datos
        return "No ha seleccionado una base de datos para realizar la transaccion"
    elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
        return "Por favor, indique el nombre de la tabla"
    elif not os.path.exists(__CARPETA_PARA_BASES_DE_DATOS + nombre_bd): # Se valida que exista la base de datos
        return "No existe la base de datos seleccionada"

    path_tabla = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_TABLAS + nombre_tabla + ".xml"
    if os.path.exists(path_tabla): # Se valida que no exista la tabla
        return "La tabla ya existe."
    else:
        # Crea el elemento raiz con el nombre de la tabla
        root = ET.Element(nombre_tabla)

        # Crea el apartado de estructura de la tabla
        estructura = ET.SubElement(root, "estructura")

        # Crea el apartado de los registros de la tabla
        ET.SubElement(root, "registros")

        # Se agrega los campos que lleva la tabla
        for param in parametros:
            # Se valida que el nchar y nvarchar cumplan con la cantidad de caracteres valida segun la longitud restringida
            if param['type'] == 'nchar':
                if int(param['length']) <= 0:
                    return "El nchar del campo " + param['name'] + " debe de ser mayor a 1"
                elif int(param['length']) > 4000:
                    return "El nchar del campo " + param['name'] + " debe de ser menor a 4000"
            elif param['type'] == 'nvarchar':
                if int(param['length']) <= 0:
                    return "El nchar del campo " + param['name'] + " debe de ser mayor a 1"
                elif int(param['length']) > 2000000:
                    return "El nchar del campo " + param['name'] + " debe de ser menor a 2000000"
            ET.SubElement(estructura, "campo", attrib=param)

        # Crea el arbol XML
        tree = ET.ElementTree(root)

        # Escribe el árbol XML en un archivo
        with open(path_tabla, "wb") as archivo:
            tree.write(archivo)

        return "La tabla ha sido creada correctamente"

def eliminar_base_de_datos(nombre_bd: str):
    '''
    Elimina una base de datos existente

    Parameters:
        nombre_bd (str): Nombre de la base de datos

    Returns:
        respuesta (str)
    '''
    # Se valida que se asigne un nombre a la base de datos
    if nombre_bd is None:
        return "Por favor, indique el nombre de la base de datos"

    # Se valida la existencia de la base de datos
    path_tabla = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd
    if not os.path.exists(path_tabla):
        return "La base de datos que desea eliminar no existe."
    else:
        shutil.rmtree(path_tabla)
        return "La base de datos ha sido eliminada correctamente."
