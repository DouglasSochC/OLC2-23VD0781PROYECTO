from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError

class Select_Print(Instruccion):

    def __init__(self, lista_expresiones: list):
        self.lista_expresiones = lista_expresiones

    def Ejecutar(self, base_datos, entorno):

        for expresion in self.lista_expresiones:
            if(expresion is not None):
                res_ejecutar = expresion.Ejecutar(base_datos, entorno)
                if isinstance(res_ejecutar, RetornoError):
                    return res_ejecutar.msg
                else:
                    return res_ejecutar.valor

    def GraficarArbol(self, id_padre):
        return ""