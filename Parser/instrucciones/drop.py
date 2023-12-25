from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..abstract.retorno import RetornoError, RetornoCorrecto
from Funcionalidad.ddl import DDL

class Drop(Instruccion):

    def __init__(self, id_nodo: str, tipo_eliminacion: str, identificador: Identificador):
        self.id_nodo = id_nodo
        self.tipo_eliminacion = tipo_eliminacion
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
        pass
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "C", self.tipo_eliminacion)
        union_tipo_encabezado = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "C")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_tipo + union_tipo_encabezado + label_identificador