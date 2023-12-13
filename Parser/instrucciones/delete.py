from ..abstract.instrucciones import Instruccion

class Delete(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, base_datos, entorno):
        print("Delete")