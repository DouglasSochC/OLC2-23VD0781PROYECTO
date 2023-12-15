from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import TIPO_DATO
from ..expresiones.identificador import Identificador 
class Drop(Instruccion):
    def __init__(self, id_nodo: int, accion:TIPO_DATO, tipo: str, identificador: Identificador):
        #accion: DATABASE | TABLE | PROCEDURE | FUNCTION
        self.id_nodo = id_nodo
        self.accion = accion
        self.tipo = tipo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
       print("Drop")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP_INST")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", self.accion)
        label_elemento = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "E", self.tipo)
        union_tipo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        union_elemento = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "E")
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_tipo + label_elemento + union_tipo +union_elemento   + constr_identificador