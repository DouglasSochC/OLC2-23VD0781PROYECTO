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

        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXPRESION")
        resultado = label_encabezado

        for parametro in self.listaExp:
            label_parametro = parametro.GraficarArbol(self.id_nodo)
            union_parametro = "\"{}\"->\"{}\";\n".format(self.id_nodo, parametro.id_nodo)
            resultado += label_parametro + union_parametro

        return resultado