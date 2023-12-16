import os
from dotenv import load_dotenv
from .util import Respuesta

load_dotenv()

class Administracion:

    def __init__(self):
        self.__path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS")) + "{}"

    ##############################################
    ################# SECCION USE ################
    ##############################################

    def verificar_existencia_bd(self, nombre_bd: str):
        '''
        Verifica que exista una base de datos

        Parameters:
            nombre_bd (str): Nombre de la base de datos

        Returns:
            Respuesta
        '''

        if not nombre_bd:
            return Respuesta(False, "Por favor, indique el nombre de la base de datos")

        if not os.path.exists(self.__path_bds.format(nombre_bd)):
            return Respuesta(False, "La base de datos '{}' que quiere utilizar no existe.".format(nombre_bd))
        else:
            return Respuesta(True, "Base de datos cambiada a: '{}'".format(nombre_bd))
