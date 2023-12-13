from ..abstract.instrucciones import Instruccion

class Update(Instruccion):
    def __init__(self):
        pass

    def Ejecutar(self, base_datos, entorno):
        print("Update")