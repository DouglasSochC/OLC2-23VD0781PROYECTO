from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError, TIPO_DATO

class Aritmetica(Expresion):

    def __init__(self, expresion_izquierda: any, operador: str, expresion_derecha: any):
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

        if self.operador == '*':

            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):

                dominante = self.DominanteMultiplicacion(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} * {}' debido a que no son tipos de datos similares".format(exp_izq.identificador, exp_der.identificador))

                for indice, diccionario in enumerate(exp_izq.lista):

                    diccionario['temporal'] = diccionario['temporal'] * exp_der.lista[indice]['temporal']

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteMultiplicacion(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} * {}' debido a que no son tipos de datos similares".format(exp_izq.identificador, exp_der.valor))

                for diccionario in exp_izq.lista:
                    diccionario['temporal'] = diccionario['temporal'] * exp_der.valor

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoIdentificador):

                return RetornoError("ERROR: No se puede realizar la operacion {} * {}".format(exp_izq.valor, exp_der.identificador))

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteMultiplicacion(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} * {}' debido a que no son tipos de datos similares".format(exp_izq.valor, exp_der.valor))

                return RetornoLiteral(exp_izq.valor * exp_der.valor, dominante)

        elif self.operador == '/':

            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):

                dominante = self.DominanteDivision(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} / {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.identificador))

                for indice, diccionario in enumerate(exp_izq.lista):

                    try:
                        diccionario['temporal'] = diccionario['temporal'] / exp_der.lista[indice]['temporal']
                    except Exception as e:
                        return RetornoError("ERROR: Ha ocurrido un error al realizar la division '{} / {}' ".format(diccionario['temporal'], exp_der.lista[indice]['temporal']))

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteDivision(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} / {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.valor))

                for diccionario in exp_izq.lista:
                    diccionario['temporal'] = diccionario['temporal'] / exp_der.valor

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoIdentificador):

                return RetornoError("ERROR: No se puede realizar la operacion {} / {}".format(exp_izq.valor, exp_der.identificador))

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteDivision(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} / {}' debido a que no son tipos de datos similares".format(exp_izq.valor, exp_der.valor))

                try:
                    return RetornoLiteral(exp_izq.valor / exp_der.valor, dominante)
                except Exception as e:
                    return RetornoError("ERROR: Ha ocurrido un error al realizar la division '{} / {}' ".format(exp_izq.valor, exp_der.valor))

        elif self.operador == '+':

            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):

                dominante = self.DominanteSuma(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} + {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.identificador))

                for indice, diccionario in enumerate(exp_izq.lista):

                    diccionario['temporal'] = diccionario['temporal'] + exp_der.lista[indice]['temporal']

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteSuma(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} + {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.valor))

                for diccionario in exp_izq.lista:
                    diccionario['temporal'] = diccionario['temporal'] + exp_der.valor

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoIdentificador):

                return RetornoError("ERROR: No se puede realizar la operacion {} + {}".format(exp_izq.valor, exp_der.identificador))

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteSuma(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} + {}' debido a que no son tipos de datos similares.".format(exp_izq.valor, exp_der.valor))

                return RetornoLiteral(exp_izq.valor + exp_der.valor, dominante)

        elif self.operador == '-':

            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):

                dominante = self.DominanteResta(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} - {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.identificador))

                for indice, diccionario in enumerate(exp_izq.lista):

                    diccionario['temporal'] = diccionario['temporal'] - exp_der.lista[indice]['temporal']

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteResta(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} - {}' debido a que no son tipos de datos similares.".format(exp_izq.identificador, exp_der.valor))

                for diccionario in exp_izq.lista:
                    diccionario['temporal'] = diccionario['temporal'] - exp_der.valor

                return RetornoIdentificador(exp_izq.identificador, dominante, exp_izq.lista)

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoIdentificador):

                return RetornoError("ERROR: No se puede realizar la operacion {} - {}".format(exp_izq.valor, exp_der.identificador))

            elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

                dominante = self.DominanteResta(exp_izq.tipado, exp_der.tipado)
                if  dominante == TIPO_DATO.NULL:
                    return RetornoError("ERROR: No se puede realizar la operacion '{} - {}' debido a que no son tipos de datos similares.".format(exp_izq.valor, exp_der.valor))

                return RetornoLiteral(exp_izq.valor - exp_der.valor, dominante)

        return RetornoError("ERROR: Ha ocurrido un error al realizar una operación aritmetica.")

    def GraficarArbol(self, id_padre):
        return ""