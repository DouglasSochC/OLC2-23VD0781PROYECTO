from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, RetornoArreglo, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.expresion import Expresion
from ..expresiones.condicion import Condicion
from Funcionalidad.dml import DML

class Select(Instruccion):

    def __init__(self, lista_tablas: list[Expresion], lista_campos: list[Expresion], condicion: Condicion):
        self.lista_tablas = lista_tablas
        self.lista_campos = lista_campos
        self.condicion = condicion

    # TODO: Falta implementar lo siguiente
        # Implementar el que se puedan obtener muchas tablas
        # Implementar BETWEEN
        # Implementar las siguientes funciones nativas CONTAR, SUMA, CAS
    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar el comando 'SELECT', es necesario seleccionar una base de datos."

        dml = DML()

        # Se obtienen el nombre de una tabla o los nombres de varias tablas
        informacion = {}
        for tabla in self.lista_tablas:

            res_tabla_ejecutar = tabla.Ejecutar(base_datos, entorno)

            if isinstance (res_tabla_ejecutar, RetornoError):
                return res_tabla_ejecutar
            elif isinstance(res_tabla_ejecutar, dict):
                # Se obtiene toda la informacion que esta en el XML de la tabla
                obtener_tabla = dml.obtener_datos_tabla(base_datos.valor, res_tabla_ejecutar['identificador'])
                if obtener_tabla.success:
                    informacion[res_tabla_ejecutar['identificador']] = obtener_tabla.lista
                else:
                    return RetornoError(obtener_tabla.valor)
            else:
                return RetornoError("Ha ocurrido un error al obtener la informacion de la(s) tabla(s).")

        nuevo_entorno = TablaDeSimbolos(entorno)

        # Se almacena la informacion de cada tabla para poder acceder a ella desde el identificador
        simbolo = Simbolo('datos_tablas', informacion, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen todos los index's que cumplen con las condiciones dadas
        res_ejecutar_condicion = self.condicion.Ejecutar(base_datos, nuevo_entorno)
        if isinstance (res_ejecutar_condicion, RetornoError):
            return res_ejecutar_condicion

        return res_ejecutar_condicion.lista

    def GraficarArbol(self, id_padre):
        return ""
