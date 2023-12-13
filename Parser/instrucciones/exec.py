from ..abstract.instrucciones import Instruccion

class Exec(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, environment):
        print("Exec")