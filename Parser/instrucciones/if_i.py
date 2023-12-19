from ..abstract.instrucciones import Instruccion
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoRelacional, RetornoAsignacion
from ..tablas.tabla_simbolo import TablaDeSimbolos

class If_I(Instruccion):

    def __init__(self, id_nodo: str, expresion: Expresion, instrucciones_then: list, instrucciones_else: list):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.instrucciones_then = instrucciones_then
        self.instrucciones_else = instrucciones_else

    # TODO: Se debe verificar que si se esta ejecutando unicamente para analizar la semantica o para ejecutar su funcionalidad
    def Ejecutar(self, base_datos, entorno):

        # Se verifica a traves de una variable en la tabla de simbolos si se esta realizando el IF como instruccion o como un DDL en el CREATE
        se_ejecuta = entorno.obtener('uso_en_crear')

        # Esta utilizando el IF para un CREATE
        if se_ejecuta is not None:
            # Se tiene que analizar la realizacion de este
            print("CREATE")

        # Esta utilizando el IF para evaluar
        else:

            # Se obtiene la expresion
            res_expresion = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion, RetornoError):
                return res_expresion.msg

            if isinstance(res_expresion, RetornoRelacional):

                obtener_valor_en_ts = entorno.obtener(res_expresion.operacion_izquierda)
                obtener_valor_en_ts.valor

                # Se realiza la operacion relacional
                if eval(f"obtener_valor_en_ts.valor {res_expresion.operador} res_expresion.operacion_derecha"):

                    print("SE HACE EL THEN")
                    nuevo_entorno = TablaDeSimbolos(entorno)
                    for instruccion in self.instrucciones_then:
                        res_instruccion_ejecutar = instruccion.Ejecutar(base_datos, nuevo_entorno)
                        print(res_instruccion_ejecutar)

                else:

                    if self.instrucciones_else is None:
                        return None

                    print("SE HACE EL ELSE")
                    # Se realiza las instrucciones que hay en el ELSE
                    nuevo_entorno = TablaDeSimbolos(entorno)
                    for instruccion in self.instrucciones_else:
                        res_instruccion_ejecutar = instruccion.Ejecutar(base_datos, nuevo_entorno)
                        print(res_instruccion_ejecutar)

            elif isinstance(res_expresion, RetornoAsignacion):
                return "ERROR: Se ha utilizado el operador de asignación (=) en lugar del operador de comparación (==) en la condición if."
            else:
                return "ERROR: Ha ocurrido un error al evaluar la instrucción If"


    def GraficarArbol(self, id_padre):
        return ""