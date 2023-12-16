from ..abstract.instrucciones import Instruccion
from Funcionalidad.ddl import DDL

class Drop(Instruccion):

    def __init__(self, tipo_eliminacion: any, identificador: any):
        self.tipo_eliminacion = tipo_eliminacion
        self.identificador = identificador

    # TODO: Falta implementar lo siguiente
        # Eliminar un procedimiento
        # Eliminar una funcion
    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("DROP")

        nombre = self.identificador.Ejecutar(base_datos, entorno).identificador

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
        return ""