from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError

class Aritmetica(Expresion):
    def __init__(self, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)
        if self.operador == '*':

            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):

                if len(exp_izq.lista) == len(exp_der.lista):

                    for indice, diccionario in enumerate(exp_izq.lista):

                        diccionario['temporal'] = diccionario['temporal'] * exp_der.lista[indice]['temporal']

                    return RetornoIdentificador(exp_izq.identificador, exp_izq.lista)
                else:
                    return "No se puede realizar la operacion {} '*' {} debido a que no son tipos de datos similares".format(exp_izq.valor, exp_der.valor)

            elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):

                for diccionario in exp_izq.lista:
                    diccionario['temporal'] = diccionario['temporal'] * exp_der.valor

                return RetornoIdentificador(exp_izq.identificador, exp_izq.lista)

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoIdentificador):
                return RetornoError("No se puede realizar la operacion {} * {}".format(exp_izq.valor, exp_der.identificador))

        elif self.operador == '/':
            print("DIVISION ENTRE: ", exp_izq, exp_der)
        elif self.operador == '+':
            print("SUMA ENTRE: ", exp_izq, exp_der)
        elif self.operador == '-':
            print("RESTA ENTRE: ", exp_izq, exp_der)

        return (self.expresion_izquierda, self.operador, self.expresion_derecha)

    def GraficarArbol(self, id_padre):
        return ""