from ..abstract.expresiones import Expresion

class Literal(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Literal")