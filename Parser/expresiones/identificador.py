from ..abstract.expresiones import Expresion

class Identificador(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Identificador")