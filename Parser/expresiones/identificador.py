from ..abstract.expresiones import Expresion

class Identificador(Expresion):
    def __init__(self, id_nodo: int, identificador: any):
        self.id_nodo = id_nodo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
        print("Identificador")

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "IDENTIFICADOR")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.identificador)
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
        union_padre = "\"{}\"->\"{}\";\n".format(id_padre, self.id_nodo)
        return label_encabezado + label_valor + union_hijo + union_padre