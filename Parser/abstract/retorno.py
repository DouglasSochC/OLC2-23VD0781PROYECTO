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
    PROCEDURE = 9
    FUNCTION = 10

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
    def __init__(self, identificador: str, tabla_del_identificador: str, lista: list = [], alias: str = None):
        self.identificador = identificador
        self.tabla_del_identificador = tabla_del_identificador
        self.lista = lista
        self.alias = alias

class RetornoCodigo:
    def __init__(self, codigo: str):
        self.codigo = codigo

class RetornoError:
    def __init__(self, msg: str):
        self.msg = msg

class RetornoCorrecto:
    def __init__(self, msg: str = None):
        self.msg = msg

class RetornoMultiplesInstrucciones:
    def __init__(self, arreglo_mensajes: list, arreglo_arreglos: list):
        self.arreglo_mensajes = arreglo_mensajes
        self.arreglo_arreglos = arreglo_arreglos
