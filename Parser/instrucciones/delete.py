from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, TIPO_TOKEN
from Funcionalidad.dml import DML

class Delete(Instruccion):

    def __init__(self, identificador: str, lista_condiciones: list):
        self.identificador = identificador
        self.lista_condiciones = lista_condiciones

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("DELETE")

        nuevo_entorno = TablaDeSimbolos({})

        # Se obtiene el nombre de la tabla
        nombre_tabla = self.identificador.Ejecutar(base_datos, nuevo_entorno).identificador

        # Se almacena la tabla para poder acceder a ella desde un identificador y asi poder obtener la informacion completa de la tabla
        simbolo = Simbolo('nombre_tabla', None, TIPO_TOKEN.DELETE, nombre_tabla, None)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen la lista de condiciones que se debe de aplicar al DELETE y se almacenan en la variable 'listado_condiciones'
        listado_condiciones = []
        if len(self.lista_condiciones) > 0:
            for condicion in self.lista_condiciones:

                res = condicion.Ejecutar(base_datos, nuevo_entorno)

                if isinstance (res, RetornoError):
                    return res.msg

                # Se obtienen los indices que cumplen con las condiciones
                listado_condiciones.append(res)
                listado_condiciones.append('AND')

            listado_condiciones.pop()

        dml = DML()
        indices_a_eliminar = dml.obtener_indices_segun_condiciones(base_datos.valor, nombre_tabla, listado_condiciones)
        respuesta = dml.eliminar_filas(base_datos.valor, nombre_tabla, indices_a_eliminar)

        if respuesta.success:
            return respuesta.valor
        else:
            return "ERROR: {}".format(respuesta.valor)

    def GraficarArbol(self, id_padre):
        return ""