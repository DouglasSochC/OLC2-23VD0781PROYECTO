from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoLiteral, RetornoArreglo, RetornoCodigo, TIPO_DATO
from Funcionalidad.dml import DML

class Asignacion(Expresion):

    def __init__(self, id_nodo, identificador: Identificador, expresion: Expresion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.expresion = expresion

    # Para comprender su funcionamiento se debe de tener en cuenta la siguiente estructura:
    # 'IDENTIFICADOR' = 'EXPRESION'
    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            # En el caso que ocurra un error al obtener la expresion
            res = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res, RetornoError):
                return res
            elif isinstance(res, RetornoCodigo):
                codigo_identificador = "{}.{}".format(res_identificador_ejecutar['referencia_tabla'], res_identificador_ejecutar['identificador']) if res_identificador_ejecutar['referencia_tabla'] != None else res_identificador_ejecutar['identificador']
                return RetornoCodigo("{} = {}".format(codigo_identificador, res.codigo))
            else:
                return RetornoError("Ha ocurrido un error al definir el codigo de la asignacion")

        else:

            # Se evalua si se esta utilizando la asignacion al hacer un WHERE
            simbolo_datos_tablas = entorno.obtener("datos_tablas")
            if simbolo_datos_tablas is None:

                res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
                if isinstance(res_expresion_ejecutar, RetornoError):
                    return res_expresion_ejecutar
                elif isinstance(res_expresion_ejecutar, RetornoLiteral):
                    return RetornoLiteral(res_expresion_ejecutar.valor, res_expresion_ejecutar.tipado, res_identificador_ejecutar['identificador'])
                else:
                    return RetornoError("La asignacion se debe de realizar unicamente con un literal.")
            else:

                # Se obtienen los datos que contiene el 'IDENTIFICADOR'
                dml = DML()
                datos_identificador = None
                # Se busca en la tabla de simbolos el nombre de la variable
                simbolo = entorno.obtener("condicion")

                if simbolo is None:
                    datos_identificador = dml.verificar_columna_tabla(base_datos.valor, simbolo_datos_tablas.valor, res_identificador_ejecutar['identificador'], res_identificador_ejecutar['referencia_tabla'], list(simbolo_datos_tablas.valor.keys()))
                    if datos_identificador.success is False:
                        return RetornoError(datos_identificador.valor)
                    datos_identificador = RetornoArreglo(res_identificador_ejecutar['identificador'], datos_identificador.valor, datos_identificador.lista)
                else:
                    datos_identificador = dml.verificar_columna_tabla(base_datos.valor, simbolo_datos_tablas.valor, res_identificador_ejecutar['identificador'], res_identificador_ejecutar['referencia_tabla'], list(simbolo_datos_tablas.valor.keys()))
                    if datos_identificador.success is False:
                        return RetornoError(datos_identificador.valor)
                    datos_identificador = RetornoArreglo(res_identificador_ejecutar['identificador'], datos_identificador.valor, simbolo.valor.lista)

                # Se obtienen los datos que contiene la 'EXPRESION'
                res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
                if isinstance(res_expresion_ejecutar, RetornoError):
                    return res_expresion_ejecutar

                # Si la expresion es un literal se verifica el cumplimiento de la condicion
                if isinstance(res_expresion_ejecutar, RetornoLiteral):

                    respuesta = []
                    for tupla in datos_identificador.lista:

                        llave_identificador = "{}.{}".format(datos_identificador.tabla_del_identificador, datos_identificador.identificador)
                        if llave_identificador not in tupla:
                            continue

                        valor_tupla = tupla[llave_identificador]
                        valor_tupla['tipado'] = self.expresion.DominanteAsignacion(valor_tupla['tipado'], res_expresion_ejecutar.tipado)
                        if valor_tupla['tipado'] == TIPO_DATO.NULL:
                            return RetornoError("No se puede realizar la operacion relacional '{} = {}' debido a que no poseen el mismo tipo de dato.".format(res_identificador_ejecutar['identificador'], ('"{}"'.format(res_expresion_ejecutar.valor) if res_expresion_ejecutar.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else res_expresion_ejecutar.valor)))

                        if tupla[llave_identificador]['valor'] == res_expresion_ejecutar.valor:
                            respuesta.append(tupla)

                    return RetornoArreglo(datos_identificador.tabla_del_identificador, datos_identificador.identificador, respuesta)

                # Si la expresion es un arreglo, entonces se empezara a homolar la informacion en un solo arreglo
                elif isinstance(res_expresion_ejecutar, RetornoArreglo):

                    # Se empieza a homologar la informacion en un solo arreglo
                    arreglo_identificador = datos_identificador
                    arreglo_expresion = res_expresion_ejecutar
                    respuesta = []

                    llave_identificador = "{}.{}".format(arreglo_identificador.tabla_del_identificador, arreglo_identificador.identificador)
                    for tupla_identificador in arreglo_identificador.lista:

                        # Se verifica que exista la llave dentro de la tupla del identificador
                        if llave_identificador not in tupla_identificador:
                            continue

                        llave_expresion = "{}.{}".format(arreglo_expresion.tabla_del_identificador, arreglo_expresion.identificador) if arreglo_expresion.identificador is not None else "auxiliar"
                        for tupla_expresion in arreglo_expresion.lista:

                            # Se verifca que exista la llave dentro de la tupla de la expresion
                            if llave_expresion not in tupla_expresion:
                                continue

                            # Se verifica si el valor es None para no realizar la operacion
                            if tupla_expresion[llave_expresion]['valor'] is None:
                                continue

                            # Se verifica que el tipo de dato sea el mismo
                            if tupla_identificador[llave_identificador]['tipado'] != tupla_expresion[llave_expresion]['tipado']:
                                return RetornoError("No se puede realizar la operacion relacional '{} = {}' debido a que no poseen el mismo tipo de dato.".format(res_identificador_ejecutar['identificador'], arreglo_expresion.identificador))

                            if tupla_identificador[llave_identificador]['valor'] == tupla_expresion[llave_expresion]['valor']:
                                tupla_homologacion = {}
                                tupla_homologacion.update(tupla_identificador)
                                tupla_homologacion.update(tupla_expresion)
                                respuesta.append(tupla_homologacion)

                    return RetornoArreglo(None, None, respuesta)

                else:
                    return RetornoError("Ha ocurrido un error al realizar la condición (=).")

    # TODO: Corregir el graficado del arbol debido a que se han modificado los parametros que se solicitan en la asignacion
    def GraficarArbol(self, id_padre):

        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ASIGNACION")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)

        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "op", "=")
        union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "op")
        resultado_exp = ""

        if isinstance(self.expresion, list):
            print("es lista")
            for exp in self.expresion:
                union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
                resultado_izquierda = exp.GraficarArbol(self.id_nodo)
                resultado_exp += union_hijo_izquierdo + resultado_izquierda
        else:
            union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
            resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
            resultado_exp += union_hijo_izquierdo + resultado_izquierda

        return label_encabezado+ label_identificador +label_operador + union_enca_operador+ resultado_exp
