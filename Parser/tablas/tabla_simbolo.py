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

    def __init__(self, padre: 'TablaDeSimbolos' = None, hijo: list['TablaDeSimbolos'] = [], realizado_en: str = ""):
        self.simbolos = {}
        self.padre = padre
        self.hijo = hijo
        self.realizado_en = realizado_en

    def agregar_hijo(self, hijo: 'TablaDeSimbolos'):
        self.hijo.append(hijo)

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

    def actualizar(self, simbolo: Simbolo):

        # Se busca el simbolo en el entorno actual
        if not simbolo.id in self.simbolos:

            # Caso contrario que no se encuentre se busca en un nivel superior
            if self.padre is not None:
                return self.padre.actualizar(simbolo)

            return None

        self.simbolos[simbolo.id] = simbolo
