from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.retorno import TIPO_DATO, TIPO_TOKEN

class Select(Instruccion):
    def __init__(self, linea: int, columna: int, identificador: str, lista_expresiones: list):
        pass
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones

    def Ejecutar(self, base_datos, entorno):

        simbolo = Simbolo(1, None, TIPO_TOKEN.SELECT, self.identificador, None)
        entorno.agregar(simbolo)

        for expr in self.lista_expresiones:
            res = expr.Ejecutar(entorno)
            print(res)
