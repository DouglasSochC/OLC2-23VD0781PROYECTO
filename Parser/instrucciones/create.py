from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.campo_table import Campo_Table
from ..expresiones.parametro import Parametro
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from Funcionalidad.ddl import DDL

class Create(Instruccion):

    def __init__(self, id_nodo: str, instruccion: str, identificador: Identificador, campos_table: list[Campo_Table], parametros: list[Parametro], instrucciones: list, retorno: Tipo_Dato):
        self.id_nodo = id_nodo
        self.instruccion = instruccion
        self.identificador = identificador
        self.campos_table = campos_table
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.retorno = retorno

    # TODO: Falta implementar lo siguiente
        # Crear una funcion
    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'CREATE' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'CREATE' dentro de la creacion de un PROCEDURE o FUNCTION")

        ddl = DDL()

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre = res_identificador['identificador']

        if self.instruccion == 'database':
            res = ddl.crear_base_de_datos(nombre)
            return RetornoCorrecto(res.valor) if res.success else RetornoError(res.valor)
        else:

            if base_datos.valor == "":
                return RetornoError("Para ejecutar el comando 'CREATE', es necesario seleccionar una base de datos.")

            if self.instruccion == 'table':

                campos = [] # En esta variable se almacenan todos los campos que se definiran al construir la tabla
                for campo in self.campos_table:

                    # Al realizar este ejecutar se pueden tener 2 instancias (RetornoError | dict)
                    res_ejecutar = campo.Ejecutar(base_datos, entorno)
                    campos.append(res_ejecutar)

                res = ddl.crear_tabla(base_datos.valor, nombre, campos)
                return RetornoCorrecto(res.valor) if res.success else RetornoError(res.valor)

            elif self.instruccion == 'procedure':

                # Se almacenan los parametros que utiliza el procedure
                lista_parametros = []
                for parametro in self.parametros:
                    res_param_ejecutar = parametro.Ejecutar(base_datos, entorno)
                    lista_parametros.append(res_param_ejecutar)

                # Se crea una tabla de simbolos que manejara una bandera para indicar que no debe de ejecutar el funcionamiento de las instruccion
                nuevo_entorno = TablaDeSimbolos(entorno)

                # Se agrega en la tabla de simbolos una variable que indica que se esta creando un procedure y no se esta analizando el funcionamiento del mismo
                simbolo_variable = Simbolo("construir_procedimiento", None, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DDL)
                nuevo_entorno.agregar(simbolo_variable)

                query = ""
                for instr in self.instrucciones:

                    # Al realizar este ejecutar se pueden tener 2 instancias (RetornoError | RetornoCodigo)
                    res_instr_ejecutar = instr.Ejecutar(base_datos, nuevo_entorno)
                    if isinstance(res_instr_ejecutar, RetornoError):
                        return res_instr_ejecutar
                    elif isinstance(res_instr_ejecutar, RetornoCodigo):
                        query += res_instr_ejecutar.codigo
                    else:
                        return RetornoError("Ha ocurrido un error al definir la(s) instruccion(es) dentro de la creacion del PROCEDURE")

                respuesta = ddl.crear_procedimiento(base_datos.valor, nombre, lista_parametros, query)
                return RetornoCorrecto(respuesta.valor) if respuesta.success else RetornoError(respuesta.valor)

            elif self.instruccion == 'function':

                # Se almacenan los parametros que utiliza el function
                lista_parametros = []
                for parametro in self.parametros:
                    res_param_ejecutar = parametro.Ejecutar(base_datos, entorno)
                    lista_parametros.append(res_param_ejecutar)

                # Se crea una tabla de simbolos que manejara una bandera para indicar que no debe de ejecutar el funcionamiento de las instruccion
                nuevo_entorno = TablaDeSimbolos(entorno)

                # Se agrega en la tabla de simbolos una variable que indica que se esta creando un function y no se esta analizando el funcionamiento del mismo
                simbolo_variable = Simbolo("construir_funcion", None, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DDL)
                nuevo_entorno.agregar(simbolo_variable)

                query = ""
                for instr in self.instrucciones:

                    # Al realizar este ejecutar se pueden tener 2 instancias (RetornoError | RetornoCodigo)
                    res_instr_ejecutar = instr.Ejecutar(base_datos, nuevo_entorno)
                    if isinstance(res_instr_ejecutar, RetornoError):
                        return res_instr_ejecutar
                    elif isinstance(res_instr_ejecutar, RetornoCodigo):
                        query += res_instr_ejecutar.codigo
                    else:
                        return RetornoError("Ha ocurrido un error al definir la(s) instruccion(es) dentro de la creacion del FUNCTION")

                respuesta = ddl.crear_funcion(base_datos.valor, nombre, lista_parametros, query)
                return RetornoCorrecto(respuesta.valor) if respuesta.success else RetornoError(respuesta.valor)

    #TODO: Falta implementar lo siguiente
        # Graficar un procedimiento
        # Graficar una funcion
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CREATE")
        label_instruccion = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "CR", self.instruccion)
        union_encabezado_instruccion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "CR")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_instruccion + union_encabezado_instruccion + label_identificador


        if isinstance(self.campos_table, list) and self.campos_table:
            primer_elemento = self.campos_table[0]
            if isinstance(primer_elemento, Campo_Table):
                 for campo in self.campos_table:
                    label_campo = campo.GraficarArbol(self.id_nodo)
                    union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, campo.id_nodo)
                    result += label_campo + union_tipo_accion_campo
            else:
                label_tipo_dato = self.campos_table.GraficarArbol(self.id_nodo)
                result += label_tipo_dato

        return result
