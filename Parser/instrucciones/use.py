from ..abstract.instrucciones import Instruccion

class Use(Instruccion):
    def __init__(self, identificador: any):
        self.identificador = identificador
        pass

    def Ejecutar(self, base_datos, entorno):
        base_datos.valor = "bd1"
    
    def GraficarArbol(self, id_padre):
        pass