from ..abstract.instrucciones import Instruccion

class Relacional(Instruccion):
    def __init__(self, identificador: str, tipo_relacional:int, valor: list):
        self.identificador = identificador
        self.tipo_relacional = tipo_relacional
        self.valor = valor

    def Ejecutar(self, environment):
        
        print(environment.obtener(1).valor)
        if self.tipo_relacional == '==':
            print("IGUAL IGUAL")
        print("RELACIONAL")
