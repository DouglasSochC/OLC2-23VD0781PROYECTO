import os
import shutil
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from .util import Respuesta
import xmltodict

load_dotenv()

class DDL:

    def __init__(self):
        self.__path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"
        self.__path_tablas = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_TABLAS"))
        self.__path_funciones = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_FUNCIONES"))
        self.__path_procedimiento = self.__path_bds + os.path.join(self.__path_bds, os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

    ##############################################
    ############### SECCION CREATE ###############
    ##############################################

    def crear_base_de_datos(self, nombre_bd: str):
        '''
        Crea una base de datos nueva

        Parameters:
            nombre_bd (str): Nombre de la base de datos

        Returns:
            Respuesta
        '''

        if not nombre_bd:
            return Respuesta(False, "Por favor, indique el nombre de la base de datos")

        if not os.path.exists(self.__path_bds.format(nombre_bd)):
            os.makedirs(self.__path_bds.format(nombre_bd))
            os.makedirs(self.__path_tablas.format(nombre_bd))
            os.makedirs(self.__path_funciones.format(nombre_bd))
            os.makedirs(self.__path_procedimiento.format(nombre_bd))
            return Respuesta(True, "La base de datos '{}' ha sido creada correctamente.".format(nombre_bd))
        else:
            return Respuesta(False, "Ya existe una base de datos con el mismo nombre.")

    def crear_tabla(self, nombre_bd:str, nombre_tabla: str, parametros: list):
        '''
        Crea una tabla nueva

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla (str): Nombre de la tabla a crear
            parametros (list): Diccionario que debe llevar la siguiente estructura [{
                name: str (*),
                type: str (int | bit | decimal | date | datetime | nchar | nvarchar) (*),
                length: int (o),
                nullable (o),
                pk (o),
                fk_table: str (o),
                fk_attribute: str (o)
            }...{}]

        Returns:
            Respuesta
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")

        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"
        if os.path.exists(path_tabla): # Se valida que no exista la tabla
            return Respuesta(False, "Ya existe una tabla con el mismo nombre.")
        else:
            # Crea el elemento raiz con el nombre de la tabla
            root = ET.Element(nombre_tabla)

            # Crea el apartado de estructura de la tabla el cual contendra la descripcion de los campos con sus respectivas restricciones
            estructura = ET.SubElement(root, "estructura")

            # Crea el apartado de los registros de la tabla el cual contendra todos los datos de la tabla
            ET.SubElement(root, "registros")

            # Se agrega los campos que lleva la tabla
            for param in parametros:

                # Se castean todos los atributos a 'str' para que puedan ser almacenados
                atributos = {clave: str(valor) for clave, valor in param.items()}

                # Se almacena cada campo que tendra la tabla
                ET.SubElement(estructura, "campo", attrib=atributos)

            # Crea el arbol XML
            tree = ET.ElementTree(root)

            # Escribe el árbol XML en un archivo
            with open(path_tabla, "wb") as archivo:
                tree.write(archivo)

            return Respuesta(True, "La tabla '{}' ha sido creada correctamente".format(nombre_tabla))

    ##############################################
    ################ SECCION DROP ################
    ##############################################

    def eliminar_base_de_datos(self, nombre_bd: str):
        '''
        Elimina una base de datos existente

        Parameters:
            nombre_bd (str): Nombre de la base de datos a eliminar

        Returns:
            Respuesta
        '''

        # Se valida que se asigne un nombre a la base de datos
        if nombre_bd is None:
            return Respuesta(False, "Por favor, indique el nombre de la base de datos")

        # Se valida la existencia de la base de datos
        path_bd = self.__path_bds.format(nombre_bd)
        if not os.path.exists(path_bd):
            return Respuesta(False, "La base de datos que desea eliminar no existe.")
        else:
            shutil.rmtree(path_bd)
            return Respuesta(True, "La base de datos '{}' ha sido eliminada correctamente.".format(nombre_bd))

    def eliminar_tabla(self, nombre_bd: str, nombre_tabla:str):
        '''
        Elimina una tabla de una base de datos

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla (str): Nombre de la tabla a eliminar

        Returns:
            Respuesta
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla))

        # Se obtienen todas las tablas existentes de la base de datos
        tablas = os.listdir(self.__path_tablas.format(nombre_bd))

        # Se evalua tabla por tabla para verificar que la tabla que se desee eliminar no este referenciada a otra tabla
        for tabla in tablas:

            # Se obtiene la raiz del XML de la tabla
            tree = ET.parse(self.__path_tablas.format(nombre_bd) + tabla)
            root = tree.getroot()

            # Se obtiene los campos que son una llave foranea
            campos_con_llave_foranea = root.findall(".//estructura/campo/[@fk_table]")

            # Se valida que no se haga referencia
            for campo in campos_con_llave_foranea:
                if campo.attrib['fk_table'] == nombre_tabla:
                    return Respuesta(False, "No es posible eliminar la tabla '{}' porque está referenciada por el campo '{}' en la tabla '{}'.".format(nombre_tabla, campo.attrib['name'], tabla.rsplit('.', 1)[0]))

        os.remove(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml")
        return Respuesta(True, "La tabla '{}' ha sido eliminada correctamente.".format(nombre_tabla))

    ##############################################
    ############## SECCION TRUNCATE ##############
    ##############################################

    def truncate_tabla(self, nombre_bd: str, nombre_tabla_truncar:str):
        '''
        Elimina toda la informacion que posee una tabla de una base de datos

        Parameters:
            nombre_bd (str): Nombre de la base de datos
            nombre_tabla_truncar (str): Nombre de la tabla

        Returns:
            Respuesta
        '''

        if nombre_bd is None: # Se valida que haya seleccionado una base de datos
            return Respuesta(False, "No ha seleccionado una base de datos para realizar la transaccion")
        elif nombre_tabla_truncar is None:  # Se valida que este el nombre de la tabla
            return Respuesta(False, "Por favor, indique el nombre de la tabla")
        elif not os.path.exists(self.__path_bds.format(nombre_bd)): # Se valida que exista la base de datos
            return Respuesta(False, "No existe la base de datos seleccionada")
        elif not os.path.exists(self.__path_tablas.format(nombre_bd) + nombre_tabla_truncar + ".xml"): # Se valida que exista la tabla
            return Respuesta(False, "La tabla '{}' no se encuentra en la base de datos.".format(nombre_tabla_truncar))

        path_tabla = self.__path_tablas.format(nombre_bd) + nombre_tabla_truncar + ".xml"

        # Se obtienen todos los ID's que contiene la tabla
        with open(path_tabla, 'r') as archivo:
            contenido_xml = archivo.read()

        # Se formatea el XML a un diccionario para manejarlo de mejor forma
        registros = xmltodict.parse(contenido_xml)[nombre_tabla_truncar]['registros']['fila']
        if isinstance(registros, dict):
            registros = [registros]

        # Se obtienen todas las tablas existentes de la base de datos
        tablas = os.listdir(self.__path_tablas.format(nombre_bd))

        # Se evalua tabla por tabla para verificar que la informacion a eliminar no este enlazada a otra tabla a traves de una llave foranea
        for tabla in tablas:

            # Se obtiene el nombre de la tabla actual que se esta analizando
            tabla_actual = tabla.rsplit('.', 1)[0]
            if tabla_actual == nombre_tabla_truncar:
                continue

            # Se busca el campo que tenga como llave foranea la tabla donde se eliminara toda la informacion, en el caso que no lo tenga se sigue analizando la siguiente tabla
            tree = ET.parse(self.__path_tablas.format(nombre_bd) + tabla)
            root = tree.getroot()
            campo = root.find(".//estructura/campo[@fk_table='" + nombre_tabla_truncar + "']")
            if campo is None:
                continue

            for contenido in registros:
                es_utilizado = root.find(".//registros/fila[" + campo.get("name") + "='" + contenido[campo.get("fk_attribute")] + "']")
                if es_utilizado is not None:
                    return Respuesta(False, "No es posible truncar la tabla '{}' ya que contiene datos referenciados por la tabla '{}'.".format(nombre_tabla_truncar, tabla_actual))

        # Parsear el archivo XML
        tree = ET.parse(path_tabla)
        root = tree.getroot()

        # Encontrar el elemento <registros>
        registros_elemento = root.find('registros')

        # Verificar si el elemento <registros> existe
        if registros_elemento is not None:
            # Eliminar todo el contenido del elemento <registros>
            for fila_elemento in registros_elemento.findall('fila'):
                registros_elemento.remove(fila_elemento)

        # Guardar los cambios de nuevo en el archivo
        tree.write(path_tabla)

        # os.remove(self.__path_tablas.format(nombre_bd) + nombre_tabla + ".xml")
        return Respuesta(True, "La tabla '{}' ha sido truncada exitosamente.".format(nombre_tabla_truncar))

    ##############################################
    ########### SECCION VALIDACIONES #############
    ##############################################

    def verificar_referencia_llave_foranea(self, nombre_bd:str, tipo_dato: dict, nombre_tabla_referencia: str, campo_tabla_referencia: str):
        '''
        Verifica que la referencia a una llave foranea sea correcta.

        Parameters:
            nombre_bd (str): Nombre de la base de datos.
            tipo_dato (dict): Contiene la informacion del campo que estara en la tabla a crear. {
                'type' (str): Tipo de dato
                'length' (str) = Longitud del tipo de dato (Este parametro existe unicamente si se es nchar y nvarchar)
            }
            nombre_tabla_referencia (str): Nombre de la tabla a la que se hara la referencia
            campo_tabla_referencia (str): Campo que pertenece a la tabla que se hara la referencia

        Returns:
            Respuesta
        '''

        path_tabla_referencia = self.__path_tablas.format(nombre_bd) + nombre_tabla_referencia + ".xml"

        # Se verifica la existencia de la tabla en la base de datos
        if not os.path.exists(path_tabla_referencia):
            return Respuesta(False, 'No existe la tabla a la que intenta hacer referencia con la llave foránea.')

        # Se obtiene el archivo para seguir realizando las respectivas validaciones
        tree = ET.parse(path_tabla_referencia)
        root = tree.getroot()

        # Buscar la definicion de los campos de la tabla en la estructura
        campo = root.findall(".//estructura/campo/[@name='" + campo_tabla_referencia + "']")

        # Se verifica que exista el campo en la tabla a referenciar
        if len(campo) <= 0:
            return Respuesta(False, 'No existe el campo en la tabla referenciada')

        # Se verifica que tengan el mismo tipo de dato
        if campo[0].attrib['type'] != tipo_dato['type']:
            return Respuesta(False, 'Los tipos de datos no son iguales')

        # En el caso que sea nchar o nvarchar se verifica que tengan la misma longitud
        if tipo_dato['type'] in ('nchar', 'nvarchar') and campo[0].attrib['length'] != tipo_dato['length']:
            return Respuesta(False, 'Las longitudes no son iguales')

        return Respuesta(True, 'Correcto')
