from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoArreglo
from ..expresiones.expresion import Expresion as Expresion_E

class Condicion(Expresion):

    def __init__(self, id_nodo: str, expresion_izquierda: Expresion_E, tipo_operador: str, expresion_derecha: Expresion_E):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.tipo_operador = tipo_operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        if self.tipo_operador is None and self.expresion_derecha is None:
            res_exp_izq_ejecutar = self.expresion_izquierda.Ejecutar(base_datos, entorno)
            return res_exp_izq_ejecutar        
        else:
            print()

    def GraficarArbol(self, id_padre):
        return ""
