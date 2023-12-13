from ..abstract.instrucciones import Instruccion

class Alter(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Alter")