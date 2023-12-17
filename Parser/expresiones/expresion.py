from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.literal import Literal

class Expresion(Expresion):

    def __init__(self, id_nodo, expresion: Identificador | Literal):
        self.id_nodo = id_nodo
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        return res_ejecutar

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXPRESION")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
        return label_encabezado + union_hijo_izquierdo + resultado_izquierda