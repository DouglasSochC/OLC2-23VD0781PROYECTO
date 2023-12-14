from ..abstract.expresiones import Expresion

class Identificador(Expresion):
    def __init__(self, id_nodo: int, valor: any, nombre_tabla: any = None, alias: any = None):
        self.id_nodo = id_nodo
        self.valor = valor
        self.nombre_tabla = nombre_tabla
        self.alias = alias

    def Ejecutar(self, base_datos, entorno):
        return self.valor

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "IDENTIFICADOR")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.valor)
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
        union_padre = "\"{}\"->\"{}\";\n".format(id_padre, self.id_nodo)
        return label_encabezado + label_valor + union_hijo + union_padre