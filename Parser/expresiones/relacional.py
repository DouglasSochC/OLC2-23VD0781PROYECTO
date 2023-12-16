from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError, RetornoRelacional

class Relacional(Expresion):

    def __init__(self, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):
            return RetornoRelacional(None, exp_izq.lista, self.operador, exp_der.lista)
        elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):
            return RetornoRelacional(None, exp_izq.lista, self.operador, exp_der.valor)
        elif isinstance(exp_izq, RetornoError):
            return exp_izq
        elif isinstance(exp_der, RetornoError):
            return exp_der
        else:
            return RetornoError("La operación relacional con '{}' es invalida".format(self.operador))
