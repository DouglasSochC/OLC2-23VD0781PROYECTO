from abc import ABCMeta, abstractclassmethod
from ..tablas.tabla_simbolo import TablaDeSimbolos

class Instruccion(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractclassmethod
    def Ejecutar(self, base_datos, entorno: TablaDeSimbolos):
        pass

    @abstractclassmethod
    def GraficarArbol(self, id_padre):
        pass