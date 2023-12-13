from ..abstract.expresiones import Expresion

class Funcion_Nativa(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Funcion_Nativa")