import os
import xml.etree.ElementTree as ET
from .util import validar_tipo_dato
from dotenv import load_dotenv

load_dotenv()
__CARPETA_PARA_BASES_DE_DATOS = str(os.environ.get("CARPETA_PARA_BASES_DE_DATOS"))
__CARPETA_PARA_TABLAS = str(os.environ.get("CARPETA_PARA_TABLAS"))
__CARPETA_PARA_FUNCIONES = str(os.environ.get("CARPETA_PARA_FUNCIONES"))
__CARPETA_PARA_PROCEDIMIENTOS = str(os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

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

def __validar_atributos(path_xml: str, atributos: list) -> str | dict:

    if len(atributos) <= 0:
        return "Debe de seleccionar por lo menos una columna"

    # Se crea una variable que devolvera un diccionario de los atributos
    atributos_respuesta = []

    # Se obtiene la raiz del XML
    tree = ET.parse(path_xml)
    root = tree.getroot()

    # Buscar la definicion de los campos de la tabla en la estructura
    campos = root.find(".//estructura")

    # Se valida cada dato de la atributos segun la estructura de la tabla
    for campo in campos.findall('./campo'):

        campo_nombre = campo.attrib['name']

        # Se verifica que venga el campo
        if campo_nombre in atributos:
            atributos_respuesta.append(campo_nombre)
            atributos.remove(campo_nombre)

    # Debido a que puede ir parametros desconocidos en la atributos parametro, se valida que no vengan demas
    if len(atributos) > 0:
        campos_invalidos = ", ".join(list(atributos))
        return "Las siguientes columnas son invalidas: " + campos_invalidos

    return atributos_respuesta

def __validar_condicion(path_xml: str, condiciones: list) -> str | dict:
    # Se crea una variable que devolvera un diccionario del registro a insertar
    tupla_respuesta = {}

    # Se obtiene la raiz del XML
    tree = ET.parse(path_xml)
    root = tree.getroot()

    # Buscar la definicion de los campos de la tabla en la estructura
    campos = root.find(".//estructura")

    # Se valida cada dato de la condiciones segun la estructura de la tabla
    for campo in campos.findall('./campo'):

        campo_nombre = campo.attrib['name']

        # Se verifica que venga el campo
        if campo_nombre not in condiciones:

            # Debido a que el campo no viene, se debe validar si puede ser NULL o no
            if campo.attrib['nullable'] == 'false':
                return "El campo '" + campo_nombre + "' no puede de ser NULL"
        else:

            # Debido a que el campo viene, hay que validar su restriccion segun el tipo de dato
            longitud = campo.attrib['length'] if 'length' in campo.attrib else None
            val_campo = validar_tipo_dato(campo_nombre, condiciones[campo_nombre], campo.attrib['type'], longitud)
            if val_campo is not None:
                return val_campo

            # Se almacena el dato en la condiciones de respuesta y se elimina la llave para la condiciones parametro de este metodo
            tupla_respuesta[campo_nombre] = condiciones[campo_nombre]
            del condiciones[campo_nombre]

    # Debido a que puede ir parametros desconocidos en la condiciones parametro, se valida que no vengan demas
    if len(condiciones) > 0:
        campos_invalidos = ", ".join(list(condiciones.keys()))
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

    path_tabla = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_TABLAS + nombre_tabla + ".xml"
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

def seleccionar_registro_tabla(nombre_bd:str, nombre_tabla: str, atributos: list, condiciones: list):

    datos = []
    path_tabla = __CARPETA_PARA_BASES_DE_DATOS + nombre_bd + __CARPETA_PARA_TABLAS + nombre_tabla + ".xml"

    # Se validan los atributos
    val_atributos = __validar_atributos(path_tabla, atributos)
    # val_condicion = __validar_condicion(path_tabla, condiciones)

    # Este es el caso que los atributos son validos para la tabla seleccionada
    if isinstance(val_atributos, str):
        return val_atributos
    # elif isinstance(val_condicion, str):
    #     return "hola"
    else:
        # Se obtiene la raiz del XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Se obtiene la definicion de los registros
        registros = root.find(".//registros")

        # Se obtiene cada fila
        filas = registros.findall(".//fila")
        for fila in filas:

            # Accede a los elementos dentro de la fila
            elementos_fila = fila.findall(".//*")

            # Se almacenan en una variable para que esta pueda aplicarsele las condiciones
            resultado_fila = {}
            for elemento in elementos_fila:
                resultado_fila[elemento.tag] = elemento.text
            datos.append(resultado_fila)

        return datos