from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, RetornoArreglo, RetornoLiteral, RetornoCorrecto, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.expresion import Expresion
from ..expresiones.condicion import Condicion
from Funcionalidad.dml import DML

class Select(Instruccion):

    def __init__(self, lista_tablas: list[Expresion], lista_campos: list[Expresion], condicion: Condicion):
        self.lista_tablas = lista_tablas
        self.lista_campos = lista_campos
        self.condicion = condicion

    # TODO: Falta implementar lo siguiente
        # Implementar BETWEEN
        # Implementar las siguientes funciones nativas: CONTAR, SUMA, CAS
    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando el comando 'SELECT' dentro de la creacion de una funcion
        construir_funcion = entorno.obtener("construir_funcion")
        if construir_funcion is not None:
            return RetornoError("No es posible realizar una instrucción 'SELECT' dentro del cuerpo del FUNCTION.")

        # Se verifica si el comando 'SELECT' esta siendo utilizado en la creacion de un procedimiento
        construir_procedimiento = entorno.obtener("construir_procedimiento")
        if construir_procedimiento is not None:

            # Cada vez que se construye un nuevo procedimiento hay que verificar que se haya seleccionado una base de datos
            if base_datos.valor == "":
                return RetornoError("Para ejecutar el comando 'SELECT', es necesario seleccionar una base de datos.")

            if self.lista_tablas is None and self.condicion is None:

                expresiones_codigo = []
                for expresion in self.lista_campos:

                    if expresion is not None:
                        res_ejecutar = expresion.Ejecutar(base_datos, entorno)
                        if isinstance(res_ejecutar, RetornoCodigo):
                            expresiones_codigo.append(res_ejecutar.codigo)
                        else:
                            return RetornoError("Se produjo un error al intentar definir la instrucción 'SELECT' dentro de la creación del PROCEDURE.")

                return RetornoCodigo("SELECT {};\n".format(", ".join(expresiones_codigo)))

            else:

                listado_campos = []
                for campo in self.lista_campos:

                    if isinstance(campo, str) and campo == '*':
                        listado_campos.append(campo)
                        continue

                    res_campo_ejecutar = campo.Ejecutar(base_datos, entorno)

                    if isinstance (res_campo_ejecutar, RetornoCodigo):
                        listado_campos.append(res_campo_ejecutar.codigo)
                    else:
                        return RetornoError("Se produjo un error al intentar definir la instrucción 'SELECT' dentro de la creación del PROCEDURE.")

                listado_tablas = []
                for tabla in self.lista_tablas:

                    res_tabla_ejecutar = tabla.Ejecutar(base_datos, entorno)

                    if isinstance (res_tabla_ejecutar, RetornoCodigo):
                        listado_tablas.append(res_tabla_ejecutar.codigo)
                    else:
                        return RetornoError("Se produjo un error al intentar definir la instrucción 'SELECT' dentro de la creación del PROCEDURE.")

                if self.condicion is not None:

                        res_condicion_ejecutar = self.condicion.Ejecutar(base_datos, entorno)

                        if isinstance (res_condicion_ejecutar, RetornoCodigo):
                            return RetornoCodigo("SELECT {} FROM {} WHERE {};\n".format(", ".join(listado_campos), ", ".join(listado_tablas), res_condicion_ejecutar.codigo))
                        else:
                            return RetornoError("Se produjo un error al intentar definir la instrucción 'SELECT' dentro de la creación del PROCEDURE.")

                else:
                    return RetornoCodigo("SELECT {} FROM {};\n".format(", ".join(listado_campos), ", ".join(listado_tablas)))

        else:

            # En el caso que sea una expresion simple el cual no necesita tabla y tampoco base de datos para ser ejecutada
            if self.lista_tablas is None and self.condicion is None:

                for expresion in self.lista_campos:

                    if expresion is not None:
                        res_ejecutar = expresion.Ejecutar(base_datos, entorno)
                        if isinstance(res_ejecutar, RetornoError):
                            return res_ejecutar
                        elif isinstance(res_ejecutar, RetornoLiteral):
                            return RetornoCorrecto(res_ejecutar.valor)
                        else:
                            return RetornoError("Ha ocurrido un problema durante la ejecución del comando 'SELECT'")

            if base_datos.valor == "":
                return RetornoError("Para ejecutar el comando 'SELECT', es necesario seleccionar una base de datos.")

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

            # Se crea un nuevo entorno para almacenar la informacion de cada tabla y asi poder acceder a esas tablas desde el identificador cuando se este realizando la(s) condicion(es)
            nuevo_entorno = TablaDeSimbolos(entorno)
            simbolo = Simbolo('datos_tablas', informacion, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
            nuevo_entorno.agregar(simbolo)

            # Se obtienen todos los index's que cumplen con las condiciones dadas
            condiciones_obtenidas = []
            if len(informacion) > 1 and self.condicion is None:
                return RetornoError("Debido a que hay mas de una tabla por mostrar y no se ha dado una condicion especifica.")

            # Se obtienen todos los campos segun las condiciones dadas
            elif self.condicion is not None:
                res_ejecutar_condicion = self.condicion.Ejecutar(base_datos, nuevo_entorno)
                if isinstance (res_ejecutar_condicion, RetornoError):
                    return res_ejecutar_condicion
                condiciones_obtenidas = res_ejecutar_condicion.lista

            # Se obtienen todos los campos de la tabla indicada en el caso que no hayan condiciones
            elif len(informacion) == 1 and self.condicion is None:
                condiciones_obtenidas = informacion[list(informacion.keys())[0]]

            # Se crea un nuevo entorno para obtener la informacion de cada columna
            simbolo = Simbolo('select_de_datos', condiciones_obtenidas, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
            nuevo_entorno.agregar(simbolo)

            # Se obtienen los campos que se van a mostrar a traves de los datos obtenidos por medio de las condiciones dadas
            resultado = { "encabezado": [], "data": []}
            indice_encabezado = 0
            for campo in self.lista_campos:

                if campo == '*':
                    resultado = dml.obtener_informacion_completa(condiciones_obtenidas)
                    continue

                res_ejecutar_campo = campo.Ejecutar(base_datos, nuevo_entorno)
                if isinstance (res_ejecutar_campo, RetornoError):
                    return res_ejecutar_campo
                elif isinstance(res_ejecutar_campo, RetornoArreglo):

                    # Se define el encabezado de la fila
                    if res_ejecutar_campo.alias is None and res_ejecutar_campo.identificador is None:
                        resultado["encabezado"].append("encabezado{}".format(indice_encabezado))
                    elif res_ejecutar_campo.alias is not None:
                        resultado["encabezado"].append(res_ejecutar_campo.alias)
                    else:
                        resultado["encabezado"].append(res_ejecutar_campo.identificador)

                    # Se formatea la informacion de la fila obtenida y se almacena en el resultado
                    if res_ejecutar_campo.identificador is None:
                        dml.obtener_fila_de_auxiliar(res_ejecutar_campo.lista, resultado)
                    elif res_ejecutar_campo.identificador is not None and res_ejecutar_campo.tabla_del_identificador is not None:
                        dml.obtener_fila_de_identificador(condiciones_obtenidas, res_ejecutar_campo.tabla_del_identificador, res_ejecutar_campo.identificador, resultado)
                    elif res_ejecutar_campo.identificador is not None and res_ejecutar_campo.tabla_del_identificador is None:
                        dml.obtener_fila_de_auxiliar_funcion_nativa(res_ejecutar_campo.lista, resultado)
                else:
                    RetornoError("Ha ocurrido un error al obtener la informacion de la(s) tabla(s).")

            return resultado

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_select = hash("SELECT" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_select, "SELECT")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_select)
        result = label_encabezado + union

        # Se crea el nodo de las tablas y se une con el nodo de select
        if self.lista_tablas is not None:
            for tabla in self.lista_tablas:
                result += tabla.GraficarArbol(id_nodo_select, contador)

        # Se crea el nodo de los campos y se une con el nodo de select
        if self.lista_campos is not None:
            if self.lista_campos[0] == '*':
                contador[0] += 1
                id_nodo_campos = hash("CAMPOS" + str(contador[0]))
                label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_campos, "*")
                union = "\"{}\"->\"{}\";\n".format(id_nodo_select, id_nodo_campos)
                result += label_encabezado + union
            else:
                for campo in self.lista_campos:
                    result += campo.GraficarArbol(id_nodo_select, contador)

        # Se crea el nodo de la condicion y se une con el nodo de select
        if self.condicion is not None:
            result += self.condicion.GraficarArbol(id_nodo_select, contador)

        return result
