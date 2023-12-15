from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador 
class Drop(Instruccion):
    def __init__(self, id_nodo: int, tipo: str, identificador: Identificador):
        #accion: DATABASE | TABLE | PROCEDURE | FUNCTION
        self.id_nodo = id_nodo
        self.tipo = tipo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
       print("Drop")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP")
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        constr_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, self.tipo)
        return label_encabezado + constr_identificador + constr_tipo