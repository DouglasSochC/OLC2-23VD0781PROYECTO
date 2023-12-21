from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoLiteral, RetornoArreglo, TIPO_DATO
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

        # Se evalua si se esta utilizando la asignacion al hacer un WHERE
        simbolo_datos_tablas = entorno.obtener("datos_tablas")
        if simbolo_datos_tablas is None:
            print("SE ESTA UTILIZANDO EN EL UPDATE!")
        else:

            # Se obtienen los datos que contiene el 'IDENTIFICADOR'
            dml = DML()
            datos_identificador = dml.verificar_columna_tabla(base_datos.valor, simbolo_datos_tablas.valor, res_identificador_ejecutar['identificador'], res_identificador_ejecutar['referencia_tabla'])
            if datos_identificador.success is False:
                return RetornoError(datos_identificador.valor)

            # Se obtienen los datos que contiene la 'EXPRESION'
            res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion_ejecutar, RetornoError):
                return res_expresion_ejecutar

            # Si la expresion es un literal se verifica el cumplimiento de la condicion
            if isinstance(res_expresion_ejecutar, RetornoLiteral):

                respuesta = []
                for tupla in datos_identificador.lista:

                    valor_tupla = tupla["{}.{}".format(res_identificador_ejecutar['referencia_tabla'], res_identificador_ejecutar['identificador'])]
                    if valor_tupla['tipado'] != res_expresion_ejecutar.tipado:
                        return RetornoError("No se puede realizar la operacion relacional '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(res_identificador_ejecutar['identificador'], "=", ('"{}"'.format(res_expresion_ejecutar.valor) if res_expresion_ejecutar.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else res_expresion_ejecutar.valor)))

                    if tupla["{}.{}".format(res_identificador_ejecutar['referencia_tabla'], res_identificador_ejecutar['identificador'])]['valor'] == res_expresion_ejecutar.valor:
                        respuesta.append(tupla)

                return RetornoArreglo(res_identificador_ejecutar['identificador'], res_identificador_ejecutar['referencia_tabla'], respuesta)

            # Si la expresion es un arreglo, entonces se empezara a homolar la informacion en un solo arreglo
            elif isinstance(res_expresion_ejecutar, RetornoArreglo):

                # Se empieza a homologar la informacion en un solo arreglo
                arreglo_identificador = datos_identificador
                arreglo_expresion = res_expresion_ejecutar
                arreglo_homologacion = []

                for tupla_identificador in arreglo_identificador.lista:

                    for tupla_expresion in arreglo_expresion.lista:

                        # Se verifica que el tipo de dato sea el mismo
                        if tupla_identificador["{}.{}".format(res_identificador_ejecutar['referencia_tabla'], res_identificador_ejecutar['identificador'])]['tipado'] != tupla_expresion["{}.{}".format(arreglo_expresion.tabla_del_identificador, arreglo_expresion.identificador)]['tipado']:
                            return RetornoError("No se puede realizar la operacion relacional '{} = {}' debido a que no poseen el mismo tipo de dato.".format(res_identificador_ejecutar['identificador'], arreglo_expresion.identificador))

                        if tupla_identificador["{}.{}".format(res_identificador_ejecutar['referencia_tabla'], res_identificador_ejecutar['identificador'])]['valor'] == tupla_expresion["{}.{}".format(arreglo_expresion.tabla_del_identificador, arreglo_expresion.identificador)]['valor']:
                            tupla_homologacion = {}
                            tupla_homologacion.update(tupla_identificador)
                            tupla_homologacion.update(tupla_expresion)
                            arreglo_homologacion.append(tupla_homologacion)

                return RetornoArreglo(None, None, arreglo_homologacion)

            else:
                return RetornoError("Ha ocurrido un error al realizar la condición (=).")

    # TODO: Corregir el graficado del arbol debido a que se han modificado los parametros que se solicitan en la asignacion
    def GraficarArbol(self, id_padre):
        return ""
        # label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        # label_exp_izq = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "AIZQ", self.expresion_izquierda)
        # union_enca_exp_izq = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "AIZQ")

        # label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "op", self.operador)
        # union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "op")
        # resultado_exp = ""

        # if isinstance(self.expresion, list):
        #     print("es lista")
        #     for exp in self.expresion:
        #         union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
        #         resultado_izquierda = exp.GraficarArbol(self.id_nodo)
        #         resultado_exp += union_hijo_izquierdo + resultado_izquierda
        # else:
        #     union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        #     resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
        #     resultado_exp += union_hijo_izquierdo + resultado_izquierda

        # return label_encabezado+ label_exp_izq+union_enca_exp_izq +label_operador + union_enca_operador+ resultado_exp
