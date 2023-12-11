from ..abstract.instrucciones import Instruccion

class Create(Instruccion):
    def __init__(self, linea: int, columna: int, tipo_instruccion: str, identificador: str):
        super().__init__(linea, columna)
        self.identificador = identificador
        self.tipo_instruccion = tipo_instruccion

    def Ejecutar(self, environment):
        print("Creando la base de datos")
