from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.retorno import TIPO_DATO, TIPO_TOKEN

class Select(Instruccion):
    def __init__(self, linea: int, columna: int, identificador: str, lista_expresiones: list):
        super().__init__(linea, columna)
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones

    def Ejecutar(self, environment):

        simbolo = Simbolo(1, None, TIPO_TOKEN.SELECT, self.identificador, None)
        environment.agregar(simbolo)

        for expr in self.lista_expresiones:
            res = expr.Ejecutar(environment)
            print(res)
