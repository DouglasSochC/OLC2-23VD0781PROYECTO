from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_Normal
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoArreglo, RetornoLiteral, TIPO_DATO

class Aritmetica(Expresion):

    def __init__(self,id_nodo, expresion_izquierda: Expresion_Normal, operador: str, expresion_derecha: Expresion_Normal):
        self.id_nodo = id_nodo
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

        if isinstance(exp_izq, RetornoCodigo) and isinstance(exp_der, RetornoCodigo):
            return RetornoCodigo("{} {} {}".format(exp_izq.codigo, self.operador, exp_der.codigo))

        if isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoArreglo):
            if self.operador == '*':
                print("ARREGLO-ARREGLO")
            elif self.operador == '/':
                print("ARREGLO-ARREGLO")
            elif self.operador == '+':
                print("ARREGLO-ARREGLO")
            elif self.operador == '-':
                print("ARREGLO-ARREGLO")
        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoLiteral):
            if self.operador == '*':
                print("ARREGLO-LITERAL")
            elif self.operador == '/':
                print("ARREGLO-LITERAL")
            elif self.operador == '+':
                print("ARREGLO-LITERAL")
            elif self.operador == '-':
                print("ARREGLO-LITERAL")
        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoArreglo):
            if self.operador == '*':
                print("LITERAL-ARREGLO")
            elif self.operador == '/':
                print("LITERAL-ARREGLO")
            elif self.operador == '+':
                print("LITERAL-ARREGLO")
            elif self.operador == '-':
                print("LITERAL-ARREGLO")
        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

            representacion_izquierda = exp_izq.valor if exp_izq.identificador is None else exp_izq.identificador
            representacion_derecha = exp_der.valor if exp_der.identificador is None else exp_der.identificador
            dominante = None

            if self.operador == '*':
                dominante = self.DominanteMultiplicacion(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '/':
                dominante = self.DominanteDivision(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '+':
                dominante = self.DominanteSuma(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '-':
                dominante = self.DominanteResta(exp_izq.tipado, exp_der.tipado)

            if dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(representacion_izquierda, self.operador, representacion_derecha))

            return RetornoLiteral(eval(f"exp_izq.valor {self.operador} exp_der.valor"), dominante, None)

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq.identificador, self.operador, exp_der['identificador']))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, RetornoArreglo):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der.identificador))
        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq.valor, self.operador, exp_der['identificador']))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, RetornoLiteral):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der.valor))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der['identificador']))

        return RetornoError("Ha ocurrido un error al realizar la operación aritmetica ({}).".format(self.operador))

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "ARITMETICA")

        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)

        resultado_izquierda = self.expresion_izquierda.GraficarArbol(self.id_nodo)
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "Op", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "Op")
        resultado_derecha = self.expresion_derecha.GraficarArbol(self.id_nodo)

        return label_encabezado + union_hijo_izquierdo  + resultado_izquierda + label_operador +union_enca_operador +resultado_derecha + union_hijo_derecho