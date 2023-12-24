from Parser.abstract.retorno import TIPO_DATO, RetornoError, RetornoLiteral, RetornoArreglo
from ..abstract.expresiones import Expresion
import datetime

class Funcion_Nativa(Expresion):

    def __init__(self, id_nodo: str, accion: str, expresiones: any):
        self.id_nodo = id_nodo
        self.accion = accion
        self.expresiones = expresiones

    def Ejecutar(self, base_datos, entorno):

        if self.expresiones is not None:

            if(self.accion == "concatena"):

                respuesta = None
                alias = ""

                for exp in self.expresiones:

                    res_ejecutar = exp.Ejecutar(base_datos, entorno)

                    # En el caso que encuentre un error durante el ejecutar
                    if isinstance(res_ejecutar, RetornoError):
                        return res_ejecutar

                    elif respuesta is None and isinstance(res_ejecutar, RetornoLiteral):

                        respuesta = str(res_ejecutar.valor)
                        alias += '"{}",'.format(res_ejecutar.valor)

                    elif respuesta is None and isinstance(res_ejecutar, RetornoArreglo):

                        # Se basa en el arreglo res_ejecutar
                        simbolo_select_datos = entorno.obtener("select_de_datos")
                        respuesta = []

                        llave = "{}.{}".format(res_ejecutar.tabla_del_identificador, res_ejecutar.identificador)

                        for tupla in simbolo_select_datos.valor:

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_ejecutar.identificador, res_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                respuesta.append({'auxiliar': ''})
                            else:
                                respuesta.append({'auxiliar': str(tupla[llave]['valor'])})

                        alias += "{" + str(res_ejecutar.identificador) + "},"

                    elif isinstance(res_ejecutar, RetornoLiteral) and isinstance(respuesta, list):

                        for valor in respuesta:
                            valor['auxiliar'] = valor['auxiliar'] + str(res_ejecutar.valor)
                        alias += '"{}",'.format(res_ejecutar.valor)

                    elif isinstance(res_ejecutar, RetornoLiteral) and isinstance(respuesta, str):

                        respuesta += str(res_ejecutar.valor)
                        alias += '"{}",'.format(res_ejecutar.valor)

                    elif isinstance(res_ejecutar, RetornoArreglo) and isinstance(respuesta, list):

                        # Se basa en el arreglo res_ejecutar
                        simbolo_select_datos = entorno.obtener("select_de_datos")

                        llave = "{}.{}".format(res_ejecutar.tabla_del_identificador, res_ejecutar.identificador)

                        for indice, tupla in enumerate(simbolo_select_datos.valor):

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_ejecutar.identificador, res_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                respuesta[indice]['auxiliar'] += ''
                            else:
                                respuesta[indice]['auxiliar'] += str(tupla[llave]['valor'])

                        alias += "{" + str(res_ejecutar.identificador) + "},"

                    elif isinstance(res_ejecutar, RetornoArreglo) and isinstance(respuesta, str):

                        # Se basa en el arreglo res_ejecutar
                        simbolo_select_datos = entorno.obtener("select_de_datos")
                        temporal_str = respuesta
                        respuesta = []

                        llave = "{}.{}".format(res_ejecutar.tabla_del_identificador, res_ejecutar.identificador)

                        for indice, tupla in enumerate(simbolo_select_datos.valor):

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_ejecutar.identificador, res_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                respuesta.append({'auxiliar': temporal_str})
                            else:
                                respuesta.append({'auxiliar': temporal_str + str(tupla[llave]['valor'])})

                        alias += "{" + str(res_ejecutar.identificador) + "},"

                if isinstance(respuesta, list):
                    return RetornoArreglo("CONCATENAR({})".format(alias[:-1]), None, respuesta)
                else:
                    return RetornoLiteral(respuesta, TIPO_DATO.NVARCHAR)

            elif(self.accion == "substraer"):

                respuesta = []
                alias = ""

                if len(self.expresiones) != 3:
                    return RetornoError("No se puede realizar la operacion SUBSTRAER debido a que la cantidad de parametros no son adecuados (3).")

                listado = []
                for exp in self.expresiones:

                    res_ejecutar = exp.Ejecutar(base_datos, entorno)

                    # En el caso que encuentre un error durante el ejecutar
                    if isinstance(res_ejecutar, RetornoError):
                        return res_ejecutar

                    listado.append(res_ejecutar)

                texto = listado[0]
                inicial = listado[1]
                longitud = listado[2]

                if isinstance(texto, RetornoLiteral):

                    if isinstance(inicial, RetornoLiteral) is False:
                        return RetornoError("El valor del inicial debe de ser entero")
                    elif isinstance(longitud, RetornoLiteral)  is False:
                        return RetornoError("El valor de la longitud debe de ser entero")

                    texto.valor = texto.valor[inicial.valor:longitud.valor]
                    return RetornoLiteral(texto.valor, TIPO_DATO.NVARCHAR)

                elif isinstance(texto, RetornoArreglo):

                    if isinstance(inicial, RetornoLiteral) is False:
                        return RetornoError("El valor del inicial debe de ser entero")
                    elif isinstance(longitud, RetornoLiteral)  is False:
                        return RetornoError("El valor de la longitud debe de ser entero")

                    # Se basa en el arreglo res_ejecutar
                    simbolo_select_datos = entorno.obtener("select_de_datos")
                    llave = "{}.{}".format(texto.tabla_del_identificador, texto.identificador) if texto.tabla_del_identificador is not None else "auxiliar"

                    for indice, tupla in enumerate(simbolo_select_datos.valor):

                        if llave == "auxiliar":
                            respuesta.append({'auxiliar': texto.lista[indice][llave][inicial.valor:longitud.valor]})
                        else:
                            respuesta.append({'auxiliar': tupla[llave]['valor'][inicial.valor:longitud.valor]})

                    alias += "SUBSTRAER({},{},{})".format(texto.identificador, inicial.valor, longitud.valor)

                    return RetornoArreglo(alias, None, respuesta)

                return RetornoError("Ha ocurrido un error al realizar la operacion SUBSTRAER.")

            # elif(self.accion == "contar"):

            #     return RetornoLiteral(None, TIPO_DATO.INT)

            # elif(self.accion == "suma"):

            #     return RetornoLiteral(None, TIPO_DATO.DECIMAL)

            # elif(self.accion == "cas"):

            #     return RetornoLiteral(None, TIPO_DATO.DECIMAL)

        else:

            if(self.accion == "hoy"):

                fecha_hora_actual = datetime.datetime.now()
                fecha_hora_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
                return RetornoLiteral(fecha_hora_formateada, TIPO_DATO.DATETIME)


        return RetornoError("Ha ocurrido un error al realizar la funcion nativa")


    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "A", self.accion)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "A")
        resultado_exp = ""

        if(self.expresiones is None):
          return label_encabezado+ label_operador + union_enca_operador

        if isinstance(self.expresiones, list):
            print("es lista")
            for exp in self.expresiones:
                union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
                resultado_izquierda = exp.GraficarArbol(self.id_nodo)
                resultado_exp += union_hijo_izquierdo + resultado_izquierda
        else:
            union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresiones.id_nodo)
            resultado_izquierda = self.expresiones.GraficarArbol(self.id_nodo)
            resultado_exp += union_hijo_izquierdo + resultado_izquierda


        return label_encabezado+ label_operador + union_enca_operador+ resultado_exp
