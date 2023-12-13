from ..abstract.expresiones import Expresion

class Accion(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Accion")