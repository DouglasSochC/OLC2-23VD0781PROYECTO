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

        # Se verifica que no se este utilizando este 'DROP' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'DROP' dentro de la creacion de un PROCEDURE o FUNCTION")

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'DROP', es necesario seleccionar una base de datos.")

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre = res_identificador['identificador']

        dll = DDL()
        respuesta = None
        if self.tipo_eliminacion == 'database':
            respuesta = dll.eliminar_base_de_datos(nombre)
            if nombre == base_datos.valor:
                base_datos.valor = ""
        elif self.tipo_eliminacion == 'table':
            respuesta = dll.eliminar_tabla(base_datos.valor, nombre)
        elif self.tipo_eliminacion == 'procedure':
            respuesta = dll.eliminar_procedimiento(base_datos.valor, nombre)
        elif self.tipo_eliminacion == 'function':
            respuesta = dll.eliminar_funcion(base_datos.valor, nombre)

        return RetornoCorrecto(respuesta.valor) if respuesta.success else RetornoError(respuesta.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "C", self.tipo_eliminacion)
        union_tipo_encabezado = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "C")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_tipo + union_tipo_encabezado + label_identificador