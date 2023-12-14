import re
from datetime import datetime

class Respuesta:
    def __init__(self, success: bool, valor: str, lista: list = []):
        self.success = success
        self.valor = valor
        self.lista = lista

def es_entero(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def es_decimal(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def validar_tipo_dato(campo: str, valor: str, tipo: str, longitud: int = None):

    if tipo == 'int':

        if es_entero(valor):
            entero = int(valor)
            if entero < -2147483648 or entero > 2147483647:
                return "El campo '" + campo + "' debe estar dentro del rango [-2147483648,2147483647]"
        else:
            return "El campo '" + campo + "' debe de ser entero"

    elif tipo == 'bit':

        if valor is not None:
            if es_entero(valor):
                if int(valor) not in (1, 0):
                    return "El campo '" + campo + "' puede tomar únicamente los valores 0 o 1."
            else:
                return "El campo '" + campo + "' debe de ser entero"

    elif tipo == 'decimal':

        if es_decimal(valor):
            decimal = float(valor)
            if decimal < -2147483648 or decimal > 2147483647:
                return "El campo '" + campo + "' debe estar dentro del rango [-2147483648,2147483647]"
        else:
            return "El campo '" + campo + "' debe de ser numerico"

    elif tipo == 'date':

        # Patron para verificar el formato dd-mm-yyyy
        patron_formato = re.compile(r'^\d{2}-\d{2}-\d{4}$')

        # Validar el formato
        if not patron_formato.match(valor):
            return "El campo '" + campo + "' es invalido. El formato debe ser dd-mm-yyyy."

        # Convertir el string a objeto datetime
        try:
            fecha = datetime.strptime(valor, "%d-%m-%Y")
        except ValueError:
            return "El campo '" + campo + "' es invalido."

        # Verificar el rango
        fecha_minima = datetime(1753, 1, 1)
        fecha_maxima = datetime(9999, 12, 31)
        if fecha < fecha_minima or fecha > fecha_maxima:
            return "El campo '" + campo + "' esta fuera del rango permitido."

    elif tipo == 'datetime':

        # Patrón para verificar el formato dd-mmyyyy hh:mm:ss
        patron_formato = re.compile(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$')

        # Validar el formato
        if not patron_formato.match(valor):
            return "El campo '" + campo + "' es invalido. El formato debe ser dd-mm-yyyy hh:mm:ss."

        # Convertir el string a objeto datetime
        try:
            fecha = datetime.strptime(valor, "%d-%m-%Y %H:%M:%S")
        except ValueError:
           return "El campo '" + campo + "' es invalido."

        # Verificar el rango
        fecha_minima = datetime(1753, 1, 1, 0, 0, 0)
        fecha_maxima = datetime(9999, 12, 31, 23, 59, 59)

        if fecha < fecha_minima or fecha > fecha_maxima:
             return "El campo '" + campo + "' esta fuera del rango permitido."

    elif tipo == 'nchar':

        if len(valor) <= 0:
            return "El campo '" + campo + "' debe de contener por lo menos 1 caracter"
        elif len(valor) > int(longitud):
            return "El campo '" + campo + "' debe de contener menos de " + longitud + " caracteres"

    elif tipo == 'nvarchar':

        if len(valor) <= 0:
            return "El campo '" + campo + "' debe de contener por lo menos 1 caracter"
        elif len(valor) > int(longitud):
            return "El campo '" + campo + "' debe de contener menos de " + longitud + " caracteres"
