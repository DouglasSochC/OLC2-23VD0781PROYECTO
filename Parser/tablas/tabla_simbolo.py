from ..abstract.retorno import TIPO_DATO, TIPO_TOKEN

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id: int, tipo_dato: TIPO_DATO, tipo_token: TIPO_TOKEN, valor: any, ambito = None) :
        self.id = id
        self.tipo_dato = tipo_dato
        self.tipo_token = tipo_token
        self.valor = valor
        self.ambito = ambito

class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, simbolos = {}) :
        self.simbolos = simbolos

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id) :
        if not id in self.simbolos :
            return None

        return self.simbolos[id]
