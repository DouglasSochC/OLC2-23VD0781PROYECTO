from ..abstract.expresiones import Expresion

class Literal(Expresion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Literal")