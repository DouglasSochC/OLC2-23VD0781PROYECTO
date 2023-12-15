from enum import Enum, unique

@unique
class TIPO_DATO(Enum):
    BIT = 0,
    INT = 1,
    DECIMAL = 2,
    DATE = 3,
    DATETIME = 4,
    NCHAR = 5,
    NVARCHAR = 6,
    NULL = 7

@unique
class TIPO_TOKEN(Enum) :
    ALIAS = 1
    VARIABLE = 2
    FUNCION = 3
    PROCEDIMIENTO = 4
    SELECT = 5
    UPDATE = 6
    INSERT = 7
    DELETE = 8
    CREATE = 9
    USE = 10
    DROP = 11
    TRUNCATE = 12
    ALTER = 13
    EXEC = 14
    PARAMETRO = 15
    COLUMNA = 16
    NOMBRE_TABLA = 17

@unique
class TIPO_ENTORNO(Enum) :
    GLOBAL = 1
    IF = 2
    WHILE = 3
    FUNCION = 4
    PROCEDIMIENTO = 5

@unique
class TIPO_OPERACION(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION = 4
    MAYOR = 5
    MENOR = 6
    MAYORIGUAL = 7
    MENORIGUAL = 8
    IGUALIGUAL = 9
    DIFERENTEIGUAL = 10
    ASIGNACION = 11
    OR_OP = 12
    AND_OP = 13
    NOT = 14

class RetornoLiteral:
    def __init__(self, valor = None, tipado = TIPO_DATO.NULL):
        self.valor = valor
        self.tipado = tipado

class RetornoIdentificador:
    def __init__(self, identificador: str, tipado: TIPO_DATO, lista: list = [], alias: str = None):
        self.identificador = identificador
        self.tipado = tipado
        self.lista = lista
        self.alias = alias

class RetornoRelacional:
    def __init__(self, valor: bool, operacion_izquierda: list, operador :str, operacion_derecha: any):
        self.valor = valor
        self.operacion_izquierda = operacion_izquierda
        self.operador = operador
        self.operacion_derecha = operacion_derecha

class RetornoError:
    def __init__(self, msg: str):
        self.msg = msg