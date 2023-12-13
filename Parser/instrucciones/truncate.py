from ..abstract.instrucciones import Instruccion

class Truncate(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Truncate")