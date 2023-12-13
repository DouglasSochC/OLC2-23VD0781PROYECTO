from ..abstract.instrucciones import Instruccion

class Declare(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Declare")