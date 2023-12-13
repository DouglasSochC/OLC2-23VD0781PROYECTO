from ..abstract.instrucciones import Instruccion

class Update(Instruccion):
    def __init__(self, linea, columna):
        super().__init__(linea, columna)

    def Ejecutar(self, environment):
        print("Update")