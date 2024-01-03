from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.campo_table import Campo_Table
from ..expresiones.parametro import Parametro
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from Funcionalidad.ddl import DDL

class Create(Instruccion):

    def __init__(self,  instruccion: str, identificador: Identificador, campos_table: list[Campo_Table], parametros: list[Parametro], instrucciones: list, retorno: Tipo_Dato):
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
                simbolo_procedure = Simbolo(nombre, -1, TIPO_DATO.PROCEDURE, -1, TIPO_ENTORNO.SENTENCIA_SSL)
                entorno.agregar(simbolo_procedure)
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
                simbolo_funcion = Simbolo(nombre, -1, TIPO_DATO.FUNCTION, -1, TIPO_ENTORNO.SENTENCIA_SSL)
                entorno.agregar(simbolo_funcion)
                return RetornoCorrecto(respuesta.valor) if respuesta.success else RetornoError(respuesta.valor)

    #TODO: Falta implementar lo siguiente
        # Graficar un procedimiento
        # Graficar una funcion
    def GraficarArbol(self, id_nodo_padre: int, contador: list):
        contador[0] += 1
        id_nodo_alias = hash("CREATE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_alias, "CREATE")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_alias)
        result = label_encabezado + union

        result+= self.identificador.GraficarArbol(id_nodo_alias, contador)

        if self.campos_table is not None:
            for campo in self.campos_table:
                result+= campo.GraficarArbol(id_nodo_alias, contador)

        if self.parametros is not None:
            for parametro in self.parametros:
                result+= parametro.GraficarArbol(id_nodo_alias, contador)

        if self.instrucciones is not None:
            for instr in self.instrucciones:
                result+= instr.GraficarArbol(id_nodo_alias, contador)

        if self.retorno is not None:
            result+= self.retorno.GraficarArbol(id_nodo_alias, contador)

        return result
