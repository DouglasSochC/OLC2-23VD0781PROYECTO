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

            respuesta = []
            arreglo_izquierdo = None
            arreglo_derecho = None
            llave_izquierda = None
            llave_derecha = None

            # Se basa en el arreglo exp_izq y la exp_der la operacion aritmetica
            simbolo_select_datos = entorno.obtener("select_de_datos")
            if simbolo_select_datos is None:

                # Se basa en los arreglos exp_izq y exp_der para realizar la operacion aritmetica estos arreglos deben tener una misma dimension y deben de ser la misma tabla
                simbolo = entorno.obtener("condicion")
                if simbolo is None:

                    if len(exp_izq.lista) != len(exp_der.lista):
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no poseen el mismo tamaño.".format(exp_izq.identificador, self.operador, exp_der.identificador))
                    elif exp_izq.tabla_del_identificador != exp_der.tabla_del_identificador:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no pertenecen a la misma tabla.".format(exp_izq.identificador, self.operador, exp_der.identificador))

                    # Se definen los arreglos
                    arreglo_izquierdo = exp_izq
                    arreglo_derecho = exp_der

                    # Se definen las llaves para obtener los valores
                    llave_izquierda = "{}.{}".format(arreglo_izquierdo.tabla_del_identificador, arreglo_izquierdo.identificador) if arreglo_izquierdo.identificador is not None else "auxiliar"
                    llave_derecha = "{}.{}".format(arreglo_derecho.tabla_del_identificador, arreglo_derecho.identificador) if arreglo_derecho.identificador is not None else "auxiliar"

                else:

                    # Se definen las llaves para obtener los valores
                    llave_izquierda = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                    llave_derecha = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"

                    # Se definen los arreglos
                    arreglo_izquierdo = exp_izq if llave_izquierda == "auxiliar" else simbolo.valor
                    arreglo_derecho = exp_der if llave_derecha == "auxiliar" else simbolo.valor

                for llave, tupla in enumerate(arreglo_izquierdo.lista):

                    # Se verifica que existan las llaves
                    if llave_izquierda not in arreglo_izquierdo.lista[llave] or llave_derecha not in arreglo_derecho.lista[llave]:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

                    # Se obtiene los valores que seran utilizados para realizar el calculo
                    valor_izquierdo = arreglo_izquierdo.lista[llave][llave_izquierda]
                    valor_derecho = arreglo_derecho.lista[llave][llave_derecha]

                    # Se verifica si el valor es None para no realizar la operacion
                    if valor_izquierdo['valor'] is None or valor_derecho['valor'] is None:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

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
                        return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho['valor']))

                   # Valores de la llave auxiliar
                    auxiliar_valor = 0
                    auxiliar_tipado = dominante

                    try:
                        auxiliar_valor = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho['valor']")
                    except Exception as e:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho['valor']))

                    tupla_homologacion = {}
                    tupla_homologacion.update(tupla)
                    tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })
                    respuesta.append(tupla_homologacion)

                return RetornoArreglo(None, arreglo_izquierdo.tabla_del_identificador, respuesta, None)

            else:

                respuesta = []
                identificador_izquierdo = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                identificador_derecho = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"
                arreglo_izquierdo = exp_izq.lista if identificador_izquierdo == "auxiliar" else simbolo_select_datos.valor
                arreglo_derecho = exp_der.lista if identificador_derecho == "auxiliar" else simbolo_select_datos.valor

                for indice, tupla in enumerate(arreglo_derecho):

                    if identificador_izquierdo not in arreglo_izquierdo[indice]:
                        texto_izquierdo = identificador_izquierdo if identificador_izquierdo != "auxiliar" else arreglo_izquierdo[indice]['auxiliar']
                        texto_derecho = identificador_derecho if identificador_derecho != "auxiliar" else arreglo_derecho[indice]['auxiliar']
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'. debido a que no existe la columna '{}' en la tabla '{}'.".format(texto_izquierdo, self.operador, texto_derecho, texto_izquierdo, exp_izq.tabla_del_identificador))
                    elif identificador_derecho not in arreglo_derecho[indice]:
                        texto_izquierdo = identificador_izquierdo if identificador_izquierdo != "auxiliar" else arreglo_izquierdo[indice]['auxiliar']
                        texto_derecho = identificador_derecho if identificador_derecho != "auxiliar" else arreglo_derecho[indice]['auxiliar']
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}'. debido a que no existe la columna '{}' en la tabla '{}'.".format(texto_izquierdo, self.operador, texto_derecho, texto_derecho, exp_der.tabla_del_identificador))

                    valor_izquierdo = arreglo_izquierdo[indice][identificador_izquierdo]
                    valor_derecho = arreglo_derecho[indice][identificador_derecho]

                    if valor_izquierdo['valor'] is not None and valor_derecho['valor'] is not None:

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
                            return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho['valor']))

                        # Valores de la llave auxiliar
                        auxiliar_valor = 0
                        auxiliar_tipado = dominante

                        try:
                            auxiliar_valor = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho['valor']")
                        except Exception as e:
                            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_izquierdo['valor']))

                    respuesta.append({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })

                return RetornoArreglo(None, exp_izq.tabla_del_identificador, respuesta)

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoLiteral):

            # Se basa en el arreglo exp_izq la operacion aritmetica
            simbolo_select_datos = entorno.obtener("select_de_datos")
            if simbolo_select_datos is None:

                respuesta = []
                arreglo_izquierdo = None
                llave_izquierda = None

                # Se basa en el arreglo exp_izq la operacion aritmetica
                simbolo = entorno.obtener("condicion")
                if simbolo is None:
                    # Se setean los valores que seran utilizados para realizar el calculo
                    arreglo_izquierdo = exp_izq
                    llave_izquierda = "{}.{}".format(arreglo_izquierdo.tabla_del_identificador, arreglo_izquierdo.identificador) if arreglo_izquierdo.identificador is not None else "auxiliar"
                else:
                    # Se setean los valores que seran utilizados para realizar el calculo
                    llave_izquierda = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                    arreglo_izquierdo = exp_izq if llave_izquierda == "auxiliar" else simbolo.valor

                for llave, tupla in enumerate(arreglo_izquierdo.lista):

                    # Se verifica que exista la llave
                    if llave_izquierda not in arreglo_izquierdo.lista[llave]:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

                    # Se obtiene los valores que seran utilizados para realizar el calculo
                    valor_izquierdo = arreglo_izquierdo.lista[llave][llave_izquierda]
                    valor_derecho = exp_der

                    # Se verifica si el valor es None para no realizar la operacion
                    if valor_izquierdo['valor'] is None:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

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
                        return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                    # Valores de la llave auxiliar
                    auxiliar_valor = 0
                    auxiliar_tipado = dominante

                    try:
                        auxiliar_valor = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho.valor")
                    except Exception as e:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                    tupla_homologacion = {}
                    tupla_homologacion.update(tupla)
                    tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })
                    respuesta.append(tupla_homologacion)

                return RetornoArreglo(None, arreglo_izquierdo.tabla_del_identificador, respuesta, None)
            else:

                respuesta = []
                identificador_izquierdo = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                arreglo_izquierdo = exp_izq.lista if identificador_izquierdo == "auxiliar" else simbolo_select_datos.valor

                valor_derecho = exp_der
                for tupla in arreglo_izquierdo:

                    if identificador_izquierdo not in tupla:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no existe la columna '{}' en la tabla '{}'.".format(tupla[identificador_izquierdo]['valor'], self.operador, valor_derecho.valor, identificador_izquierdo, exp_izq.tabla_del_identificador))

                    valor_izquierdo = tupla[identificador_izquierdo]

                    if valor_izquierdo['valor'] is not None:

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
                            return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                        # Valores de la llave auxiliar
                        auxiliar_valor = 0
                        auxiliar_tipado = dominante

                        try:
                            auxiliar_valor = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho.valor")
                        except Exception as e:
                            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                    respuesta.append({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })

                return RetornoArreglo(None, exp_izq.tabla_del_identificador, respuesta)

        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoArreglo):

            # Se basa en el arreglo exp_izq la operacion aritmetica
            simbolo_select_datos = entorno.obtener("select_de_datos")
            if simbolo_select_datos is None:

                respuesta = []
                arreglo_derecho = None
                llave_derecha = None

                # Se basa en el arreglo exp_der la operacion aritmetica
                simbolo = entorno.obtener("condicion")
                if simbolo is None:
                    # Se setean los valores que seran utilizados para realizar el calculo
                    arreglo_derecho = exp_der
                    llave_derecha = "{}.{}".format(arreglo_derecho.tabla_del_identificador, arreglo_derecho.identificador) if arreglo_derecho.identificador is not None else "auxiliar"
                else:
                    # Se setean los valores que seran utilizados para realizar el calculo
                    llave_derecha = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"
                    arreglo_derecho = exp_der if llave_derecha == "auxiliar" else simbolo.valor

                for llave, tupla in enumerate(arreglo_derecho.lista):

                    # Se verifica que existan las llaves
                    if llave_derecha not in arreglo_derecho.lista[llave]:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

                    # Se obtiene los valores que seran utilizados para realizar el calculo
                    valor_izquierdo = exp_izq
                    valor_derecho = arreglo_derecho.lista[llave][llave_derecha]

                    # Se verifica si el valor es None para no realizar la operacion
                    if valor_derecho['valor'] is None:
                        tupla_homologacion = {}
                        tupla_homologacion.update(tupla)
                        tupla_homologacion.update({ "auxiliar": { 'valor': None, 'tipado': TIPO_DATO.NULL } })
                        respuesta.append(tupla_homologacion)
                        continue

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
                        return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo.valor, self.operador, valor_derecho['valor']))

                    # Valores de la llave auxiliar
                    auxiliar_valor = 0
                    auxiliar_tipado = dominante

                    try:
                        auxiliar_valor = eval(f"valor_izquierdo.valor {self.operador} valor_derecho['valor']")
                    except Exception as e:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo.valor, self.operador, valor_derecho['valor']))

                    tupla_homologacion = {}
                    tupla_homologacion.update(tupla)
                    tupla_homologacion.update({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })
                    respuesta.append(tupla_homologacion)

                return RetornoArreglo(None, arreglo_derecho.tabla_del_identificador, respuesta, None)

            else:

                respuesta = []
                identificador_derecho = "{}.{}".format(exp_der.tabla_del_identificador, exp_der.identificador) if exp_der.identificador is not None else "auxiliar"
                arreglo_derecho = exp_der.lista if identificador_derecho == "auxiliar" else simbolo_select_datos.valor

                valor_izquierdo = exp_izq
                for tupla in arreglo_derecho:

                    if identificador_derecho not in tupla:
                        return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a que no existe la columna '{}' en la tabla '{}'.".format(valor_izquierdo.valor, self.operador, tupla[identificador_derecho]['valor'], identificador_derecho, exp_der.tabla_del_identificador))

                    valor_derecho = tupla[identificador_derecho]

                    if valor_derecho['valor'] is not None:

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
                            return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(valor_izquierdo.valor, self.operador, valor_derecho['valor']))

                        # Valores de la llave auxiliar
                        auxiliar_valor = 0
                        auxiliar_tipado = dominante

                        try:
                            auxiliar_valor = eval(f"valor_izquierdo.valor {self.operador} valor_derecho['valor']")
                        except Exception as e:
                            return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_izquierdo.valor))

                    respuesta.append({ "auxiliar": { 'valor': auxiliar_valor, 'tipado': auxiliar_tipado } })

                return RetornoArreglo(None, exp_der.tabla_del_identificador, respuesta)

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
                    return RetornoError("No se puede realizar la operacion '{} {} {}' debido a que no son tipos de datos similares".format(representacion_izquierda, self.operador, representacion_derecha))

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