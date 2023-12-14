from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO, RetornoLiteral
from datetime import datetime

class Literal(Expresion):

    def __init__(self, value, tipado):
        super().__init__()
        self.value = value
        self.tipado = tipado

    def Ejecutar(self, base_datos, entorno):

        if self.tipado == TIPO_DATO.BIT:

            if(len(str(self.value)) == 1):
                if(str(self.value) == "1" or str(self.value) == "0"):
                    return RetornoLiteral(int(self.value), TIPO_DATO.BIT)
                else:
                    return RetornoLiteral(self.value, TIPO_DATO.NULL)
            else:
                return RetornoLiteral(self.value, TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.INT:

            try:
                numero_entero = int(self.value)
                if (-2147483648 <= numero_entero <= 2147483647):
                    return RetornoLiteral(numero_entero, TIPO_DATO.INT)
                else:
                    return RetornoLiteral(numero_entero, TIPO_DATO.NULL)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.DECIMAL:

            try:
                numero_decimal = float(self.value)
                if (-2147483648 <= numero_decimal <= 2147483647):
                    return RetornoLiteral(numero_decimal, TIPO_DATO.DECIMAL)
                else:
                    return RetornoLiteral(numero_decimal, TIPO_DATO.NULL)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.DATE:

            try:
                fecha_obj = datetime.strptime(str(self.value), '%d-%m-%Y')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31)
                if fecha_minima <= fecha_obj <= fecha_maxima:
                    return RetornoLiteral(fecha_obj, TIPO_DATO.DATE)
                else:
                    return RetornoLiteral(fecha_obj, TIPO_DATO.NULL)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.DATETIME:

            try:
                fecha_hora_obj = datetime.strptime(str(self.value), '%d-%m-%Y %H:%M:%S')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59)
                if fecha_minima <= fecha_hora_obj <= fecha_maxima:
                    return RetornoLiteral(fecha_hora_obj, TIPO_DATO.DATETIME)
                else:
                    return RetornoLiteral(fecha_hora_obj, TIPO_DATO.NULL)
            except ValueError:
                return RetornoLiteral(self.value, TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.NCHAR:

            ref = len(str(self.value))
            if(1 <= ref <= 4000):
                return RetornoLiteral(str(self.value)[1:-1], TIPO_DATO.NCHAR)
            else:
                return RetornoLiteral(self.value[1:-1], TIPO_DATO.NULL)

        elif self.tipado == TIPO_DATO.NVARCHAR:

            ref = len(str(self.value))
            if(0 < ref <= 2000000):
                return RetornoLiteral(str(self.value)[1:-1], TIPO_DATO.NVARCHAR)
            else:
                return RetornoLiteral(self.value[1:-1], TIPO_DATO.NULL)
