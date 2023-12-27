from ..abstract.instrucciones import Instruccion
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoLiteral, RetornoCorrecto, RetornoMultiplesInstrucciones
from ..tablas.tabla_simbolo import TablaDeSimbolos

class If_I(Instruccion):

    def __init__(self, id_nodo: str, expresion: Expresion, instrucciones_then: list, instrucciones_else: list):
        self.id_nodo = id_nodo
        self.expresion = expresion
        self.instrucciones_then = instrucciones_then
        self.instrucciones_else = instrucciones_else

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            # Variables
            expresion = ""
            sentencia_then = ""
            sentencia_else = ""

            res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion_ejecutar, RetornoCodigo):
                expresion = res_expresion_ejecutar.codigo
            else:
                return RetornoError("Se produjo un error al intentar definir la 'EXPRESION' de la instrucción 'IF' dentro de la creación del PROCEDURE o FUNCTION.")

            for then_ in self.instrucciones_then:

                res_then_ejecutar = then_.Ejecutar(base_datos, entorno)
                if isinstance(res_then_ejecutar, RetornoCodigo):
                    sentencia_then += res_then_ejecutar.codigo
                else:
                    return RetornoError("Se produjo un error al intentar definir la sentencia 'THEN' de la instrucción 'IF' dentro de la creación del PROCEDURE o FUNCTION.")

            if self.instrucciones_else is not None:

                for else_ in self.instrucciones_else:

                        res_else_ejecutar = else_.Ejecutar(base_datos, entorno)
                        if isinstance(res_else_ejecutar, RetornoCodigo):
                            sentencia_else += res_else_ejecutar.codigo
                        else:
                            return RetornoError("Se produjo un error al intentar definir la sentencia 'ELSE' de la instrucción 'IF' dentro de la creación del PROCEDURE o FUNCTION.")

            if sentencia_else == "":
                return RetornoCodigo("IF {} THEN\n{}END IF;\n".format(expresion, sentencia_then))
            else:
                return RetornoCodigo("IF {} THEN\n{}ELSE\n{}END IF;\n".format(expresion, sentencia_then, sentencia_else))

        else:

            # Variables para el retorno del If
            arreglo_mensajes = []
            arreglo_arreglos = []
            nuevo_entorno = None

            # Se obtiene la expresion
            res_expresion = self.expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion, RetornoError):
                return res_expresion
            elif isinstance(res_expresion, RetornoLiteral):

                # Se realiza las instrucciones THEN del IF
                if res_expresion.valor == 1:
                    nuevo_entorno = TablaDeSimbolos(entorno, [], "IF-THEN")
                    for instruccion in self.instrucciones_then:
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
                        elif isinstance(res_instruccion_ejecutar, RetornoMultiplesInstrucciones):
                            arreglo_mensajes += res_instruccion_ejecutar.arreglo_mensajes
                            arreglo_arreglos += res_instruccion_ejecutar.arreglo_arreglos
                        else:
                            return RetornoError("Ha ocurrido un error al evaluar la instrucción If-Then")

                # Se realiza las instrucciones ELSE del IF
                else:

                    if self.instrucciones_else is None:
                        return None

                    nuevo_entorno = TablaDeSimbolos(entorno, [], "IF-ELSE")
                    nuevo_entorno.realizado_en = "IF-ELSE"
                    for instruccion in self.instrucciones_else:
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
                        elif isinstance(res_instruccion_ejecutar, RetornoMultiplesInstrucciones):
                            arreglo_mensajes += res_instruccion_ejecutar.arreglo_mensajes
                            arreglo_arreglos += res_instruccion_ejecutar.arreglo_arreglos
                        else:
                            return RetornoError("Ha ocurrido un error al evaluar la instrucción If-Else")

                if nuevo_entorno is not None:
                    entorno.agregar_hijo(nuevo_entorno)
                return RetornoMultiplesInstrucciones(arreglo_mensajes, arreglo_arreglos)
            else:
                return RetornoError("Ha ocurrido un error al evaluar la instrucción If")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "IF")
        label_expresion = self.expresion.GraficarArbol(self.id_nodo)
        union_encabezado_expresion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        result = label_encabezado + label_expresion + union_encabezado_expresion

        # Se grafica instrucciones_list
        if self.instrucciones_then is not None:
            for instruccion in self.instrucciones_then:
                instrucciones_then = instruccion.GraficarArbol(self.id_nodo)
                union_encabezado_instruccion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, instruccion.id_nodo)
                result += instrucciones_then + union_encabezado_instruccion

        # Se grafica instrucciones_else
        if self.instrucciones_else is not None:
            for instruccion in self.instrucciones_else:
                instrucciones_else = instruccion.GraficarArbol(self.id_nodo)
                union_encabezado_instruccion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, instruccion.id_nodo)
                result += instrucciones_else + union_encabezado_instruccion

        return result
