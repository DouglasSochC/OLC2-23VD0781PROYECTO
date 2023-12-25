from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.campo_table import Campo_Table
from ..expresiones.parametro import Parametro
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from Funcionalidad.ddl import DDL

class Create(Instruccion):

    def __init__(self, id_nodo: str, instruccion: str, identificador: Identificador, campos_table: list[Campo_Table], parametros: list[Parametro], instrucciones: list, retorno: Tipo_Dato):
        self.id_nodo = id_nodo
        self.instruccion = instruccion
        self.identificador = identificador
        self.campos_table = campos_table
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.retorno = retorno

    # TODO: Falta implementar lo siguiente
        # Crear una funcion
    def Ejecutar(self, base_datos, entorno):
        pass

    #TODO: Falta implementar lo siguiente
        # Graficar un procedimiento
        # Graficar una funcion
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CREATE")
        label_instruccion = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "CR", self.instruccion)
        union_encabezado_instruccion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "CR")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_instruccion + union_encabezado_instruccion + label_identificador


        if isinstance(self.campos_table, list) and self.campos_table:
            primer_elemento = self.campos_table[0]
            if isinstance(primer_elemento, Campo_Table):
                 for campo in self.campos_table:
                    label_campo = campo.GraficarArbol(self.id_nodo)
                    union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, campo.id_nodo)
                    result += label_campo + union_tipo_accion_campo
            else:
                label_tipo_dato = self.campos_table.GraficarArbol(self.id_nodo)
                result += label_tipo_dato

        return result
