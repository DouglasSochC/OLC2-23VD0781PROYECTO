import os
import xml.etree.ElementTree as ET
from .util import validar_tipo_dato

__CARPETA_PARA_BASES_DE_DATOS='databases/'

def __validar_estructura_tupla(path_xml: str, tupla: list) -> str | dict:

    # Se crea una variable que devolvera un diccionario del registro a insertar
    tupla_respuesta = {}

    # Se obtiene la raiz del XML
    tree = ET.parse(path_xml)
    root = tree.getroot()

    # Buscar la definicion de los campos de la tabla en la estructura
    campos = root.find(".//estructura")

    # Se valida cada dato de la tupla segun la estructura de la tabla
    for campo in campos.findall('./campo'):

        campo_nombre = campo.attrib['name']

        # Se verifica que venga el campo
        if campo_nombre not in tupla:

            # Debido a que el campo no viene, se debe validar si puede ser NULL o no
            if campo.attrib['nullable'] == 'false':
                return "El campo '" + campo_nombre + "' no puede de ser NULL"
        else:

            # Debido a que el campo viene, hay que validar su restriccion segun el tipo de dato
            longitud = campo.attrib['length'] if 'length' in campo.attrib else None
            val_campo = validar_tipo_dato(campo_nombre, tupla[campo_nombre], campo.attrib['type'], longitud)
            if val_campo is not None:
                return val_campo

            # Se almacena el dato en la tupla de respuesta y se elimina la llave para la tupla parametro de este metodo
            tupla_respuesta[campo_nombre] = tupla[campo_nombre]
            del tupla[campo_nombre]

    # Debido a que puede ir parametros desconocidos en la tupla parametro, se valida que no vengan demas
    if len(tupla) > 0:
        campos_invalidos = ", ".join(list(tupla.keys()))
        return "Las siguientes columnas son invalidas: " + campos_invalidos

    return tupla_respuesta

def insertar_registro_tabla(nombre_bd:str, nombre_tabla: str, tupla: list) -> str:
    '''
    Realiza un registro de una tupla a una tabla

    Parameters:
        nombre_bd (str): Nombre de la base de datos
        nombre_tabla (str): Nombre de la tabla
        tupla (list): Diccionario de los parametros que viene como {llave: valor, ...}
    '''

    if nombre_bd is None: # Se valida que haya seleccionado una base de datos
        return "No ha seleccionado una base de datos para realizar la transaccion"
    elif nombre_tabla is None:  # Se valida que haya seleccionado una tabla
        return "Por favor, indique el nombre de la tabla"
    elif not os.path.exists(__CARPETA_PARA_BASES_DE_DATOS + nombre_bd): # Se valida que exista la base de datos
        return "No existe la base de datos seleccionada"

    path_tabla = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + "/" + nombre_tabla + ".xml"
    respuesta = __validar_estructura_tupla(path_tabla, tupla)

    # Este es el caso que la estructura de la tupla es valida
    if isinstance(respuesta, dict):

        # Se obtiene la raiz del XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Se obtiene la definicion de los registros
        registros = root.find(".//registros")

        # Crear un nuevo elemento fila
        fila = ET.Element("fila")

        # Se agrega los elementos del registro a la fila
        for llave, valor in respuesta.items():
            ET.SubElement(fila, llave).text = valor

        # Agregar el nuevo elemento al elemento registros
        registros.append(fila)
        # Guardar el árbol XML actualizado en el mismo archivo
        tree.write(path_tabla)

        return "INSERT 1"
    # Este es el caso que la estructura de la tupla es valida
    else:
        return respuesta
