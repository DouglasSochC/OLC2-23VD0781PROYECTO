from ..abstract.expresiones import Expresion

class Aritmetica(Expresion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Aritmetica")