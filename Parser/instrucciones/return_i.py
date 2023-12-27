from ..abstract.instrucciones import Instruccion
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoCodigo, RetornoError

class Return_I(Instruccion):

    def __init__(self, id_nodo: str, expresion: Expresion):
        self.id_nodo = id_nodo
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando el comando 'RETURN' dentro de la creacion de un procedimiento
        construir_procedimiento = entorno.obtener("construir_procedimiento")
        if construir_procedimiento is not None:
            return RetornoError("No es posible realizar una instrucción 'RETURN' dentro del cuerpo del PROCEDURE.")

        # Se verifica si el comando 'RETURN' esta siendo utilizado en la creacion de una funcion
        construir_procedimiento = entorno.obtener("construir_funcion")
        if construir_procedimiento is not None:

            res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion_ejecutar, RetornoCodigo):
                return RetornoCodigo("RETURN {};\n".format(res_expresion_ejecutar.codigo))
            else:
                return RetornoError("Se produjo un error al intentar definir la instrucción 'RETURN' dentro de la creación de una función.")

        else:
            res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            return res_expresion_ejecutar

    def GraficarArbol(self, id_padre):
        return ""