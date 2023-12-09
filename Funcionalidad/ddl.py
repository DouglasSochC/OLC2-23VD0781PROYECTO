import os
import shutil
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from .util import Respuesta

load_dotenv()

class DDL:

    def __init__(self):
        self.path_bd = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"
        self.path_tablas = self.path_bd + os.path.join(self.path_bd, os.environ.get("CARPETA_PARA_TABLAS"))
        self.path_funciones = self.path_bd + os.path.join(self.path_bd, os.environ.get("CARPETA_PARA_FUNCIONES"))
        self.path_procedimiento = self.path_bd + os.path.join(self.path_bd, os.environ.get("CARPETA_PARA_PROCEDIMIENTOS"))

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

        if not os.path.exists(self.path_bd.format(nombre_bd)):
            os.makedirs(self.path_bd.format(nombre_bd))
            os.makedirs(self.path_tablas.format(nombre_bd))
            os.makedirs(self.path_funciones.format(nombre_bd))
            os.makedirs(self.path_procedimiento.format(nombre_bd))
            return Respuesta(True, "La base de datos ha sido creada correctamente.")
        else:
            return Respuesta(False, "Ya existe una base de datos con el mismo nombre.")

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
        path_bd = self.path_bd.format(nombre_bd)
        if not os.path.exists(path_bd):
            return Respuesta(False, "La base de datos que desea eliminar no existe.")
        else:
            shutil.rmtree(path_bd)
            return Respuesta(True, "La base de datos ha sido eliminada correctamente.")