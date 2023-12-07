import os
import xml.etree.ElementTree as ET

CARPETA_PARA_BASES_DE_DATOS='databases/'

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
    path_tabla = CARPETA_PARA_BASES_DE_DATOS + nombre_bd
    if not os.path.exists(path_tabla):
        os.makedirs(path_tabla)
        return "La base de datos creada correctamente."
    else:
        return "La base de datos ya existe."

def crear_tabla(nombre_bd:str, nombre_tabla: str, parametros: list):
    '''
    Crea una tabla nueva

    Parameters:
        nombre_bd (str): Nombre de la base de datos en la que realizara alguna funcionalidad
        nombre_tabla (str): Nombre de la tabla
        parametros (list): Este es un diccionario que debe llevar la siguiente estructura [{name, type, length, nullable: true|false, primary_key}]

    Returns:
        respuesta (str)
    '''

    if nombre_bd is None: # Se valida que haya seleccionado una base de datos
        return "No ha seleccionado una base de datos para realizar la transaccion"
    elif not os.path.exists(CARPETA_PARA_BASES_DE_DATOS + nombre_bd): # Se valida que exista la base de datos
        return "No existe la base de datos seleccionada"

    path_tabla = CARPETA_PARA_BASES_DE_DATOS + nombre_bd + "/" + nombre_tabla + ".xml"
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
            ET.SubElement(estructura, "campo", attrib=param)

        # Crea el árbol XML
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
    path_tabla = CARPETA_PARA_BASES_DE_DATOS + nombre_bd
    if not os.path.exists(path_tabla):
        return "La base de datos que desea eliminar no existe."
    else:
        os.rmdir(path_tabla)
        return "La base de datos ha sido eliminada correctamente."
