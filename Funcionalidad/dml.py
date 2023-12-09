import os
import xml.etree.ElementTree as ET
from .util import Respuesta, validar_tipo_dato
from dotenv import load_dotenv

load_dotenv()

class DML:

    def __init__(self):
        self.__path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"
        self.__path_tablas = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_TABLAS"))
        self.__path_funciones = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_FUNCIONES"))
        self.__path_procedimiento = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

    def __validar_estructura_tupla(self, nombre_bd: str, path_tabla: str, tupla: list) -> str | dict:

        # Se crea una variable que almacenara toda la informacion de los campos a registrar
        tupla_respuesta = {}

        # Se obtiene la raiz del XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Buscar la definicion de los campos de la tabla en la estructura
        campos = root.findall(".//estructura/campo")

        # Se valida cada dato de la tupla segun la estructura de la tabla
        for campo in campos:

            campo_nombre = campo.attrib['name']

            # Si no viene un campo perteneciente a la tabla, se verifica si es nulleable o no
            if campo_nombre not in tupla:

                # Debido a que el campo no viene, se debe validar si puede ser NULL o no
                if 'nullable' not in campo.attrib:
                    return "El campo '" + campo_nombre + "' no puede de ser NULL"

            # Debido a que el campo viene, hay que validar su restriccion segun el tipo de dato
            else:

                # En el caso que el parametro sea nchar o nvarchar se define una variable con su longitud
                longitud = campo.attrib['length'] if 'length' in campo.attrib else None

                # Se valida el tipo de dato
                val_campo = validar_tipo_dato(campo_nombre, tupla[campo_nombre], campo.attrib['type'], longitud)
                if val_campo is not None:
                    return val_campo

                # Si es una llave primaria se valida que no se repita su valor
                if 'pk' in campo.attrib:
                    encontrado = root.findall(".//registros/fila[id='" + tupla[campo_nombre] + "']")
                    if len(encontrado) > 0:
                        return "No se pueden duplicar valores en la clave primaria"

                # Si es una llave foranea se valida que exista su valor en la tabla de referencia
                if 'fk_table' in campo.attrib:
                    # Se obtiene la raiz de la tabla de referencia
                    tree = ET.parse(self.__path_tablas.format(nombre_bd) + campo.attrib['fk_table'] + ".xml")
                    root = tree.getroot()

                    # Se busca y se valida que exista el valor
                    campos = root.findall(".//registros/fila[" + campo.attrib['fk_attribute'] + "='" + tupla[campo_nombre] + "']")
                    if len(campos) <= 0:
                        return "La clave " + tupla[campo_nombre] + " no se encuentra en la tabla " + campo.attrib['fk_table']

                # Se almacena el dato en la tupla de respuesta
                tupla_respuesta[campo_nombre] = tupla[campo_nombre]

                # Se elimina la llave de la tupla para que posteriormente se pueda evaluar si se utilizaron campos que no existen en la estructura de la tabla
                del tupla[campo_nombre]

        # Debido a que puede ir parametros desconocidos en la tupla, se valida que no vengan demas
        if len(tupla) > 0:
            campos_invalidos = ", ".join(list(tupla.keys()))
            return "Los siguientes campos son invalidas: " + campos_invalidos

        return tupla_respuesta

    ##############################################
    ############### SECCION INSERT ###############
    ##############################################

    def insertar_registro_tabla(self, nombre_bd:str, nombre_tabla: str, tupla: list) -> str:
        '''
        Ingresa una tupla en una tabla

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla (str): Nombre de la tabla
            tupla (list): Diccionario de los parametros que viene como
            {
                llave (campo): valor (valor del campo), ...
            }
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")

        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        val_estructura_tupla = self.__validar_estructura_tupla(nombre_bd, path_tabla, tupla)

        # Este es el caso que la estructura de la tupla es valida
        if isinstance(val_estructura_tupla, dict):

            # Se obtiene la raiz del XML
            tree = ET.parse(path_tabla)
            root = tree.getroot()

            # Se obtiene la definicion de los registros
            registros = root.find(".//registros")

            # Crear un nuevo elemento fila
            fila = ET.Element("fila")

            # Se agrega los elementos del registro a la fila
            for llave, valor in val_estructura_tupla.items():
                ET.SubElement(fila, llave).text = valor

            # Agregar el nuevo elemento al elemento registros
            registros.append(fila)

            # Guardar el árbol XML actualizado en el mismo archivo
            tree.write(path_tabla)

            return Respuesta(True, "INSERT 1")
        # Este es el caso que la estructura de la tupla es valida
        else:
            return Respuesta(False, val_estructura_tupla)
