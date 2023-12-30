from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from ..expresiones.identificador import Identificador
from ..expresiones.accion import Accion
from Funcionalidad.ddl import DDL

class Alter(Instruccion):

    def __init__(self, identificador: Identificador, accion: Accion):
        self.identificador = identificador
        self.accion = accion

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'ALTER' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'ALTER' dentro de la creacion de un PROCEDURE o FUNCTION")

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'ALTER', es necesario seleccionar una base de datos.")

        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        res_accion = self.accion.Ejecutar(base_datos, entorno)
        if isinstance(res_accion, RetornoError):
            return res_accion

        ddl = DDL()

        # Si la accion devuelve un string quiere decir que se esta eliminando una columna
        if isinstance(res_accion, str):
            res_alter_drop = ddl.alter_drop_columna(base_datos.valor, nombre_tabla, res_accion)
            return RetornoCorrecto(res_alter_drop.valor) if res_alter_drop.success else RetornoError(res_alter_drop.valor)
        # Si la accion devuelve una lista quiere decir que se esta agregando nuevas columnas a la tabla
        elif isinstance(res_accion, list):
            res_alter_add = ddl.alter_add_campos(base_datos.valor, nombre_tabla, res_accion)
            return RetornoCorrecto(res_alter_add.valor) if res_alter_add.success else RetornoError(res_alter_add.valor)
        else:
            return RetornoError("Ha ocurrido un error al realizar la instruccion 'ALTER'")

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_alter = hash("ALTER" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_alter, "ALTER")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_alter)
        result = label_encabezado + union

        # Se obtienen los nodos hijos que son el identificador y la accion
        result += self.identificador.GraficarArbol(id_nodo_alter, contador)
        result += self.accion.GraficarArbol(id_nodo_alter, contador)

        return result
