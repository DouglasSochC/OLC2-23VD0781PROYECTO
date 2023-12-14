from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO, RetornoTipoDato 
from datetime import datetime

class Literal(Expresion):
    def __init__(self, value, tipado):
        super().__init__()
        self.value = value
        self.tipado = tipado
        
    def Ejecutar(self, base_datos, entorno):
        print("EJECUTANDO LITERAL")
        aux = RetornoTipoDato()
        if self.tipado.value[0] == 0:
            if(len(str(self.value)) == 1):
                if(str(self.value == "1") or str(self.value == "0")):
                    aux.__init__(int(self.value), TIPO_DATO.BIT, 1)
                else:
                    aux.__init__(self.value, TIPO_DATO.NULL, 0)
            else:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)
        elif self.tipado.value[0] == 1:
            try:
                numero_entero = int(self.value)
                if (-2147483648 <= numero_entero <= 2147483647):
                    aux.__init__(int(self.value), TIPO_DATO.INT, len(str(self.value)))
                else:
                    aux.__init__(self.value, TIPO_DATO.NULL, 0)
            except ValueError:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)
        elif self.tipado.value[0] == 2:
            try:
                numero_decimal = float(self.value)
                if (-2147483648 <= numero_decimal <= 2147483647):
                    aux.__init__(float(self.value), TIPO_DATO.DECIMAL, len(str(self.value)))
                else:
                    aux.__init__(self.value, TIPO_DATO.NULL, 0)
            except ValueError:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)
        elif self.tipado.value[0] == 3:
            try:
                fecha_obj = datetime.strptime(str(self.value), '%d-%m-%Y')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31)
                if fecha_minima <= fecha_obj <= fecha_maxima:
                    aux.__init__(fecha_obj, TIPO_DATO.DATE, len(str(self.value)))
                else:
                    aux.__init__(self.value, TIPO_DATO.NULL, 0)
            except ValueError:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)       
        elif self.tipado.value[0] == 4:
            try:
                fecha_hora_obj = datetime.strptime(str(self.value), '%d-%m-%Y %H:%M:%S')
                fecha_minima = datetime(year=1753, month=1, day=1)
                fecha_maxima = datetime(year=9999, month=12, day=31, hour=23, minute=59, second=59)

                if fecha_minima <= fecha_hora_obj <= fecha_maxima:
                    return aux.__init__(fecha_hora_obj, TIPO_DATO.DATETIME, len(str(self.value)))
                else:
                    aux.__init__(self.value, TIPO_DATO.NULL, 0)
            except ValueError:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)  
        elif self.tipado.value[0] == 5:
            ref = len(str(self.value))
            if(1 <= ref <= 4000):
                aux.__init__(str(self.value), TIPO_DATO.NCHAR, len(str(self.value))) 
            else:
                aux.__init__(self.value, TIPO_DATO.NULL, 0)
        elif self.tipado.value[0] == 6:
            ref = len(str(self.value))
            if(0 < ref <= 2000000):
                aux.__init__(str(self.value), TIPO_DATO.NVARCHAR, len(str(self.value)))
            else: 
                aux.__init__(self.value, TIPO_DATO.NULL, 0)
        else:
            aux.__init__(self.value, TIPO_DATO.NULL, 0)        
        return aux