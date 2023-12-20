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
    NULL = 7,
    BOOLEAN = 8

@unique
class TIPO_ENTORNO(Enum) :
    GLOBAL = 1
    SENTENCIA_DDL = 2
    SENTENCIA_DML = 3
    SENTENCIA_SSL = 4

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
    NOT_OP = 14

class RetornoLiteral:
    def __init__(self, valor: any = None, tipado: TIPO_DATO = TIPO_DATO.NULL, identificador: str = None):
        self.valor = valor
        self.tipado = tipado
        self.identificador = identificador

class RetornoArreglo:
    def __init__(self, identificador: str, tipado: TIPO_DATO = TIPO_DATO.NULL, lista: list = [], alias: str = None):
        self.identificador = identificador
        self.tipado = tipado
        self.lista = lista
        self.alias = alias

class RetornoCodigo:
    def __init__(self, codigo: str):
        self.codigo = codigo

# ELIMINAR
# ELIMINAR
# ELIMINAR
# ELIMINAR
class RetornoRelacional:
    def __init__(self, valor: bool, operacion_izquierda: list, operador :str, operacion_derecha: any):
        self.valor = valor
        self.operacion_izquierda = operacion_izquierda
        self.operador = operador
        self.operacion_derecha = operacion_derecha

# ELIMINAR
# ELIMINAR
# ELIMINAR
# ELIMINAR
class RetornoAsignacion:
    def __init__(self, nombre_variable: str, expresion: any):
        self.nombre_variable = nombre_variable
        self.expresion = expresion

class RetornoError:
    def __init__(self, msg: str):
        self.msg = msg

class RetornoCorrecto:
    def __init__(self, msg: str = None):
        self.msg = msg