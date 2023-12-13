from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import TIPO_DATO
from ..expresiones.identificador import Identificador

class Declare(Instruccion):

    def __init__(self, id_nodo: int, identificador: Identificador, tipo_dato: TIPO_DATO):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.tipo_dato = tipo_dato

    def Ejecutar(self, base_datos, entorno):

        tipo_dato = self.tipo_dato.Ejecutar(base_datos, entorno)

        if tipo_dato['tipo_dato'] == TIPO_DATO.INT:
            print("Declare")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DECLARE")
        constr_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador + constr_tipo_dato