from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from ..expresiones.identificador import Identificador
from Funcionalidad.ddl import DDL

class Truncate(Instruccion):

    def __init__(self, id_nodo, identificador: Identificador):
        self.id_nodo = id_nodo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'TRUNCATE' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'TRUNCATE' dentro de la creacion de un PROCEDURE o FUNCTION")

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'TRUNCATE', es necesario seleccionar una base de datos.")

        # Se obtiene el nombre de la tabla
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        ddl = DDL()
        res_truncate = ddl.truncate_tabla(base_datos.valor, nombre_tabla)

        return RetornoCorrecto(res_truncate.valor) if res_truncate.success else RetornoError(res_truncate.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "TRUNCATE")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_identificador