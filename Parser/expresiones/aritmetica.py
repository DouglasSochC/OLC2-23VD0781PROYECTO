from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_Normal
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoArreglo, RetornoLiteral, TIPO_DATO

class Aritmetica(Expresion):

    def __init__(self,id_nodo, expresion_izquierda: Expresion_Normal, operador: str, expresion_derecha: Expresion_Normal):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoError):
            return exp_izq

        elif isinstance(exp_der, RetornoError):
            return exp_der

        if isinstance(exp_izq, RetornoCodigo) and isinstance(exp_der, RetornoCodigo):
            return RetornoCodigo("{} {} {}".format(exp_izq.codigo, self.operador, exp_der.codigo))

        if isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoArreglo):

            simbolo = entorno.obtener("condicion")

            # Se basa en los arreglos exp_izq y exp_der para realizar la operacion aritmetica estos arreglos deben tener una misma dimension y deben de ser la misma tabla
            if simbolo is None:

                respuesta = []

                if len(exp_izq.lista) != len(exp_der.lista):
                    return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no poseen el mismo tamaño.".format(exp_izq.identificador, self.operador, exp_der.identificador))
                elif exp_izq.tabla_del_identificador != exp_der.tabla_del_identificador:
                    return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no pertenecen a la misma tabla.".format(exp_izq.identificador, self.operador, exp_der.identificador))
                else:

                    for llave, valor in enumerate(exp_izq.lista):

                        # Se definen las llaves para obtener los valores
                        llave_izquierda = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                        llave_derecha = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"

                        # Se obtiene los valores que seran utilizados para realizar el calculo
                        valor_izquierdo = exp_izq.lista[llave][llave_izquierda]
                        valor_derecho = exp_der.lista[llave][llave_derecha]

                        # Se verifica si se puede realizar la operacion segun el dominante
                        dominante = None
                        if self.operador == '*':
                            dominante = self.DominanteMultiplicacion(valor_izquierdo['tipado'], valor_derecho['tipado'])
                        elif self.operador == '/':
                            dominante = self.DominanteDivision(valor_izquierdo['tipado'], valor_derecho['tipado'])
                        elif self.operador == '+':
                            dominante = self.DominanteSuma(valor_izquierdo['tipado'], valor_derecho['tipado'])
                        elif self.operador == '-':
                            dominante = self.DominanteResta(valor_izquierdo['tipado'], valor_derecho['tipado'])
                        if dominante == TIPO_DATO.NULL:
                            return RetornoError("ERROR: No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho['valor']))

                        # Valores de la llave auxiliar
                        auxiliar = 0
                        tipado = dominante

                        try:
                            if valor_izquierdo['valor'] is None or valor_derecho['valor'] is None:
                                auxiliar = None
                            else:
                                auxiliar = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho['valor']")
                        except Exception as e:
                            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho['valor']))

                        tupla_homologacion = {}
                        tupla_homologacion.update(valor)
                        tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar, 'tipado': tipado } })
                        respuesta.append(tupla_homologacion)

                    return RetornoArreglo(None, exp_izq.tabla_del_identificador, respuesta, None)

            # Se basa en el simbolo de la tabla de simbolos para realizar la operacion aritmetica
            else:
                print()

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoLiteral):

            simbolo = entorno.obtener("condicion")

            # Se basa en el arreglo exp_izq la operacion aritmetica
            if simbolo is None:

                respuesta = []

                for llave, valor in enumerate(exp_izq.lista):

                    # Se definen la llave para obtener los valores
                    llave_izquierda = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"

                    # Se obtiene los valores que seran utilizados para realizar el calculo
                    valor_izquierdo = exp_izq.lista[llave][llave_izquierda]
                    valor_derecho = exp_der

                    # Se verifica si se puede realizar la operacion segun el dominante
                    dominante = None
                    if self.operador == '*':
                        dominante = self.DominanteMultiplicacion(valor_izquierdo['tipado'], valor_derecho.tipado)
                    elif self.operador == '/':
                        dominante = self.DominanteDivision(valor_izquierdo['tipado'], valor_derecho.tipado)
                    elif self.operador == '+':
                        dominante = self.DominanteSuma(valor_izquierdo['tipado'], valor_derecho.tipado)
                    elif self.operador == '-':
                        dominante = self.DominanteResta(valor_izquierdo['tipado'], valor_derecho.tipado)
                    if dominante == TIPO_DATO.NULL:
                        return RetornoError("ERROR: No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                    # Valores de la llave auxiliar
                    auxiliar = 0
                    tipado = dominante

                    try:
                        if valor_izquierdo['valor'] is None:
                            auxiliar = None
                        else:
                            auxiliar = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho.valor")
                    except Exception as e:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                    tupla_homologacion = {}
                    tupla_homologacion.update(valor)
                    tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar, 'tipado': tipado } })
                    respuesta.append(tupla_homologacion)

                return RetornoArreglo(None, exp_izq.tabla_del_identificador, respuesta, None)

            # Se basa en el simbolo de la tabla de simbolos para realizar la operacion aritmetica
            else:

                # respuesta = []

                # for tupla in exp_izq.lista:

                #     if "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) not in tupla:
                #         continue

                #     campo = tupla["{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador)]
                #     if campo['tipado'] != exp_der.tipado:
                #         return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(exp_izq.identificador, self.operador, ('"{}"'.format(exp_der.valor) if exp_der.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_der.valor)))

                #     if campo['valor'] is not None:
                #         try:
                #             campo['valor'] = eval(f"campo['valor'] {self.operador} exp_der.valor")
                #         except Exception as e:
                #             return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(exp_izq.identificador, self.operador, ('"{}"'.format(exp_der.valor) if exp_der.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_der.valor)))
                #         respuesta.append(tupla)

                # return RetornoArreglo(exp_izq.identificador, exp_izq.tabla_del_identificador, respuesta, exp_izq.alias)
                print()

        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoArreglo):

            simbolo = entorno.obtener("condicion")

            # Se basa en el arreglo exp_der la operacion aritmetica
            if simbolo is None:

                respuesta = []

                for llave, valor in enumerate(exp_der.lista):

                    # Se definen la llave para obtener los valores
                    llave_derecha = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"

                    # Se obtiene los valores que seran utilizados para realizar el calculo
                    valor_izquierdo = exp_izq
                    valor_derecho = exp_der.lista[llave][llave_derecha]

                    # Se verifica si se puede realizar la operacion segun el dominante
                    dominante = None
                    if self.operador == '*':
                        dominante = self.DominanteMultiplicacion(valor_izquierdo.tipado, valor_derecho['tipado'])
                    elif self.operador == '/':
                        dominante = self.DominanteDivision(valor_izquierdo.tipado, valor_derecho['tipado'])
                    elif self.operador == '+':
                        dominante = self.DominanteSuma(valor_izquierdo.tipado, valor_derecho['tipado'])
                    elif self.operador == '-':
                        dominante = self.DominanteResta(valor_izquierdo.tipado, valor_derecho['tipado'])
                    if dominante == TIPO_DATO.NULL:
                        return RetornoError("ERROR: No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo.valor, self.operador, valor_derecho['valor']))

                    # Valores de la llave auxiliar
                    auxiliar = 0
                    tipado = dominante

                    try:
                        if valor_derecho['valor'] is None:
                            auxiliar = None
                        else:
                            auxiliar = eval(f"valor_izquierdo.valor {self.operador} valor_derecho['valor']")
                    except Exception as e:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo.valor, self.operador, valor_derecho['valor']))

                    tupla_homologacion = {}
                    tupla_homologacion.update(valor)
                    tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar, 'tipado': tipado } })
                    respuesta.append(tupla_homologacion)

                return RetornoArreglo(None, exp_der.tabla_del_identificador, respuesta, None)

            # Se basa en el simbolo de la tabla de simbolos para realizar la operacion aritmetica
            else:

                print()
                # respuesta = []

                # for tupla in exp_der.lista:

                #     if "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) not in tupla:
                #         continue

                #     campo = tupla["{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador)]
                #     if campo['tipado'] != exp_izq.tipado:
                #         return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(('"{}"'.format(exp_izq.valor) if exp_izq.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_izq.valor), self.operador, exp_der.identificador))

                #     if campo['valor'] is not None:
                #         try:
                #             campo['valor'] = eval(f"exp_izq.valor {self.operador} campo['valor']")
                #         except Exception as e:
                #             return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(('"{}"'.format(exp_izq.valor) if exp_izq.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_izq.valor), self.operador, exp_der.identificador))
                #         respuesta.append(tupla)

                # return RetornoArreglo(exp_der.identificador, exp_der.tabla_del_identificador, respuesta, exp_der.alias)

        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

            representacion_izquierda = exp_izq.valor if exp_izq.identificador is None else exp_izq.identificador
            representacion_derecha = exp_der.valor if exp_der.identificador is None else exp_der.identificador
            dominante = None

            if self.operador == '*':
                dominante = self.DominanteMultiplicacion(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '/':
                dominante = self.DominanteDivision(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '+':
                dominante = self.DominanteSuma(exp_izq.tipado, exp_der.tipado)
            elif self.operador == '-':
                dominante = self.DominanteResta(exp_izq.tipado, exp_der.tipado)

            if dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(representacion_izquierda, self.operador, representacion_derecha))

            return RetornoLiteral(eval(f"exp_izq.valor {self.operador} exp_der.valor"), dominante, None)

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq.identificador, self.operador, exp_der['identificador']))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, RetornoArreglo):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der.identificador))
        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq.valor, self.operador, exp_der['identificador']))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, RetornoLiteral):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der.valor))
        elif isinstance(exp_izq, dict) and isinstance(exp_der, dict):
            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'.".format(exp_izq['identificador'], self.operador, exp_der['identificador']))

        return RetornoError("Ha ocurrido un error al realizar la operación aritmetica ({}).".format(self.operador))

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "ARITMETICA")

        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)

        resultado_izquierda = self.expresion_izquierda.GraficarArbol(self.id_nodo)
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "Op", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "Op")
        resultado_derecha = self.expresion_derecha.GraficarArbol(self.id_nodo)

        return label_encabezado + union_hijo_izquierdo  + resultado_izquierda + label_operador +union_enca_operador +resultado_derecha + union_hijo_derecho