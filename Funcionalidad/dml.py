import os
import xml.etree.ElementTree as ET
from .util import Respuesta, validar_tipo_dato, convertir_a_literal
from dotenv import load_dotenv
import xmltodict

load_dotenv()

class DML:

    def __init__(self):
        self.__path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"
        self.__path_tablas = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_TABLAS"))

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
                    encontrado = root.findall(".//registros/fila[{}='{}']".format(campo_nombre, tupla[campo_nombre]))
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
    ############### SECCION UPDATE ###############
    ##############################################

    def actualizar_datos_tabla(self, nombre_bd: str, nombre_tabla: str, campos_a_actualizar: list, indices_a_actualizar: list) -> Respuesta:

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        # Parsear el archivo XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Se almacenan los campos con llaves foraneas para verificar que exista el valor en la tabla de referencia
        campos_con_llaves_foraneas = {}

        # Se verifica cada campo exista
        for nombre_campo in campos_a_actualizar:

            campo_encontrado = root.find('.//estructura/campo[@name="{}"]'.format(nombre_campo['columna']))

            if campo_encontrado is None:
                return Respuesta(False, "El campo '{}' no existe en la tabla '{}'.".format(nombre_campo['columna'], nombre_tabla))

            # Se verifica que cada campo tengan el formato y tipo de dato correcto
            elif campo_encontrado is not None and convertir_a_literal(-1, campo_encontrado.attrib['type'])['tipo'] != nombre_campo['tipado']:
                return Respuesta(False, "El campo '{}' no es del tipo de dato '{}'.".format(nombre_campo['columna'], campo_encontrado.attrib['type']))

            if "fk_table" in campo_encontrado.attrib:
                campos_con_llaves_foraneas[nombre_campo['columna']] = { "tabla": campo_encontrado.attrib["fk_table"], "id": campo_encontrado.attrib['fk_attribute']}

        cantidad_registros_actualizados = 0
        for indice in indices_a_actualizar:

            # Encontrar la fila con cierto index
            fila_a_editar = root.find('.//fila[@index="{}"]'.format(indice))

            # Verificar si se encontro la fila
            if fila_a_editar is not None:

                for campo in campos_a_actualizar:

                    elemento = fila_a_editar.find(campo['columna'])

                    # Se verifica si el campo es una llave foranea
                    if campo['columna'] in campos_con_llaves_foraneas:

                        # Se obtiene la raiz de la tabla de referencia
                        tree_tabla_referencia = ET.parse(self.__path_tablas.format(nombre_bd) + campos_con_llaves_foraneas[campo['columna']]['tabla'] + ".xml")
                        root_tabla_referencia = tree_tabla_referencia.getroot()

                        # Se busca y se valida que exista el valor
                        campos = root_tabla_referencia.findall('.//fila[{}="{}"]'.format(campos_con_llaves_foraneas[campo['columna']]['id'], campo['valor']))
                        if len(campos) <= 0:
                            return Respuesta(False, "La clave '{}' no se encuentra en la tabla '{}'.".format(campo['valor'], campos_con_llaves_foraneas[campo['columna']]['tabla']))

                    # Verificar si el elemento existe en la fila
                    if elemento is not None:
                        # Actualizar el valor del elemento
                        elemento.text = str(campo['valor'])
                    else:
                        # Si el elemento no existe, crearlo y actualizar su valor
                        nuevo_elemento = ET.Element(campo['columna'])
                        nuevo_elemento.text = str(campo['valor'])
                        fila_a_editar.append(nuevo_elemento)

                cantidad_registros_actualizados += 1

        # Guardar los cambios de vuelta en el archivo
        tree.write(path_tabla)

        return Respuesta(True, "UPDATE {}".format(cantidad_registros_actualizados))

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
        contenido = xmltodict.parse(contenido_xml)[nombre_tabla]['registros']
        if contenido is None:
            return Respuesta(True, None, [])
        contenido = contenido['fila']
        estructura = xmltodict.parse(contenido_xml)[nombre_tabla]['estructura']['campo']

        if isinstance(contenido, dict):
            contenido = [contenido]

        # Se recorre fila por fila
        for fila in contenido:

            fila_tipada = {}
            for tipado in estructura:

                fila_tipada['{}.@index'.format(nombre_tabla)] = fila['@index']
                if tipado['@name'] in fila:
                    conversion_literal = convertir_a_literal(fila[tipado['@name']], tipado['@type'])
                    fila_tipada[nombre_tabla + "." + tipado['@name']] = { 'valor': conversion_literal['valor'], 'tipado': conversion_literal['tipo'] }
                else:
                    conversion_literal = convertir_a_literal(-1, tipado['@type'])
                    fila_tipada[nombre_tabla + "." + tipado['@name']] = { 'valor': None, 'tipado': conversion_literal['tipo'] }

            respuesta_datos.append(fila_tipada)

        return Respuesta(True, None, respuesta_datos)

    def verificar_columna_tabla(self, nombre_bd: str, datos: list, nombre_columna:str, nombre_tabla:str = None, tablas_a_verificar: list = []) -> Respuesta:

        # Se busca en que tabla se encuentra la columna
        if nombre_tabla is None:

            # Variable que valida si existe alguna ambiguedad
            ambiguedad = 0

            # Se evalua tabla por tabla para verificar que la informacion a eliminar no este enlazada a otra tabla a traves de una llave foranea
            for tabla in tablas_a_verificar:

                # Se obtienen todos registros que contiene la tabla
                path_tabla = self.__path_tablas.format(nombre_bd) + tabla + ".xml"
                with open(path_tabla, 'r') as archivo:
                    contenido_xml = archivo.read()

                # Se formatea el XML a un diccionario para manejarlo de mejor forma
                campos = xmltodict.parse(contenido_xml)[tabla.split(".")[0]]['estructura']['campo']

                # Se recorre cada campo de la tabla
                for campo in campos:

                    # Se verifica si el campo es igual al que se desea eliminar
                    if campo['@name'] == nombre_columna:
                        ambiguedad += 1
                        nombre_tabla = tabla

            if ambiguedad == 0:
                return Respuesta(False, "La columna '{}' es invalida.".format(nombre_columna), None)
            elif ambiguedad > 1:
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

            if existe_campo is False:
                return Respuesta(False, "La columna '{}' no se encuentra en la tabla '{}'.".format(nombre_columna, nombre_tabla), None)

        if nombre_tabla not in datos:
            return Respuesta(False, "La consulta 'SELECT' no incluye la tabla '{}' en la cláusula FROM.".format(nombre_tabla), None)

        # El 'valor' de la respuesta tendra el nombre de la tabla
        # La 'lista' de la respuesta tendra todo el contenido que tiene la tabla
        return Respuesta(True, nombre_tabla, datos[nombre_tabla])

    def obtener_fila_de_auxiliar(self, datos: list, resultado: list) -> list:

        for indice, tupla in enumerate(datos):

            if indice < len(resultado['data']):
                resultado['data'][indice].append(tupla['auxiliar']['valor'])
            else:
                resultado['data'].append([tupla['auxiliar']['valor']])

    def obtener_fila_de_auxiliar_funcion_nativa(self, datos: list, resultado: list) -> list:

        for indice, tupla in enumerate(datos):

            if indice < len(resultado['data']):
                resultado['data'][indice].append(tupla['auxiliar'])
            else:
                resultado['data'].append([tupla['auxiliar']])

    def obtener_fila_de_identificador(self, datos_condiciones: list, nombre_tabla: str, nombre_columna: str, resultado: list):

        for indice, tupla in enumerate(datos_condiciones):

            llave = "{}.{}".format(nombre_tabla, nombre_columna)
            if llave in tupla:

                if indice < len(resultado['data']):
                    resultado['data'][indice].append(tupla[llave]['valor'])
                else:
                    resultado['data'].append([tupla[llave]['valor']])
            else:

                if indice < len(resultado['data']):
                    resultado['data'][indice].append(None)
                else:
                    resultado['data'].append([None])

    def obtener_informacion_completa(self, datos_condiciones: list):

        respuesta = { "encabezado": [], "data": []}

        for tupla in datos_condiciones:

            fila = []
            encabezado = []

            for llave, valor in tupla.items():

                if "@index" not in llave:
                    encabezado.append(llave)
                    fila.append(valor['valor'])

            respuesta['data'].append(fila)
            respuesta['encabezado'] = encabezado

        return respuesta

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

    def validar_indices(self, nombre_bd: str, nombre_tabla: str, listado_indices: list) -> Respuesta:

        # Se obtienen todos los registros de los indices debido a que es necesario revisar si no esta siendo utilizado en otro lugar algun registro por medio de llave foranea
        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"

        # Se obtiene la raiz del XML
        tree = ET.parse(path_tabla)
        root_tabla_actual = tree.getroot()

        registros = []
        for indice in listado_indices:
            fila = root_tabla_actual.find(f".//fila[@index='{indice}']")
            registros.append(fila)

        # Se obtienen todas las tablas existentes de la base de datos
        tablas = os.listdir(self.__path_tablas.format(nombre_bd))

        # Se evalua tabla por tabla para verificar
        for tabla in tablas:

            nombre_tabla_evaluar = tabla.rsplit('.', 1)[0]
            if  nombre_tabla_evaluar == nombre_tabla:
                continue

            # Se obtiene la raiz del XML de la tabla
            tree = ET.parse(self.__path_tablas.format(nombre_bd) + tabla)
            root_a_evaluar = tree.getroot()

            # Se obtiene los campos de la tabla a verificar que son una llave foranea
            campos_con_llave_foranea = root_a_evaluar.findall(".//estructura/campo/[@fk_table]")

            # Se verifica que no se elimine un registro que esta siendo utilizado en otra tabla
            for campo in campos_con_llave_foranea:

                if campo.attrib['fk_table'] == nombre_tabla:

                    for obj in registros:

                        fila = obj.find(campo.attrib['fk_attribute'])
                        if fila is not None:

                            resultado = root_a_evaluar.find(".//fila[{}='{}']".format(campo.attrib['name'], fila.text))
                            if resultado is not None:
                                return Respuesta(False, "No se puede realizar la operación 'DELETE' en la tabla '{}' debido a que el campo '{}' con valor '{}' esta siendo referenciado en la tabla '{}' a través de una llave foranea.".format(nombre_tabla, campo.attrib['fk_attribute'], fila.text, nombre_tabla_evaluar))

        return Respuesta(True, "")
