from abc import ABCMeta, abstractclassmethod

class Instruccion(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractclassmethod
    def Ejecutar(self, environment):
        pass
