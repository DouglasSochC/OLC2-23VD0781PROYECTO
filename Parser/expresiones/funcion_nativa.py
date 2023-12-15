from Parser.abstract.retorno import TIPO_DATO, RetornoError, RetornoLiteral
from ..abstract.expresiones import Expresion
import datetime

class Funcion_Nativa(Expresion):

    def __init__(self, accion, expresiones):
        self.accion = accion
        self.expresiones = expresiones

    def Ejecutar(self, base_datos, entorno):

        if(self.expresiones is not None):

            lista_exp = self.expresiones

        if(self.accion == "HOY"):

            fecha_hora_actual = datetime.datetime.now()
            fecha_hora_formateada = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")
            return RetornoLiteral(fecha_hora_formateada, TIPO_DATO.DATETIME)

        elif(self.accion == "CONCATENA"):

            texto = ""
            for exp in lista_exp:
                aux = exp.Ejecutar(base_datos, entorno)
                if(aux.tipado == TIPO_DATO.NCHAR or aux.tipado == TIPO_DATO.NVARCHAR):
                    texto = texto + aux.valor
                else:
                    return RetornoError("ERROR: No se puede realizar la operacion CONCATENA debido a que no son tipos de datos compatibles")
            return RetornoLiteral(texto, TIPO_DATO.NVARCHAR)

        elif(self.accion == "SUBSTRAER"):

            texto = ""
            if(len(lista_exp) == 3):
                aux = lista_exp[0].Ejecutar(base_datos, entorno)
                aux2 = lista_exp[1].Ejecutar(base_datos, entorno)
                aux3 = lista_exp[2].Ejecutar(base_datos, entorno)
                texto = aux.valor[aux2.valor:aux3.valor]
                if(aux.tipado == TIPO_DATO.NCHAR or aux.tipado == TIPO_DATO.NVARCHAR)and(aux2.tipado == TIPO_DATO.INT or aux2.tipado == TIPO_DATO.BIT )and(aux3.tipado == TIPO_DATO.INT or aux3.tipado == TIPO_DATO.BIT):
                    if(len(aux.valor) >= aux3.valor) and (aux3.valor > aux2.valor):
                        texto = aux.valor[aux2.valor:aux3.valor]
                    else:
                        return RetornoError("ERROR: No se puede realizar la operacion SUBSTRAER debido a que los parametros no son de un tipo de dato compatible los parametros de inicio y fin de texto son erroneos")
                else:
                    return RetornoError("ERROR: No se puede realizar la operacion SUBSTRAER debido a que los parametros no son de un tipo de dato compatible con los parametros necesarios para esta funcion")
            else:
                return RetornoError("ERROR: No se puede realizar la operacion SUBSTRAER porque los parametros enviados son incorrectos")

            return RetornoLiteral(texto, TIPO_DATO.NVARCHAR)

        elif(self.accion == "CONTAR"):

            return RetornoLiteral(None, TIPO_DATO.INT)

        elif(self.accion == "SUMA"):

            return RetornoLiteral(None, TIPO_DATO.DECIMAL)

        return RetornoError("ERROR: Ha ocurrido un error al realizar la funcion nativa")