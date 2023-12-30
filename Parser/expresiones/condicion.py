from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoArreglo, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..expresiones.expresion import Expresion as Expresion_Normal

class Condicion(Expresion):

    def __init__(self, expresion_izquierda: Expresion_Normal, tipo_operador: str, expresion_derecha: Expresion_Normal):
        self.expresion_izquierda = expresion_izquierda
        self.tipo_operador = tipo_operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        if self.tipo_operador is None and self.expresion_derecha is None:
            res_exp_izq_ejecutar = self.expresion_izquierda.Ejecutar(base_datos, entorno)
            return res_exp_izq_ejecutar
        else:

            # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
            construccion = entorno.obtener("construir_procedimiento")
            construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
            if construccion is not None:

                codigo_izquierdo = ""
                codigo_derecho = ""
                res_exp_izq_ejecutar = self.expresion_izquierda.Ejecutar(base_datos, entorno)
                if isinstance(res_exp_izq_ejecutar, RetornoError):
                    return res_exp_izq_ejecutar
                elif isinstance(res_exp_izq_ejecutar, RetornoCodigo):
                    codigo_izquierdo = res_exp_izq_ejecutar.codigo
                else:
                    return RetornoError("Ha ocurrido un error al definir el codigo de la condicion")

                res_exp_der_ejecutar = self.expresion_derecha.Ejecutar(base_datos, entorno)
                if isinstance(res_exp_der_ejecutar, RetornoError):
                    return res_exp_der_ejecutar
                elif isinstance(res_exp_der_ejecutar, RetornoCodigo):
                    codigo_derecho = res_exp_der_ejecutar.codigo
                else:
                    return RetornoError("Ha ocurrido un error al definir el codigo de la condicion")

                return RetornoCodigo("{} {} {}".format(codigo_izquierdo, self.tipo_operador, codigo_derecho))

            else:

                res_exp_izq_ejecutar = self.expresion_izquierda.Ejecutar(base_datos, entorno)
                if isinstance(res_exp_izq_ejecutar, RetornoError):
                    return res_exp_izq_ejecutar
                elif isinstance(res_exp_izq_ejecutar, RetornoArreglo):

                    # Se crea un nuevo entorno debido que a traves del mismo se podra realizar operaciones relacionales, aritmeticas y de asignacion a la expresion derecha
                    nuevo_entorno = TablaDeSimbolos(entorno)

                    # Se crea un nuevo simbolo de datos
                    simbolo_condicion = Simbolo("condicion", res_exp_izq_ejecutar, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
                    nuevo_entorno.agregar(simbolo_condicion)

                    # Se ejecuta la expresion derecha y esta contendra todos los indices y la informacion que servira para hacer el 'SELECT'
                    res_exp_der_ejecutar = self.expresion_derecha.Ejecutar(base_datos, nuevo_entorno)
                    return res_exp_der_ejecutar
                else:
                    RetornoError("Ha ocurrido un error al ejecutar la condicion.")

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_condicion = hash("CONDICION" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_condicion, "CONDICION")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_condicion)
        result = label_encabezado + union

        # Se crea el nodo de la expresion izquierda y se une con el nodo de condicion
        result += self.expresion_izquierda.GraficarArbol(id_nodo_condicion, contador)

        if self.expresion_derecha is not None:

            # Se crea el nodo del operador y se une con el nodo de condicion
            contador[0] += 1
            id_nodo_operador = hash("OPERADOR" + str(contador[0]))
            label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_operador, self.tipo_operador)
            union_operador = "\"{}\"->\"{}\";\n".format(id_nodo_condicion, id_nodo_operador)
            result += label_operador + union_operador

            # Se crea el nodo de la expresion derecha y se une con el nodo de condicion
            result += self.expresion_derecha.GraficarArbol(id_nodo_condicion, contador)

        return result
