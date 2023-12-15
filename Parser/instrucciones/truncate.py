from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import TIPO_DATO
from ..expresiones.identificador import Identificador

class Truncate(Instruccion):
    def __init__(self, id_nodo, tipo_dato: TIPO_DATO, objetivo: any, identificador: Identificador ):
        self.id_nodo = id_nodo
        self.tipo_dato = tipo_dato
        self.objetivo = objetivo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
        print("Truncate")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "TRUNCATE_INST")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", self.tipo_dato)
        label_elemento = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "E", self.objetivo)
        union_tipo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        union_elemento = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "E")
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_tipo + label_elemento + union_tipo +union_elemento   + constr_identificador