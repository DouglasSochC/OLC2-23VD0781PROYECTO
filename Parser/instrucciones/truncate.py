from ..abstract.instrucciones import Instruccion

class Truncate(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Truncate")