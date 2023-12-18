from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO, RetornoTipoDato

class Tipo_Dato(Expresion):

    def __init__(self, id_nodo: int, tipo_dato: TIPO_DATO, dimension: int):
        self.id_nodo = id_nodo
        self.tipo_dato = tipo_dato
        self.dimension = dimension

    def Ejecutar(self, base_datos, entorno):
        tipo = RetornoTipoDato(self.tipo_dato, self.dimension)
        return tipo

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "TIPO_DATO")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", "INT")
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        union_padre = "\"{}\"->\"{}\";\n".format(id_padre, self.id_nodo)
        return label_encabezado + label_valor + union_hijo + union_padre