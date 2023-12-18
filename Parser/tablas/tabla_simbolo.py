from ..abstract.retorno import  TIPO_ENTORNO, TIPO_TOKEN, RetornoTipoDato

class Simbolo() :
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id: int, tipo_dato: RetornoTipoDato, tipo_token: TIPO_TOKEN, valor: any, ambito: TIPO_ENTORNO):
        self.id = id
        self.tipo_dato = tipo_dato
        self.tipo_token = tipo_token
        self.valor = valor
        self.ambito = ambito


class TablaDeSimbolos() :
    'Esta clase representa la tabla de simbolos'

    def __init__(self, entorno: TIPO_ENTORNO, simbolos = {}) :
        self.entorno = entorno
        self.simbolos = simbolos

       

    def agregar(self, simbolo) :
        self.simbolos[simbolo.id] = simbolo
    

    def obtener(self, id):
        if not id in self.simbolos :
            return None
        return self.simbolos[id]

    def actualizar(self, simbolo) :
        if not simbolo.id in self.simbolos :
            print('Error: variable ', simbolo.id, ' no definida.')
        else :
            self.simbolos[simbolo.id] = simbolo
            
