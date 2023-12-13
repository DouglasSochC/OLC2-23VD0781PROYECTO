from ..abstract.instrucciones import Instruccion

class Alter(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Alter")