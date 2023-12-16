from Parser.abstract.retorno import TIPO_DATO, RetornoError, RetornoLiteral, RetornoIdentificador
from ..abstract.expresiones import Expresion
import datetime

class Funcion_Nativa(Expresion):

    def __init__(self,id_nodo, accion, expresiones):
        self.id_nodo = id_nodo
        self.accion = accion
        self.expresiones = expresiones

    def Ejecutar(self, base_datos, entorno):

        if self.expresiones is not None:

            if(self.accion == "CONCATENA"):

                respuesta = None
                alias = ""

                for exp in self.expresiones:

                    res_ejecutar = exp.Ejecutar(base_datos, entorno)

                    # En el caso que encuentre un error durante el ejecutar
                    if isinstance(res_ejecutar, RetornoError):
                        return res_ejecutar

                    if res_ejecutar.tipado == TIPO_DATO.NCHAR or res_ejecutar.tipado == TIPO_DATO.NVARCHAR:

                        if respuesta is None and isinstance(res_ejecutar, RetornoLiteral):

                            respuesta = res_ejecutar.valor
                            alias += res_ejecutar.valor

                        elif respuesta is None and isinstance(res_ejecutar, RetornoIdentificador):

                            respuesta = res_ejecutar.lista
                            alias += "{" + "{}".format(res_ejecutar.identificador) + "}"

                        elif isinstance(res_ejecutar, RetornoLiteral) and isinstance(respuesta, list):

                            for valor in respuesta:
                                valor['temporal'] = valor['temporal'] + res_ejecutar.valor
                            alias += res_ejecutar.valor

                        elif isinstance(res_ejecutar, RetornoLiteral) and isinstance(respuesta, list) is False:

                            respuesta += res_ejecutar.valor
                            alias += res_ejecutar.valor

                        elif isinstance(res_ejecutar, RetornoIdentificador) and isinstance(respuesta, list):

                            for llave, valor in enumerate(res_ejecutar.lista):
                                respuesta[llave]['temporal'] = respuesta[llave]['temporal'] + valor['temporal']
                            alias += "{" + "{}".format(res_ejecutar.identificador) + "}"

                        elif isinstance(res_ejecutar, RetornoIdentificador) and isinstance(respuesta, list) is False:

                            for valor in res_ejecutar.lista:
                                valor['temporal'] = respuesta + valor['temporal']
                            respuesta = []
                            respuesta = res_ejecutar.lista
                            alias = "{" + "{}".format(res_ejecutar.identificador) + "}"

                        elif isinstance(res_ejecutar, RetornoError):
                            return res_ejecutar

                    elif isinstance(res_ejecutar, RetornoIdentificador):
                        return RetornoError("La concatenación no puede llevarse a cabo con la columna '{}' debido a que no es un tipo de dato válido.".format(res_ejecutar.identificador))
                    elif isinstance(res_ejecutar, RetornoLiteral):
                        return RetornoError("La concatenación no puede llevarse a cabo con el valor '{}' debido a que no es un tipo de dato válido.".format(res_ejecutar.valor))


                if isinstance(respuesta, list):
                    return RetornoIdentificador(alias, TIPO_DATO.NVARCHAR, respuesta)
                else:
                    return RetornoLiteral(respuesta, TIPO_DATO.NVARCHAR)

            elif(self.accion == "SUBSTRAER"):

                respuesta = None

                if len(self.expresiones) != 3:
                    return RetornoError("ERROR: No se puede realizar la operacion SUBSTRAER debido a que la cantidad de parametros no son adecuados (3).")

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
                        return RetornoError("ERROR: El valor del inicial debe de ser entero")
                    elif isinstance(longitud, RetornoLiteral)  is False:
                        return RetornoError("ERROR: El valor de la longitud debe de ser entero")

                    texto.valor = texto.valor[inicial.valor:longitud.valor]
                    return RetornoLiteral(texto.valor, TIPO_DATO.NVARCHAR)

                elif isinstance(texto, RetornoIdentificador):

                    if isinstance(inicial, RetornoLiteral) is False:
                        return RetornoError("ERROR: El valor del inicial debe de ser entero")
                    elif isinstance(longitud, RetornoLiteral)  is False:
                        return RetornoError("ERROR: El valor de la longitud debe de ser entero")

                    for valor in texto.lista:
                        valor['temporal'] = valor['temporal'][inicial.valor:longitud.valor]

                    return RetornoIdentificador(texto.identificador, TIPO_DATO.NVARCHAR, texto.lista)

                return RetornoError("ERROR: Ha ocurrido un error al realizar la operacion SUBSTRAER.")

            # elif(self.accion == "CONTAR"):

            #     return RetornoLiteral(None, TIPO_DATO.INT)

            # elif(self.accion == "SUMA"):

            #     return RetornoLiteral(None, TIPO_DATO.DECIMAL)

            # elif(self.accion == "CAS"):

            #     return RetornoLiteral(None, TIPO_DATO.DECIMAL)

        else:

            if(self.accion == "HOY"):

                fecha_hora_actual = datetime.datetime.now()
                fecha_hora_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
                return RetornoLiteral(fecha_hora_formateada, TIPO_DATO.DATETIME)


        return RetornoError("ERROR: Ha ocurrido un error al realizar la funcion nativa")
    

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "A", self.accion)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "A")
        resultado_exp = ""
        if(self.expresiones is None):
            return label_encabezado + label_operador + union_enca_operador
        
        for exp in self.expresiones:
            union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
            resultado_izquierda = exp.GraficarArbol(self.id_nodo)
            resultado_exp += union_hijo_izquierdo + resultado_izquierda 
      
        return label_encabezado+ label_operador + union_enca_operador+ resultado_exp

     