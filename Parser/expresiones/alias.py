from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_E
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoArreglo

class Alias(Expresion):

    def __init__(self, expresion: Expresion_E, alias: str):
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

    def GraficarArbol(self, id_nodo_padre: int, contador: list):
        contador[0] += 1
        id_nodo_alias = hash("CAMPO_TABLE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_alias, "ALIAS")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_alias)
        result = label_encabezado + union


        result += self.expresion.GraficarArbol(id_nodo_alias, contador)

        contador[0] += 1
        id_nodo_IDENTIFICADOR = hash("TIPO_ELIMINACION" + str(contador[0]))
        label_tipo_eliminacion = "\"{}\"[label=\"{}\"];\n".format(id_nodo_IDENTIFICADOR, self.alias)
        union_tipo_eliminacion = "\"{}\"->\"{}\";\n".format(id_nodo_alias, id_nodo_IDENTIFICADOR)
        result += label_tipo_eliminacion + union_tipo_eliminacion




        return result