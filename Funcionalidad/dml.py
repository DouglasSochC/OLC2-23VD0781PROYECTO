import os
import xml.etree.ElementTree as ET
from .util import Respuesta, validar_tipo_dato
from dotenv import load_dotenv
from Parser.abstract.retorno import TIPO_DATO, RetornoRelacional
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

    def __tipo_dato_campo(self, path_tabla: str, nombre_tabla: str, nombre_campo: str) -> dict | None:

        if nombre_campo == "":
            return "Debe de indicar el campo"

        # Lee el contenido del archivo XML
        with open(path_tabla, 'r') as archivo:
            contenido_xml = archivo.read()

        # Se formatea el XML a un diccionario para manejarlo de mejor forma
        contenido = xmltodict.parse(contenido_xml)

        # Se verifica que exista el campo y ademas se obtiene el tipo de dato de ese campo
        for campo in contenido[nombre_tabla]['estructura']['campo']:

            if campo["@name"] == nombre_campo:
                return campo["@type"]

        return None

    def __cumple_condicion(self, condiciones: list) -> bool:

        cumple_condicion = True

        for condicion in condiciones:

            if isinstance(condicion, tuple):

                # Se obtiene la estructura de la condicion
                op_izq = condicion[0]
                operador = condicion[1]
                op_der = condicion[2]

                # Se verifica que la condicion se cumpla
                if operador == '=' and str(op_izq) != str(op_der):
                    cumple_condicion = False
                if operador == '==' and str(op_izq) != str(op_der):
                    cumple_condicion = False
                elif operador == '>=' and op_izq < op_der:
                    cumple_condicion = False
                elif operador == '>' and op_izq <= op_der:
                    cumple_condicion = False
                elif operador == '<=' and op_izq > op_der:
                    cumple_condicion = False
                elif operador == '<' and op_izq >= op_der:
                    cumple_condicion = False

            else:
                if condicion == 'AND':
                    pass
                elif condicion == 'OR':
                    cumple_condicion = True

        return cumple_condicion

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

    def seleccionar_columna_tabla(self, nombre_bd:str, nombre_tabla: str, nombre_columna:str):
        '''
        Obtiene la informacion de una columna

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla (str): Nombre de la tabla
            nombre_columna (str): Todos los datos que contiene la columna
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif nombre_columna is None:  # Se valida que este el nombre de la columna
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

        respuesta_datos = [] # Variable que almacenara toda la informacion obtenida
        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        # Se obtiene el tipo de dato del campo
        res_tipo_campo = self.__tipo_dato_campo(path_tabla, nombre_tabla, nombre_columna)
        if res_tipo_campo is None:
            return Respuesta(False, "La columna '{}' es invalida".format(nombre_columna))

        # Lee el archivo XML
        with open(path_tabla, 'r') as archivo:
            contenido_xml = archivo.read()

        # Se formatea el XML a un diccionario para manejarlo de mejor forma
        contenido = xmltodict.parse(contenido_xml)[nombre_tabla]['registros']['fila']
        tipo_dato = None

        if isinstance(contenido, dict):
            contenido = [contenido]

        # Se recorre fila por fila
        for fila in contenido:

            # Se ingresa a la fila la columna que se esta solicitando casteandolo al tipo de dato a utilizar
            if res_tipo_campo == 'int':
                fila["temporal"] = int(fila[nombre_columna]) if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.INT
            elif res_tipo_campo == 'decimal':
                fila["temporal"] = float(fila[nombre_columna]) if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.DECIMAL
            elif res_tipo_campo == 'bit':
                fila["temporal"] = int(fila[nombre_columna]) if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.BIT
            elif res_tipo_campo == 'date':
                fila["temporal"] =str(fila[nombre_columna]) if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.DATE
            elif res_tipo_campo == 'datetime':
                fila["temporal"] =str(fila[nombre_columna]) if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.DATETIME
            elif res_tipo_campo == 'nchar':
                fila["temporal"] = fila[nombre_columna] if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.NCHAR
            elif res_tipo_campo == 'nvarchar':
                fila["temporal"] = fila[nombre_columna] if nombre_columna in fila else None
                tipo_dato = TIPO_DATO.NVARCHAR

            respuesta_datos.append(fila)

        return Respuesta(True, tipo_dato, respuesta_datos)

    def obtener_todas_las_columnas_tabla(self, nombre_bd:str, nombre_tabla: str):

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))
        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        # Lee el archivo XML
        with open(path_tabla, 'r') as archivo:
            contenido_xml = archivo.read()

        respuesta = []
        # Se formatea el XML a un diccionario para manejarlo de mejor forma
        contenido = xmltodict.parse(contenido_xml)[nombre_tabla]['estructura']['campo']
        for campo in contenido:
            respuesta.append(campo['@name'])

        return respuesta

    def obtener_indices_segun_condiciones(self, nombre_bd:str, nombre_tabla: str, listado_condiciones: list):

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))
        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        auxiliar = {}
        indices = []
        for condicion in listado_condiciones:

            # Se verifica si viene AND
            if isinstance(condicion, RetornoRelacional):

                # Se verifica que la operacion derecha sea lista igual que el de la izquierda. Se considera que ambas listas tienen las mismas dimensiones
                if isinstance(condicion.operacion_derecha, list):
                    if len(auxiliar) > 0:
                        for llave, valor in enumerate(condicion.operacion_izquierda):
                            auxiliar[valor['@index']].append((valor['temporal'], condicion.operador, condicion.operacion_derecha[llave]['temporal']))
                    else:
                        for llave, valor in enumerate(condicion.operacion_izquierda):
                            auxiliar[valor['@index']] = ([(valor['temporal'], condicion.operador, condicion.operacion_derecha[llave]['temporal'])])
                else:
                    if len(auxiliar) > 0:
                        for valor in condicion.operacion_izquierda:
                            auxiliar[valor['@index']].append((valor['temporal'], condicion.operador, condicion.operacion_derecha))
                    else:
                        for valor in condicion.operacion_izquierda:
                            auxiliar[valor['@index']] = ([(valor['temporal'], condicion.operador, condicion.operacion_derecha)])
            else:
                for llave in auxiliar:
                    auxiliar[llave].append(condicion)

        if len(auxiliar) > 0:
            for clave, valor in auxiliar.items():
                res_cumple_condicion = self.__cumple_condicion(valor)
                if res_cumple_condicion:
                    indices.append(clave)
        else:
            # Lee el archivo XML
            with open(path_tabla, 'r') as archivo:
                contenido_xml = archivo.read()

            # Se formatea el XML a un diccionario para manejarlo de mejor forma
            contenido = xmltodict.parse(contenido_xml)[nombre_tabla]['registros']['fila']
            if isinstance(contenido, list):
                for fila in contenido:
                    indices.append(fila['@index'])
            else:
                indices.append(contenido['@index'])

        return indices

    def sintetizar_condiciones(self, data: list, lista_indices: list):

        respuesta_datos = [] # Variable que almacenara toda la informacion obtenida

        for fila in data:

            # Se identifica si el index esta dentro del listado de indices disponibles para mostrar
            if fila["@index"] in lista_indices:
                respuesta_datos.append(fila['temporal'])

        return Respuesta(True, None, respuesta_datos)

    ##############################################
    ############### SECCION DELETE ###############
    ##############################################

    def eliminar_filas(self, nombre_bd:str, nombre_tabla: str, lista_indices: list):

            if nombre_bd is None: # Se valida que haya seleccionado una base de datos
                return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
            elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
                return Respuesta(False, "Por favor, indique el nombre de la tabla")
            elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
                return Respuesta(False, "No existe la base de datos seleccionada")
            elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
                return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

            path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

            # Se obtiene la raiz del XML
            tree = ET.parse(path_tabla)
            root = tree.getroot()

            cantidad_registros_eliminados = 0
            for indice in lista_indices:

                # Buscar y eliminar el registro con el indice especificado
                registro_a_eliminar = root.find(f"./registros/fila[@index='{indice}']")
                if registro_a_eliminar is not None:
                    root.find('./registros').remove(registro_a_eliminar)
                    cantidad_registros_eliminados += 1

            # Guardar el resultado en un nuevo archivo XML
            tree.write(path_tabla)

            return Respuesta(True, "DELETE {}".format(cantidad_registros_eliminados))