from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO, RetornoLiteral
from datetime import datetime

class Literal(Expresion):

    def __init__(self, value: any, tipado: TIPO_DATO, identificador: str = None):
        self.value = value
        self.tipado = tipado
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):

        if self.tipado == TIPO_DATO.BIT:

            if(len(str(self.value)) == 1):
                if(str(self.value) == "1" or str(self.value) == "0"):
                    return RetornoLiteral(int(self.value), TIPO_DATO.BIT, self.identificador)
                else:
                    return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)
            else:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.INT:

            try:
                numero_entero = int(self.value)
                if (-2147483648 <= numero_entero <= 2147483647):
                    return RetornoLiteral(numero_entero, TIPO_DATO.INT, self.identificador)
                else:
                    return RetornoLiteral(numero_entero, TIPO_DATO.NULL, self.identificador)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.DECIMAL:

            try:
                numero_decimal = float(self.value)
                if (-2147483648 <= numero_decimal <= 2147483647):
                    return RetornoLiteral(numero_decimal, TIPO_DATO.DECIMAL, self.identificador)
                else:
                    return RetornoLiteral(numero_decimal, TIPO_DATO.NULL, self.identificador)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.DATE:

            try:
                fecha_obj = datetime.strptime(str(self.value), '%d-%m-%Y')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31)
                if fecha_minima <= fecha_obj <= fecha_maxima:
                    return RetornoLiteral(str(self.value), TIPO_DATO.DATE, self.identificador)
                else:
                    return RetornoLiteral(str(self.value), TIPO_DATO.NULL, self.identificador)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.DATETIME:

            try:
                fecha_hora_obj = datetime.strptime(str(self.value), '%d-%m-%Y %H:%M:%S')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59)
                if fecha_minima <= fecha_hora_obj <= fecha_maxima:
                    return RetornoLiteral(str(self.value), TIPO_DATO.DATETIME, self.identificador)
                else:
                    return RetornoLiteral(str(self.value), TIPO_DATO.NULL, self.identificador)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.NCHAR:

            ref = len(str(self.value))
            if(1 <= ref <= 4000):
                return RetornoLiteral(str(self.value), TIPO_DATO.NCHAR, self.identificador)
            else:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.NVARCHAR:

            ref = len(str(self.value))
            if(0 < ref <= 2000000):
                return RetornoLiteral(str(self.value), TIPO_DATO.NVARCHAR, self.identificador)
            else:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_literal = hash("LITERAL" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_literal, "LITERAL")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_literal)
        result = label_encabezado + union

        # Se crea el nodo del valor del literal y se une con el nodo de literal
        contador[0] += 1
        id_nodo_valor_literal = hash("VALOR_LITERAL" + str(contador[0]))
        label_valor_literal = "\"{}\"[label=\"{}\"];\n".format(id_nodo_valor_literal, self.value)
        union_valor_literal = "\"{}\"->\"{}\";\n".format(id_nodo_literal, id_nodo_valor_literal)
        result += label_valor_literal + union_valor_literal

        # Se crea el nodo del tipado del literal y se une con el nodo de literal
        contador[0] += 1
        id_nodo_tipado_literal = hash("TIPADO_LITERAL" + str(contador[0]))
        label_tipado_literal = "\"{}\"[label=\"{}\"];\n".format(id_nodo_tipado_literal, self.tipado.name)
        union_tipado_literal = "\"{}\"->\"{}\";\n".format(id_nodo_literal, id_nodo_tipado_literal)
        result += label_tipado_literal + union_tipado_literal

        return result
