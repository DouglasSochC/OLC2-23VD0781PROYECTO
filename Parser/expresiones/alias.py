from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_E
from ..abstract.retorno import RetornoError, RetornoArreglo

class Alias(Expresion):

    def __init__(self, id_nodo: str, expresion: Expresion_E, alias: str):
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
            return RetornoArreglo(res_ejecutar.identificador, res_ejecutar.tabla_del_identificador, res_ejecutar.lista, self.alias)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ALIAS")
        resultado_exp = ""

        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
        resultado_exp += union_hijo_izquierdo + resultado_izquierda

        label_alias = "\"{}\"[label=\"{}\"];\n".format(self.alias, self.alias)
        union_alias = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.alias)

        return label_encabezado+ resultado_exp+ label_alias+ union_alias
