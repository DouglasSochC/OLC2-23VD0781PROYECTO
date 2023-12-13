from ..abstract.instrucciones import Instruccion

class If(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, base_datos, entorno):
        print("If")