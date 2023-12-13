from abc import ABCMeta, abstractclassmethod

class Instruccion(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractclassmethod
    def Ejecutar(self, base_datos, entorno):
        pass

    @abstractclassmethod
    def GraficarArbol(self, id_padre):
        pass