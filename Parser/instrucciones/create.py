from ..abstract.instrucciones import Instruccion
from Funcionalidad.ddl import DDL

class Create(Instruccion):
    def __init__(self, linea: int, columna: int, tipo_instruccion: str, identificador: str):
        pass
        self.identificador = identificador
        self.tipo_instruccion = tipo_instruccion

    def Ejecutar(self, environment):

        ddl = DDL()
        if self.tipo_instruccion == 'DATABASE':
            res = ddl.crear_base_de_datos(self.identificador)
            return res
