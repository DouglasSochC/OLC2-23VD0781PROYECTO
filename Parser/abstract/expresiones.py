from abc import ABCMeta, abstractclassmethod
from ..tablas.tabla_tipos import TablaSuma, TablaResta, TablaMultiplicacion, TablaDivision

class Expresion(metaclass=ABCMeta):
    
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna
    
    @abstractclassmethod
    def Ejecutar(self):
        pass

    def DominanteSuma(self, tipo1, tipo2):
        tipado = TablaSuma[tipo1.value[0]][tipo2.value[0]]
        return tipado

    def DominanteResta(self, tipo1, tipo2):
        tipado = TablaResta[tipo1.value[0]][tipo2.value[0]]
        return tipado

    def DominanteMultiplicacion(self, tipo1, tipo2):
        tipado = TablaMultiplicacion[tipo1.value[0]][tipo2.value[0]]
        return tipado

    def DominanteDivision(self, tipo1, tipo2):
        tipado = TablaDivision[tipo1.value[0]][tipo2.value[0]]
        return tipado
