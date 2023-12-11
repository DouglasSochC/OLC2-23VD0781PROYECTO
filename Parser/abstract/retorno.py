from enum import Enum, unique


@unique
class Type(Enum):
    BIT = 0,
    INT = 1,
    DECIMAL = 2,
    DATE = 3,
    DATETIME = 4,
    NCHAR = 5,
    NVARCHAR = 6,
    NULL = 7


class Retorno:
    def __init__(self, value = None, tipado = Type.NULL):
        self.value = value
        self.tipado = tipado