from ..abstract.expresiones import Expresion

class Identificador(Expresion):

    def __init__(self, id_nodo: str, valor: str, referencia_tabla: str = None):
        self.id_nodo = id_nodo
        self.valor = valor
        self.referencia_tabla = referencia_tabla

    def Ejecutar(self, base_datos, entorno):

        return {'identificador': self.valor, 'referencia_tabla': self.referencia_tabla}

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "IDENTIFICADOR")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.valor)
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
        union_padre = "\"{}\"->\"{}\";\n".format(id_padre, self.id_nodo)
        return label_encabezado + label_valor + union_hijo + union_padre