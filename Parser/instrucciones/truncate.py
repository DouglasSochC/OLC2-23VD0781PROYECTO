from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from ..expresiones.identificador import Identificador
from Funcionalidad.ddl import DDL

class Truncate(Instruccion):

    def __init__(self, identificador: Identificador):
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

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_truncate = hash("TRUNCATE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_truncate, "TRUNCATE")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_truncate)
        result = label_encabezado + union

        # Se obtiene el cuerpo del nodo identificador
        result += self.identificador.GraficarArbol(id_nodo_truncate, contador)

        return result
