from ..abstract.instrucciones import Instruccion

class Use(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Use")