from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError, RetornoRelacional

class Relacional(Expresion):

    def __init__(self,id_nodo, expresion_izquierda: any, operador: str, expresion_derecha: any):
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
        if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):
            return RetornoRelacional(None, exp_izq.lista, self.operador, exp_der.lista)
        elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):
            return RetornoRelacional(None, exp_izq.lista, self.operador, exp_der.valor)
        else:
            return RetornoError("La operación relacional con '{}' es invalida".format(self.operador))

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "RELACIONAL")

        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)

        resultado_izquierda = self.expresion_izquierda.GraficarArbol(self.id_nodo)
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "Op", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "Op")
        resultado_derecha = self.expresion_derecha.GraficarArbol(self.id_nodo)

        return label_encabezado + union_hijo_izquierdo  + resultado_izquierda + label_operador +union_enca_operador +resultado_derecha + union_hijo_derecho