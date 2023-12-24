from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoArreglo, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..expresiones.expresion import Expresion as Expresion_E

class Condicion(Expresion):

    def __init__(self, id_nodo: str, expresion_izquierda: Expresion_E, tipo_operador: str, expresion_derecha: Expresion_E):
        self.id_nodo = id_nodo
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

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CONDICION")
        label_expresion_izquierda = self.expresion_izquierda.GraficarArbol(self.id_nodo)
        union_encabezado_expresion_izquierda = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion_izquierda.id_nodo)
       
        if self.tipo_operador is None and self.expresion_derecha is None:
            return label_encabezado + label_expresion_izquierda + union_encabezado_expresion_izquierda

        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "1", self.tipo_operador)
        union_encabezado_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "1")
        label_expresion_derecha = self.expresion_derecha.GraficarArbol(self.id_nodo)
        label_union_encabezado_expresion_derecha = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion_derecha.id_nodo)

        return label_encabezado + label_expresion_izquierda + union_encabezado_expresion_izquierda + label_operador + union_encabezado_operador + label_expresion_derecha + label_union_encabezado_expresion_derecha
