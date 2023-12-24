from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO, RetornoLiteral
from datetime import datetime

class Literal(Expresion):

    def __init__(self, id_nodo: str, value, tipado: TIPO_DATO, identificador: str = None):
        super().__init__()
        self.id_nodo = id_nodo
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
                    return RetornoLiteral(fecha_obj, TIPO_DATO.DATE, self.identificador)
                else:
                    return RetornoLiteral(fecha_obj, TIPO_DATO.NULL, self.identificador)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL, self.identificador)

        elif self.tipado == TIPO_DATO.DATETIME:

            try:
                fecha_hora_obj = datetime.strptime(str(self.value), '%d-%m-%Y %H:%M:%S')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59)
                if fecha_minima <= fecha_hora_obj <= fecha_maxima:
                    return RetornoLiteral(fecha_hora_obj, TIPO_DATO.DATETIME, self.identificador)
                else:
                    return RetornoLiteral(fecha_hora_obj, TIPO_DATO.NULL, self.identificador)
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

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "LITERAL")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.removeQuotes(self.value))
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
        return label_encabezado + label_valor + union_hijo

    def removeQuotes(self, value):
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                mundo_without_quotes = value.strip('"')
                return mundo_without_quotes
        return value