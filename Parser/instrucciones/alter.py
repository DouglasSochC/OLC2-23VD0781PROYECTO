from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from ..expresiones.identificador import Identificador
from ..expresiones.accion import Accion
from Funcionalidad.ddl import DDL

class Alter(Instruccion):

    def __init__(self, id_nodo,identificador: Identificador, accion: Accion):
        self.id_nodo = id_nodo
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

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ALTER")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        label_accion = self.accion.GraficarArbol(self.id_nodo)
        union_encabezado_accion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.accion.id_nodo)
        return label_encabezado + label_identificador + label_accion  + union_encabezado_accion
