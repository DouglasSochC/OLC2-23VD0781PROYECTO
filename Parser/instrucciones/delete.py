from ..abstract.instrucciones import Instruccion

class Delete(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Delete")