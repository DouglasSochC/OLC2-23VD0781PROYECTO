from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..abstract.retorno import RetornoError
from Funcionalidad.ddl import DDL

class Drop(Instruccion):

    def __init__(self, id_nodo, tipo_eliminacion: str, identificador: Identificador):
        self.id_nodo = id_nodo
        self.tipo_eliminacion = tipo_eliminacion
        self.identificador = identificador

    # TODO: Falta implementar lo siguiente
        # Eliminar un procedimiento
        # Eliminar una funcion
    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar el comando '{}', es necesario seleccionar una base de datos.".format("DROP")

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador, RetornoError):
            return res_identificador.msg
        nombre = res_identificador.identificador

        dll = DDL()
        respuesta = None
        if self.tipo_eliminacion == 'database':
            respuesta = dll.eliminar_base_de_datos(nombre)
            if nombre == base_datos.valor:
                base_datos.valor = ""
        elif self.tipo_eliminacion == 'table':
            respuesta = dll.eliminar_tabla(base_datos.valor, nombre)
        elif self.tipo_eliminacion == 'procedure':
            return "FALTA IMPLEMENTAR EL PROCEDURE"
        elif self.tipo_eliminacion == 'function':
            return "FALTA IMPLEMENTAR EL FUNCTION"

        if respuesta.success:
            return respuesta.valor
        else:
            return "ERROR: {}".format(respuesta.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "C", self.tipo_eliminacion)
        union_tipo_encabezado = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "C")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + label_tipo + union_tipo_encabezado + label_identificador