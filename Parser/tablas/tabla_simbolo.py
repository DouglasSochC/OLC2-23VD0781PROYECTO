from ..abstract.retorno import TIPO_DATO, TIPO_ENTORNO

class Simbolo():
    'Esta clase representa un simbolo dentro de nuestra tabla de simbolos'

    def __init__(self, id: str,  valor: any, tipo_dato: TIPO_DATO, dimension: int, tipo_ambito: TIPO_ENTORNO):
        self.id = id
        self.valor = valor
        self.tipo_dato = tipo_dato
        self.dimension = dimension
        self.tipo_ambito = tipo_ambito

class TablaDeSimbolos():
    'Esta clase representa la tabla de simbolos'

    def __init__(self, padre: 'TablaDeSimbolos' = None):
        self.simbolos = {}
        self.padre = padre

    def agregar(self, simbolo: Simbolo):
        self.simbolos[simbolo.id] = simbolo

    def obtener(self, id: str) -> Simbolo:

        # Se busca el simbolo en el entorno actual
        if not id in self.simbolos:

            # Caso contrario que no se encuentre se busca en un nivel superior
            if self.padre is not None:
                return self.padre.obtener(id)

            return None

        return self.simbolos[id]

    def actualizar(self, simbolo):

        if not simbolo.id in self.simbolos:
            return False
        else:
            self.simbolos[simbolo.id] = simbolo
            return True
