from ..abstract.expresiones import Expresion

class Tipo_Dato(Expresion):
    def __init__(self, linea, columna, tipo_dato, dimension):
        pass
        self.tipo_dato = tipo_dato
        self.dimension = dimension

    def Ejecutar(self, environment):
        print("Tipo_Dato")