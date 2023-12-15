from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoIdentificador

class Alias(Expresion):

    def __init__(self, id_nodo: int, expresion: any, alias: str):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.alias = alias

    def Ejecutar(self, base_datos, entorno):

        # En el caso que sea una instancia de 'RetornoError' se retorna el error encontrado
        if isinstance(self.expresion, RetornoError):
            return self.expresion

        res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        if isinstance(res_ejecutar, RetornoError):
            return res_ejecutar
        else:
            return RetornoIdentificador(res_ejecutar.identificador, res_ejecutar.tipado, res_ejecutar.lista, self.alias)

    def GraficarArbol(self, id_padre):
        pass