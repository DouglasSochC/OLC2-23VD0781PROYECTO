from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_E
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoArreglo

class Alias(Expresion):

    def __init__(self, id_nodo: str, expresion: Expresion_E, alias: str):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.alias = alias

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no si se esta construyendo un procedimiento o una funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_ejecutar, RetornoError):
                return res_ejecutar
            elif isinstance(res_ejecutar, RetornoCodigo):
                return RetornoCodigo("{} AS {}".format(res_ejecutar.codigo, self.alias))
            else:
                return RetornoError("Se produjo un error al intentar definir la instrucción 'ALIAS' dentro de la creación del PROCEDURE.")

        else:

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
