import os
from .util import Respuesta, validar_tipo_dato
from Parser.abstract.retorno import TIPO_DATO
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()

class SSL:

    def __init__(self):
        self.__path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"
        self.__path_funcion = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_FUNCIONES"))
        self.__path_procedimiento = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

    def verificar_parametros_procedimiento_y_obtener_query(self, nombre_bd: str, nombre_procedimiento: str, lista_parametros: list):

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_procedimiento is None:  # Se valida que este el nombre del procedimiento
            return Respuesta(False, "Por favor, indique el nombre del procedimiento")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_procedimiento.format(nombre_bd) + nombre_procedimiento + ".xml"): # Se valida que exista el procedimiento
            return Respuesta(False, "El procedimiento '{}' no se encuentra en la base de datos.".format(nombre_procedimiento))

        path_funcion = self.__path_procedimiento.format(nombre_bd) + nombre_procedimiento + ".xml"

        # Parsear el archivo XML
        tree = ET.parse(path_funcion)
        root = tree.getroot()

        # Se obtienen todos los campos
        campos_procedimiento = root.findall('.//estructura/campo')

        # Se verifica si el procedimiento no hace uso de parametros
        if campos_procedimiento is None and len(lista_parametros) > 0:
            return Respuesta(False, "El procedimiento '{}' no hace uso de parámetros.".format(nombre_procedimiento))

        # El procedimiento no hace uso de parametros y no se especificaron parametros
        elif campos_procedimiento is None and len(lista_parametros) == 0:
            return Respuesta(True, "Los parametros son correctos")

        # Se verifica si el procedimiento hace uso de parametros
        elif campos_procedimiento is not None and len(lista_parametros) == 0:
            return Respuesta(False, "El procedimiento '{}' requiere la especificación de sus parámetros para su correcta ejecución.".format(nombre_procedimiento))

        # Se verifica si la cantidad de parametros es igual a la cantidad de campos
        elif campos_procedimiento is not None and  len(campos_procedimiento) != len(lista_parametros):
            return Respuesta(False, "La cantidad de parametros no coincide con la cantidad de campos del procedimiento '{}'.".format(nombre_procedimiento))

        # Se verifica parametro por parametro
        variables_nuevas = ""
        for indice, valor in enumerate(campos_procedimiento):

            validar_tipo = validar_tipo_dato(valor.get('name'), lista_parametros[indice]['valor'], valor.get('type'), len(str(lista_parametros[indice]['valor'])) if lista_parametros[indice]['tipado'] in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else None)
            if validar_tipo is not None:
                return Respuesta(False, validar_tipo)

            # Se declara la variable
            variables_nuevas += "DECLARE {} AS {};\n".format(valor.get('name'), "{}({})".format(valor.get('type'), valor.get('length')) if lista_parametros[indice]['tipado'] in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else valor.get('type'))
            # Se setea su valor
            valor_comillas_sin_comillas = "'{}'".format(lista_parametros[indice]['valor']) if lista_parametros[indice]['tipado'] in (TIPO_DATO.DATE, TIPO_DATO.DATETIME, TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else lista_parametros[indice]['valor']
            variables_nuevas += "SET {} = {};".format(valor.get('name'), valor_comillas_sin_comillas)

        # Todo esta correctamente entonces se obtiene el query del procedimiento
        query = root.find('.//query')
        return Respuesta(True, variables_nuevas + query.text)

    def verificar_parametros_funcion_y_obtener_query(self, nombre_bd: str, nombre_funcion: str, lista_parametros: list):

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_funcion is None:  # Se valida que este el nombre del funcion
            return Respuesta(False, "Por favor, indique el nombre del funcion")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_funcion.format(nombre_bd) + nombre_funcion + ".xml"): # Se valida que exista el funcion
            return Respuesta(False, "La funcion '{}' no se encuentra en la base de datos.".format(nombre_funcion))

        path_funcion = self.__path_funcion.format(nombre_bd) + nombre_funcion + ".xml"

        # Parsear el archivo XML
        tree = ET.parse(path_funcion)
        root = tree.getroot()

        # Se obtienen todos los campos
        campos_funcion = root.findall('.//estructura/campo')

        # Se verifica si el funcion no hace uso de parametros
        if campos_funcion is None and len(lista_parametros) > 0:
            return Respuesta(False, "El funcion '{}' no hace uso de parámetros.".format(nombre_funcion))

        # El funcion no hace uso de parametros y no se especificaron parametros
        elif campos_funcion is None and len(lista_parametros) == 0:
            return Respuesta(True, "Los parametros son correctos")

        # Se verifica si el funcion hace uso de parametros
        elif campos_funcion is not None and len(lista_parametros) == 0:
            return Respuesta(False, "El funcion '{}' requiere la especificación de sus parámetros para su correcta ejecución.".format(nombre_funcion))

        # Se verifica si la cantidad de parametros es igual a la cantidad de campos
        elif campos_funcion is not None and  len(campos_funcion) != len(lista_parametros):
            return Respuesta(False, "La cantidad de parametros no coincide con la cantidad de campos del funcion '{}'.".format(nombre_funcion))

        # Se verifica parametro por parametro
        variables_nuevas = ""
        for indice, valor in enumerate(campos_funcion):

            validar_tipo = validar_tipo_dato(valor.get('name'), lista_parametros[indice]['valor'], valor.get('type'), len(str(lista_parametros[indice]['valor'])) if lista_parametros[indice]['tipado'] in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else None)
            if validar_tipo is not None:
                return Respuesta(False, validar_tipo)

            # Se declara la variable
            variables_nuevas += "DECLARE {} AS {};\n".format(valor.get('name'), "{}({})".format(valor.get('type'), valor.get('length')) if lista_parametros[indice]['tipado'] in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else valor.get('type'))
            # Se setea su valor
            valor_comillas_sin_comillas = "'{}'".format(lista_parametros[indice]['valor']) if lista_parametros[indice]['tipado'] in (TIPO_DATO.DATE, TIPO_DATO.DATETIME, TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else lista_parametros[indice]['valor']
            variables_nuevas += "SET {} = {};".format(valor.get('name'), valor_comillas_sin_comillas)

        # Todo esta correctamente entonces se obtiene el query del funcion
        query = root.find('.//query')
        return Respuesta(True, variables_nuevas + query.text)
