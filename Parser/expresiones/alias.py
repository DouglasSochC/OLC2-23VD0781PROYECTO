from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoIdentificador

class Alias(Expresion):

    def __init__(self, id_nodo: int, expresion: any, alias: str):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.alias = alias

    def Ejecutar(self, base_datos, entorno):

        # En el caso que sea una instancia de 'RetornoError' se retorna el error encontrado
        if isinstance(self.expresion, RetornoError):
            return self.expresion

        res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        if isinstance(res_ejecutar, RetornoError):
            return res_ejecutar
        else:
            return RetornoIdentificador(res_ejecutar.identificador, res_ejecutar.tipado, res_ejecutar.lista, self.alias)

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "ALIAS")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion.id_nodo)
        
        resultado_izquierda = self.expresion.GraficarArbol(id_padre)

        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "as", self.alias)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "as")
        
        return label_encabezado + union_hijo_izquierdo+resultado_izquierda +label_operador+union_enca_operador