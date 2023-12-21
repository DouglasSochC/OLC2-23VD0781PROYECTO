import os
import xml.etree.ElementTree as ET
from .util import Respuesta, validar_tipo_dato
from dotenv import load_dotenv
from Parser.abstract.retorno import TIPO_DATO
import xmltodict

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

        # Todos los valores de la tupla se castean a 'str' para que no haya problemas
        tupla = {clave: str(valor) for clave, valor in tupla.items()}

        # Se obtiene la raiz del XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Buscar la definicion de los campos de la tabla en la estructura
        campos = root.findall(".//estructura/campo")

        # Se valida cada dato de la tupla segun la estructura de la tabla
        for campo in campos:

            campo_nombre = campo.attrib['name']

            # Si no viene un campo perteneciente a la tabla, se verifica si es not_null
            if campo_nombre not in tupla:

                if 'pk' in campo.attrib:
                    return "La llave primaria '{}' no puede de ser NULL".format(campo_nombre)

                # Debido a que el campo no viene, se debe validar si puede ser NULL o no
                if 'not_null' in campo.attrib:
                    return "El campo '{}' no puede de ser NULL".format(campo_nombre)

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
                        return "La clave '{}' no se encuentra en la tabla '{}'.".format(tupla[campo_nombre], campo.attrib['fk_table'])

                # Se almacena el dato en la tupla de respuesta
                tupla_respuesta[campo_nombre] = tupla[campo_nombre]

                # Se elimina la llave de la tupla para que posteriormente se pueda evaluar si se utilizaron campos que no existen en la estructura de la tabla
                del tupla[campo_nombre]

        # Debido a que puede ir parametros desconocidos en la tupla, se valida que no vengan demas
        if len(tupla) > 0:
            campos_invalidos = ", ".join(list(tupla.keys()))
            return "Los siguientes campos son invalidas: {}".format(campos_invalidos)

        return tupla_respuesta

    def __convertir_a_literal(self, valor: any, tipo_dato: str) -> any:

            if tipo_dato == 'int':
                return {'valor': int(valor), 'tipo': TIPO_DATO.INT}
            elif tipo_dato == 'decimal':
                return {'valor': float(valor), 'tipo': TIPO_DATO.DECIMAL}
            elif tipo_dato == 'bit':
                return {'valor': int(valor), 'tipo': TIPO_DATO.BIT}
            elif tipo_dato == 'date':
                return {'valor': str(valor), 'tipo': TIPO_DATO.DATE}
            elif tipo_dato == 'datetime':
                return {'valor': str(valor), 'tipo': TIPO_DATO.DATETIME}
            elif tipo_dato == 'nchar':
                return {'valor': str(valor), 'tipo': TIPO_DATO.NCHAR}
            elif tipo_dato == 'nvarchar':
                return {'valor': str(valor), 'tipo': TIPO_DATO.NVARCHAR}

    ##############################################
    ############### SECCION INSERT ###############
    ##############################################

    def insertar_registro_tabla(self, nombre_bd:str, nombre_tabla: str, tupla: list) -> Respuesta:
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
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        val_estructura_tupla = self.__validar_estructura_tupla(nombre_bd, path_tabla, tupla)

        # Este es el caso que la estructura de la tupla es valida
        if isinstance(val_estructura_tupla, dict):

            # Se obtiene la raiz del XML
            tree = ET.parse(path_tabla)
            root = tree.getroot()

            # Se obtiene la definicion de los registros
            registros = root.find(".//registros")

            ultima_posicion = registros.findall(".//fila")
            index = '1'
            if len(ultima_posicion) > 0:
                acum = registros.findall(".//fila")[-1].get("index")
                index = str(int(acum) + 1)

            # Crear un nuevo elemento fila
            fila = ET.Element("fila", attrib={'index' : index})

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

    ##############################################
    ############### SECCION SELECT ###############
    ##############################################

    def obtener_datos_tabla(self, nombre_bd: str, nombre_tabla:str):
        '''
        Obtiene todos los datos de una tabla

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla (str): Nombre de la tabla
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

        respuesta_datos = [] # Variable que almacenara toda la informacion obtenida
        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        # Lee el archivo XML
        with open(path_tabla, 'r') as archivo:
            contenido_xml = archivo.read()

        # Se formatea el XML a un diccionario para manejarlo de mejor forma
        contenido = xmltodict.parse(contenido_xml)[nombre_tabla]['registros']['fila']
        estructura = xmltodict.parse(contenido_xml)[nombre_tabla]['estructura']['campo']

        if isinstance(contenido, dict):
            contenido = [contenido]

        # Se recorre fila por fila
        for fila in contenido:

            fila_tipada = {}
            for tipado in estructura:

                fila_tipada['{}.@index'.format(nombre_tabla)] = fila['@index']
                if tipado['@name'] in fila:
                    conversion_literal = self.__convertir_a_literal(fila[tipado['@name']], tipado['@type'])
                    fila_tipada[nombre_tabla + "." + tipado['@name']] = { 'valor': conversion_literal['valor'], 'tipado': conversion_literal['tipo'] }
                else:
                    conversion_literal = self.__convertir_a_literal(-1, tipado['@type'])
                    fila_tipada[nombre_tabla + "." + tipado['@name']] = { 'valor': None, 'tipado': conversion_literal['tipo'] }

            respuesta_datos.append(fila_tipada)

        return Respuesta(True, None, respuesta_datos)

    def verificar_columna_tabla(self, nombre_bd: str, datos: list, nombre_columna:str, nombre_tabla:str = None) -> Respuesta:

        # Se busca en que tabla se encuentra la columna
        if nombre_tabla is None:

            # Se obtienen todas las tablas existentes de la base de datos
            tablas = os.listdir(self.__path_tablas.format(nombre_bd))
            # Variable que valida si existe alguna ambiguedad
            ambiguedad = 0

            # Se evalua tabla por tabla para verificar que la informacion a eliminar no este enlazada a otra tabla a traves de una llave foranea
            for tabla in tablas:

                # Se obtienen todos registros que contiene la tabla
                path_tabla = self.__path_tablas.format(nombre_bd) + tabla
                with open(path_tabla, 'r') as archivo:
                    contenido_xml = archivo.read()

                # Se formatea el XML a un diccionario para manejarlo de mejor forma
                campos = xmltodict.parse(contenido_xml)[tabla.split(".")[0]]['estructura']['campo']

                # Se recorre cada campo de la tabla
                for campo in campos:

                    # Se verifica si el campo es igual al que se desea eliminar
                    if campo['@name'] == nombre_columna:
                        ambiguedad += 1
                        nombre_tabla = tabla.split(".")[0]

            if ambiguedad > 1:
                return Respuesta(False, "La columna '{}' se encuentra en mas de una tabla, por favor, especifique en que tabla se encuentra.".format(nombre_columna), None)
        else:

            if not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
                return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

            existe_campo = False

            # Se obtienen todos registros que contiene la tabla
            path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"
            with open(path_tabla, 'r') as archivo:
                contenido_xml = archivo.read()

            # Se formatea el XML a un diccionario para manejarlo de mejor forma
            campos = xmltodict.parse(contenido_xml)[nombre_tabla]['estructura']['campo']
             # Se recorre cada campo de la tabla
            for campo in campos:

                # Se verifica si el campo es igual al que se desea eliminar
                if campo['@name'] == nombre_columna:
                    existe_campo = True
                    break

        if nombre_tabla is None:
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla), None)
        elif existe_campo is False:
            return Respuesta(False, "La columna '{}' no se encuentra en la tabla '{}'.".format(nombre_columna, nombre_tabla), None)

        # # El 'valor' de la respuesta tendra el nombre de la tabla
        # # La 'lista' de la respuesta tendra todo el contenido que tiene la tabla
        return Respuesta(True, nombre_tabla, datos[nombre_tabla])
