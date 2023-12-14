from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError

class Relacional(Expresion):

    def __init__(self, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):
            return (exp_izq.identificador, self.operador, exp_der.identificador)
        elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):
            return (exp_izq.identificador, self.operador, exp_der.valor)
        else:
            return RetornoError("La operación relacional con '{}' es invalida".format(self.operador))
