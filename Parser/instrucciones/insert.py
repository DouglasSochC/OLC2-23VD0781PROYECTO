from ..abstract.instrucciones import Instruccion

class Insert(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Insert")