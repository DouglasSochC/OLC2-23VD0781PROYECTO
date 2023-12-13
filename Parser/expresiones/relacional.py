from ..abstract.expresiones import Expresion

class Relacional(Expresion):
    def __init__(self, identificador: str, tipo_relacional:int, valor: list):
        self.identificador = identificador
        self.tipo_relacional = tipo_relacional
        self.valor = valor

    def Ejecutar(self, base_datos, entorno):

        print(entorno.obtener(1).valor)
        if self.tipo_relacional == '==':
            print("IGUAL IGUAL")
        print("RELACIONAL")
