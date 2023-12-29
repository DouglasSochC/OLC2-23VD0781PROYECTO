from Parser.abstract.retorno import TIPO_DATO, RetornoError, RetornoLiteral, RetornoArreglo, RetornoCodigo
from ..abstract.expresiones import Expresion
from ..expresiones.tipo_dato import Tipo_Dato
from ..expresiones.identificador import Identificador
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from Funcionalidad.ssl import SSL
import datetime

class Funcion_Nativa(Expresion):

    def __init__(self, id_nodo: str, accion: str | Identificador, expresiones: any, tipo_dato: Tipo_Dato | None):
        self.id_nodo = id_nodo
        self.accion = accion
        self.expresiones = expresiones
        self.tipo_dato = tipo_dato

    def Ejecutar(self, base_datos, entorno):

        if(self.accion == "concatena"):

            if self.expresiones is None:
                return RetornoError("No se puede realizar la operacion 'CONCATENA' debido a que no se ha especificado ningun parametro.")

            respuesta = None
            alias = ""
            codigo = ""

            for exp in self.expresiones:

                res_ejecutar = exp.Ejecutar(base_datos, entorno)

                # En el caso que encuentre un error durante el ejecutar
                if isinstance(res_ejecutar, RetornoError):
                    return res_ejecutar
                elif isinstance(res_ejecutar, RetornoCodigo):
                    codigo += "{},".format(res_ejecutar.codigo)
                    continue

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

            if len(codigo) > 0:
                return RetornoCodigo("CONCATENA({})".format(codigo[:-1]))
            elif isinstance(respuesta, list):
                return RetornoArreglo("CONCATENA({})".format(alias[:-1]), None, respuesta)
            else:
                return RetornoLiteral(respuesta, TIPO_DATO.NVARCHAR)

        elif(self.accion == "substraer"):

            if self.expresiones is None:
                return RetornoError("No se puede realizar la operacion SUBSTRAER debido a que no se ha especificado ningun parametro.")

            respuesta = []
            alias = ""
            codigo = ""

            if len(self.expresiones) != 3:
                return RetornoError("No se puede realizar la operacion SUBSTRAER debido a que la cantidad de parametros no son adecuados (3).")

            listado = []
            for exp in self.expresiones:

                res_ejecutar = exp.Ejecutar(base_datos, entorno)

                # En el caso que encuentre un error durante el ejecutar
                if isinstance(res_ejecutar, RetornoError):
                    return res_ejecutar
                elif isinstance(res_ejecutar, RetornoCodigo):
                    codigo += "{},".format(res_ejecutar.codigo)
                    continue

                listado.append(res_ejecutar)

            if len(codigo) > 0:
                return RetornoCodigo("SUBSTRAER({})".format(codigo[:-1]))

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

        elif(self.accion == "cast"):
            tipo_identificador = entorno.obtener(self.expresiones.expresion.Ejecutar(base_datos, entorno)['identificador']).tipo_dato
            #dimension_identificador = entorno.obtener(self.expresiones.expresion.Ejecutar(base_datos, entorno)['identificador']).dimension
            valor_identificador = entorno.obtener(self.expresiones.expresion.Ejecutar(base_datos, entorno)['identificador']).valor
            tipo_nuevo = self.tipo_dato.Ejecutar(base_datos, entorno)['tipo_dato']
            #dimension_nuevo = self.tipo_dato.Ejecutar(base_datos, entorno)['dimension']
            dominante = self.DominanteAsignacion(tipo_identificador, tipo_nuevo)
            #id_nodo_identificador = entorno.obtener(self.expresiones.expresion.Ejecutar(base_datos, entorno)['identificador']).id
            #print(id_nodo_identificador)
            #print(tipo_identificador)
            #print(dimension_identificador)
            #print(valor_identificador)
            #print(tipo_nuevo)
            #print(dimension_nuevo)
            #print(dominante)
            #print("SIGUIENTE")
            if(dominante == TIPO_DATO.BIT):
                if(valor_identificador == 1 or valor_identificador == 0 or valor_identificador == "1" or valor_identificador == "0"):
                    #print(valor_identificador)
                    return RetornoLiteral(valor_identificador, dominante, None)
                else:
                    return RetornoError("Error, el tipo de dato valor de la expresion no puede convertirse en un BIT")
            elif(dominante == TIPO_DATO.INT):
                new_int = self.transformar_valor_int(valor_identificador)
                #print(new_int)
                return RetornoLiteral(new_int, dominante, None)
            elif(dominante == TIPO_DATO.DECIMAL):
                new_decimal = self.convertir_a_decimal(valor_identificador)
                #print(new_decimal)
                return RetornoLiteral(new_decimal, dominante, None)
            elif(dominante == TIPO_DATO.NCHAR or dominante == TIPO_DATO.NVARCHAR):
                new_text = self.convertir_a_texto(valor_identificador)
                if(new_text != None):
                    #print(new_text)
                    return RetornoLiteral(new_text, dominante, None)    
                else:
                    return RetornoError("Error, no es posible realizar el casting de INT a NVARCHAR O NCHAR con valores enteros mayores a 255")      
            else:
                return RetornoError("Error, no es posible realizar esa conversion por los tipos de datos de las expresiones utilizadas en la operacion")

        elif(self.accion == "hoy"):

            # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
            construccion = entorno.obtener("construir_procedimiento")
            construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
            if construccion is not None:
                return RetornoCodigo("HOY()")
            else:
                fecha_hora_actual = datetime.datetime.now()
                fecha_hora_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
                return RetornoLiteral(fecha_hora_formateada, TIPO_DATO.DATETIME)

        # Esto indica que es una funcion creada por el usuario
        else:

            res_accion_ejecutar = self.accion.Ejecutar(base_datos, entorno)
            nombre_funcion = res_accion_ejecutar['identificador']

            respuesta = None
            indice_parametro = 1
            alias = ""
            codigo = ""

            if self.expresiones is not None:

                for exp in self.expresiones:

                    res_exp_ejecutar = exp.Ejecutar(base_datos, entorno)

                    # En el caso que encuentre un error durante el ejecutar
                    if isinstance(res_exp_ejecutar, RetornoError):
                        return res_exp_ejecutar
                    elif isinstance(res_exp_ejecutar, RetornoCodigo):
                        codigo += "{},".format(res_exp_ejecutar.codigo)
                        continue

                    elif respuesta is None and isinstance(res_exp_ejecutar, RetornoLiteral):

                        respuesta = [{'valor': str(res_exp_ejecutar.valor), 'tipado': res_exp_ejecutar.tipado}]
                        alias += '{},'.format(res_exp_ejecutar.valor)

                    elif respuesta is None and isinstance(res_exp_ejecutar, RetornoArreglo):

                        # Se basa en el arreglo res_exp_ejecutar
                        simbolo_select_datos = entorno.obtener("select_de_datos")
                        respuesta = []

                        llave = "{}.{}".format(res_exp_ejecutar.tabla_del_identificador, res_exp_ejecutar.identificador)

                        for tupla in simbolo_select_datos.valor:

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_exp_ejecutar.identificador, res_exp_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                respuesta.append({'auxiliar': [{'valor': '', 'tipado': TIPO_DATO.NULL}]})
                            else:
                                respuesta.append({'auxiliar': [{'valor': str(tupla[llave]['valor']), 'tipado': tupla[llave]['tipado']}]})

                        alias += "{" + str(res_exp_ejecutar.identificador) + "},"

                    elif isinstance(res_exp_ejecutar, RetornoLiteral) and 'auxiliar' in respuesta[0]:

                        for valor in respuesta:
                            valor['auxiliar'].append({'valor': str(res_exp_ejecutar.valor), 'tipado': res_exp_ejecutar.tipado})
                        alias += '"{}",'.format(res_exp_ejecutar.valor)

                    elif isinstance(res_exp_ejecutar, RetornoLiteral) and 'auxiliar' not in respuesta[0]:

                        respuesta.append({'valor': str(res_exp_ejecutar.valor), 'tipado': res_exp_ejecutar.tipado})
                        alias += '"{}",'.format(res_exp_ejecutar.valor)

                    elif isinstance(res_exp_ejecutar, RetornoArreglo) and 'auxiliar' in respuesta[0]:

                        simbolo_select_datos = entorno.obtener("select_de_datos")

                        llave = "{}.{}".format(res_exp_ejecutar.tabla_del_identificador, res_exp_ejecutar.identificador)

                        for indice, tupla in enumerate(simbolo_select_datos.valor):

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_exp_ejecutar.identificador, res_exp_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                respuesta[indice]['auxiliar'].append({'valor': '', 'tipado': TIPO_DATO.NULL})
                            else:
                                respuesta[indice]['auxiliar'].append({'valor': str(tupla[llave]['valor']), 'tipado': tupla[llave]['tipado']})

                        alias += "{" + str(res_exp_ejecutar.identificador) + "},"

                    elif isinstance(res_exp_ejecutar, RetornoArreglo) and 'auxiliar' not in respuesta[0]:

                        # Se basa en el arreglo res_exp_ejecutar
                        simbolo_select_datos = entorno.obtener("select_de_datos")
                        temporal_str = respuesta
                        respuesta = []

                        llave = "{}.{}".format(res_exp_ejecutar.tabla_del_identificador, res_exp_ejecutar.identificador)

                        for indice, tupla in enumerate(simbolo_select_datos.valor):

                            if llave not in tupla:
                                return RetornoError("No se ha encontrado la columna '{}' en la tabla '{}'.".format(res_exp_ejecutar.identificador, res_exp_ejecutar.tabla_del_identificador))
                            elif tupla[llave]['valor'] is None:
                                auxiliar = temporal_str.copy()
                                auxiliar.append({'valor': '', 'tipado': TIPO_DATO.NULL})
                                respuesta.append({'auxiliar': auxiliar})
                            else:
                                auxiliar = temporal_str.copy()
                                auxiliar.append({'valor': str(tupla[llave]['valor']), 'tipado': tupla[llave]['tipado']})
                                respuesta.append({'auxiliar': auxiliar})

                        alias += "{" + str(res_exp_ejecutar.identificador) + "},"

                    else:
                        return RetornoError("El parametro no. '{}' es invalido.".format(indice_parametro))

                    indice_parametro += 1

            if len(codigo) > 0:
                return RetornoCodigo("{}({})".format(nombre_funcion, codigo[:-1]))

            lista_parametros = []
            es_un_literal = False
            # Esto significa que no trae ningun parametro
            if respuesta is None:
                lista_parametros.append([])
            # Esto significa que es un literal
            elif 'auxiliar' not in respuesta[0]:
                es_un_literal = True
                lista_parametros.append(respuesta)
            # Significa que es un arreglo
            elif 'auxiliar' in respuesta[0]:
                for res in respuesta:
                    lista_parametros.append(res['auxiliar'])

            respuesta = []
            for parametros in lista_parametros:
                ejecucion = self.__EjecutarFuncion(base_datos, entorno, nombre_funcion, parametros)
                if isinstance(ejecucion, RetornoError):
                    return RetornoError(ejecucion.msg)
                else:
                    respuesta.append(ejecucion)

            if es_un_literal:
                return RetornoLiteral(respuesta[0]['valor'], respuesta[0]['tipado'])
            else:
                arreglo = [{'auxiliar': res['valor']} for res in respuesta]
                return RetornoArreglo("{}({})".format(nombre_funcion, alias[:-1]), None, arreglo)

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

        if self.tipo_dato is not None:
            label_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
            resultado_exp += label_tipo_dato

        return label_encabezado+ label_operador + union_enca_operador+ resultado_exp

    def __EjecutarFuncion(sefl, base_datos: any, entorno: TablaDeSimbolos, nombre_funcion: str, lista_parametros: list) -> RetornoArreglo | RetornoLiteral:

        ssl = SSL()

        # Se valida que los parametros sean correctos para ser utilizados al ejecutar la funcion
        validar_parametros = ssl.verificar_parametros_funcion_y_obtener_query(base_datos.valor, nombre_funcion, lista_parametros)
        if validar_parametros.success is False:
            return RetornoError(validar_parametros.valor)

        # Se obtiene el query de la funcion
        query = validar_parametros.valor

        # Se genera un nuevo entorno para la funcion
        nuevo_entorno = TablaDeSimbolos(entorno, [], "FUNCION")

        # Se realiza el parseo del query que tiene el funcion
        from Parser.parser import parse
        instrucciones = parse(query)

        # Se revisa que se haya obtenido una instrucciones
        if instrucciones is not None:

            if isinstance(instrucciones, str):
                return RetornoError(instrucciones)
            else:
                for instr in instrucciones:
                    res = instr.Ejecutar(base_datos, nuevo_entorno)
                    if isinstance(res, RetornoError):
                        return RetornoError(res.msg)
                    elif isinstance(res, RetornoLiteral):
                        entorno.agregar_hijo(nuevo_entorno)
                        return {'valor': res.valor, 'tipado': res.tipado}

                entorno.agregar_hijo(nuevo_entorno)
                return RetornoError("La funcion '{}' no retorna ningun valor.".format(nombre_funcion))

    def transformar_valor_int(self, parametro):
        if isinstance(parametro, str):
            # Verifica si es una letra
            if len(parametro) == 1 and parametro.isalpha():
                return ord(parametro)  # Retorna el valor ASCII de la letra
            else:
                # Si es una palabra, suma los valores ASCII de cada carácter
                suma_ascii = sum(ord(caracter) for caracter in parametro)
                return suma_ascii
        elif isinstance(parametro, (int, float)):
            # Si es un número decimal, retorna el entero más cercano
            return round(parametro)
        else:
            return None  # Retorna None si el tipo de dato no es compatible
        
    def convertir_a_decimal(self, numero):
        return float(numero)
    
    def convertir_a_texto(self, valor):
        if isinstance(valor, int) and 0 <= valor <= 255:
            return chr(valor)  # Devuelve el carácter ASCII correspondiente
        else:
            return None