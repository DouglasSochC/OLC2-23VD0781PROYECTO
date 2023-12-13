from ..abstract.expresiones import Expresion

class Asignacion(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Asignacion")