import os
import shutil
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from .util import Respuesta

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
            return Respuesta(True, "La base de datos ha sido creada correctamente.")
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

                # Se verificara que las llaves foraneas esten debidamente validadas
                ET.SubElement(estructura, "campo", attrib=param)

            # Crea el arbol XML
            tree = ET.ElementTree(root)

            # Escribe el árbol XML en un archivo
            with open(path_tabla, "wb") as archivo:
                tree.write(archivo)

            return Respuesta(True, "La tabla ha sido creada correctamente")

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
            return Respuesta(True, "La base de datos ha sido eliminada correctamente.")

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
            nombre_tabla_referencia (str): abc
            campo_tabla_referencia (str):

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
