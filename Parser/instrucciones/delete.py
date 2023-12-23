from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.identificador import Identificador
from ..expresiones.condicion import Condicion

from Funcionalidad.dml import DML

class Delete(Instruccion):

    def __init__(self, id_nodo, identificador: Identificador, condicion: Condicion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.condicion = condicion

    def Ejecutar(self, base_datos, entorno):
        pass
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DELETE")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_identificador
        label_lista_condiciones = ""

        if self.condicion is not None and isinstance(self.condicion, Condicion):
            print("ENTRO A CONDICION")
            label_condicion = self.condicion.GraficarArbol(self.id_nodo)
            union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.condicion.id_nodo)
            result += label_condicion + union_tipo_accion_campo
            
        return result