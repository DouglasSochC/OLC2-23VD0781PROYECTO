from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..abstract.retorno import RetornoError, RetornoCorrecto
from Funcionalidad.ddl import DDL

class Drop(Instruccion):

    def __init__(self, tipo_eliminacion: str, identificador: Identificador):
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

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_drop = hash("DROP" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_drop, "DROP")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_drop)
        result = label_encabezado + union

        # Se crea el nodo del tipo de eliminacion y se une con el nodo de drop
        contador[0] += 1
        id_nodo_tipo_eliminacion = hash("TIPO_ELIMINACION" + str(contador[0]))
        label_tipo_eliminacion = "\"{}\"[label=\"{}\"];\n".format(id_nodo_tipo_eliminacion, self.tipo_eliminacion)
        union_tipo_eliminacion = "\"{}\"->\"{}\";\n".format(id_nodo_drop, id_nodo_tipo_eliminacion)
        result += label_tipo_eliminacion + union_tipo_eliminacion

        # Se obtiene el cuerpo del nodo identificador
        result += self.identificador.GraficarArbol(id_nodo_drop, contador)

        return result
