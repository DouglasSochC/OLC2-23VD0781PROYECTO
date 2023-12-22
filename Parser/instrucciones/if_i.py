from ..abstract.instrucciones import Instruccion
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoLiteral, RetornoCorrecto
from ..tablas.tabla_simbolo import TablaDeSimbolos

class If_I(Instruccion):

    def __init__(self, id_nodo: str, expresion: Expresion, instrucciones_then: list, instrucciones_else: list):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.instrucciones_then = instrucciones_then
        self.instrucciones_else = instrucciones_else

    # TODO: Se debe verificar que si se esta ejecutando unicamente para analizar la semantica o para ejecutar su funcionalidad
    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            RetornoCodigo("If")

        else:

            # Se obtiene la expresion
            res_expresion = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion, RetornoError):
                return res_expresion
            elif isinstance(res_expresion, RetornoLiteral):

                # Se realiza las instrucciones THEN del IF
                if res_expresion.valor == 1:
                    nuevo_entorno = TablaDeSimbolos(entorno)
                    for instruccion in self.instrucciones_then:
                        res_instruccion_ejecutar = instruccion.Ejecutar(base_datos, nuevo_entorno)
                        print("INSTRUCCIONES THEN: ", res_instruccion_ejecutar)

                # Se realiza las instrucciones ELSE del IF
                else:

                    if self.instrucciones_else is None:
                        return None

                    nuevo_entorno = TablaDeSimbolos(entorno)
                    for instruccion in self.instrucciones_else:
                        res_instruccion_ejecutar = instruccion.Ejecutar(base_datos, nuevo_entorno)
                        print("INSTRUCCIONES ELSE: ",res_instruccion_ejecutar)

                return RetornoCorrecto()
            else:
                return RetornoError("Ha ocurrido un error al evaluar la instrucción If")

    def GraficarArbol(self, id_padre):
        return ""