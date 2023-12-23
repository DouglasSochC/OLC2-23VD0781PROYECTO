from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, RetornoCorrecto, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.identificador import Identificador
from ..expresiones.condicion import Condicion
from Funcionalidad.dml import DML

class Delete(Instruccion):

    def __init__(self, id_nodo, identificador: Identificador, condicion: Condicion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.condicion = condicion

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return RetornoError("Para ejecutar la consulta 'DELETE', es necesario seleccionar una base de datos.")

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        # Se inicializa la clase que sera utilizada para realizar el proceso del delete
        dml = DML()

        # Se obtiene toda la informacion de la tabla
        informacion = {}
        obtener_tabla = dml.obtener_datos_tabla(base_datos.valor, nombre_tabla)
        if obtener_tabla.success is False:
            return RetornoError(obtener_tabla.valor)
        informacion[nombre_tabla] = obtener_tabla.lista

        # Se crea un nuevo entorno para almacenar la informacion de la tabla asi poder acceder a ella desde el identificador cuando se este realizando la condicion
        nuevo_entorno = TablaDeSimbolos(entorno)
        simbolo = Simbolo('datos_tablas', informacion, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen todos los index's que cumplen con las condiciones dadas
        condiciones_obtenidas = []
        if self.condicion is not None:
            res_ejecutar_condicion = self.condicion.Ejecutar(base_datos, nuevo_entorno)
            if isinstance (res_ejecutar_condicion, RetornoError):
                return res_ejecutar_condicion
            condiciones_obtenidas = res_ejecutar_condicion.lista

        # Se obtienen todos los campos de la tabla indicada en el caso que no hayan condiciones
        elif len(informacion) == 1 and self.condicion is None:
            condiciones_obtenidas = informacion[list(informacion.keys())[0]]

        indices_a_eliminar = []
        for tupla in condiciones_obtenidas:
            indices_a_eliminar.append(tupla["{}.{}".format(nombre_tabla,'@index')])

        res_validar_indices = dml.validar_indices(base_datos.valor, nombre_tabla, indices_a_eliminar)
        if res_validar_indices.success is False:
            return RetornoError(res_validar_indices.valor)

        respuesta = dml.eliminar_filas(base_datos.valor, nombre_tabla, indices_a_eliminar)
        return RetornoCorrecto(respuesta.valor) if respuesta.success else RetornoError(respuesta.valor)

    def GraficarArbol(self, id_padre):
        return ""
        # label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DELETE")
        # label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        # result = label_encabezado + label_identificador
        # label_lista_condiciones = ""

        # if isinstance(self.lista_condiciones, list) and self.lista_condiciones:
        #     primer_elemento = self.lista_condiciones[0]
        #     if isinstance(primer_elemento, Expresion):
        #         for condicion in self.lista_condiciones:
        #             label_condicion = condicion.GraficarArbol(self.id_nodo)
        #             union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, condicion.id_nodo)
        #             result += label_condicion + union_tipo_accion_campo
        #     else:
        #         label_lista_condiciones = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "LC", self.lista_condiciones)
        #         union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "LC")
        #         result += label_lista_condiciones + union_tipo_accion_campo

        # return result