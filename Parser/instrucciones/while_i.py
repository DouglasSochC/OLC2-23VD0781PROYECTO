from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoLiteral, RetornoCorrecto, RetornoMultiplesInstrucciones
from ..expresiones.expresion import Expresion
from ..tablas.tabla_simbolo import TablaDeSimbolos

class While_I(Instruccion):
    def __init__(self, id_nodo: int, expresion: Expresion, lista_instrucciones: list):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.lista_instrucciones = lista_instrucciones

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            # Variables
            expresion = ""
            instrucciones = ""

            res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion_ejecutar, RetornoCodigo):
                expresion = res_expresion_ejecutar.codigo
            else:
                return RetornoError("Se produjo un error al intentar definir la 'EXPRESION' de la instrucción 'WHILE' dentro de la creación del PROCEDURE o FUNCTION.")

            for instruccion in self.lista_instrucciones:

                res_then_ejecutar = instruccion.Ejecutar(base_datos, entorno)
                if isinstance(res_then_ejecutar, RetornoCodigo):
                    instrucciones += res_then_ejecutar.codigo
                else:
                    return RetornoError("Se produjo un error al intentar definir las instrucciones de la instrucción 'WHILE' dentro de la creación del PROCEDURE o FUNCTION.")

            return RetornoCodigo("WHILE {} BEGIN\n {} END\n".format(expresion, instrucciones))

        else:

            # Variables para el retorno del If
            arreglo_mensajes = []
            arreglo_arreglos = []

            # Se obtiene la expresion
            res_expresion = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion, RetornoError):
                return res_expresion
            elif isinstance(res_expresion, RetornoLiteral):

                while res_expresion.valor == 1:

                    nuevo_entorno = TablaDeSimbolos(entorno)
                    for instruccion in self.lista_instrucciones:
                        res_instruccion_ejecutar = instruccion.Ejecutar(base_datos, nuevo_entorno)
                        if isinstance(res_instruccion_ejecutar, RetornoError):
                            arreglo_mensajes.append("ERROR: {}".format(res_instruccion_ejecutar.msg))
                        elif isinstance(res_instruccion_ejecutar, RetornoCorrecto) and res_instruccion_ejecutar.msg is not None:
                            arreglo_mensajes.append(res_instruccion_ejecutar.msg)
                        elif isinstance(res_instruccion_ejecutar, RetornoCorrecto) and res_instruccion_ejecutar.msg is None:
                            pass
                        elif isinstance(res_instruccion_ejecutar, dict):
                            arreglo_arreglos.append(res_instruccion_ejecutar)
                        elif isinstance(res_instruccion_ejecutar, RetornoLiteral):
                            return res_instruccion_ejecutar
                        else:
                            return RetornoError("Ha ocurrido un error al evaluar la instrucción While")

                    res_expresion = self.expresion.Ejecutar(base_datos, entorno)

                return RetornoMultiplesInstrucciones(arreglo_mensajes, arreglo_arreglos)
            else:
                return RetornoError("Ha ocurrido un error al evaluar la condición del While")

    def GraficarArbol(self, id_padre):
        return ""