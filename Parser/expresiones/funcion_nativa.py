from ..abstract.expresiones import Expresion

class Funcion_Nativa(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, base_datos, entorno):
        print("Funcion_Nativa")