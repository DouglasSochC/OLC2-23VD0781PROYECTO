from ..abstract.instrucciones import Instruccion

class Drop(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Drop")