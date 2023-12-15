from ..abstract.expresiones import Expresion

class Logico(Expresion):
    def __init__(self, id_nodo ,expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):
        print("Logico")

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre

        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, self.operador)
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        if self.expresion_derecha is not None:
            union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)
            resultado_derecha = self.expresion_derecha.GraficarArbol(id_padre)
        else:
            union_hijo_derecho = ""
            resultado_derecha = ""

        resultado_izquierda = self.expresion_izquierda.GraficarArbol(id_padre)

        return label_operador + union_hijo_izquierdo + union_hijo_derecho + resultado_izquierda + resultado_derecha