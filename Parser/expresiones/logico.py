from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError, TIPO_DATO

class Logico(Expresion):
    def __init__(self, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoError):
            return exp_izq
        elif isinstance(exp_der, RetornoError):
            return exp_der

        if self.operador == "&&":
            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):
                for indice, diccionario in enumerate(exp_izq.lista):

                    diccionario['temporal'] = diccionario['temporal'] and exp_der.lista[indice]['temporal']

                return RetornoIdentificador(exp_izq.identificador, TIPO_DATO.BOOLEAN, exp_izq.lista)