from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoArreglo, TIPO_DATO, TIPO_ENTORNO
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
            res_exp_izq_ejecutar = self.expresion_izquierda.Ejecutar(base_datos, entorno)
            if isinstance(res_exp_izq_ejecutar, RetornoError):
                return res_exp_izq_ejecutar
            elif isinstance(res_exp_izq_ejecutar, RetornoArreglo):

                nuevo_entorno = TablaDeSimbolos(entorno)

                # Se crea un nuevo simbolo de datos debido que a traves del mismo se podra realizar operaciones relacionales, aritmeticas y de asignacion a la expresion derecha
                simbolo_condicion = Simbolo("condicion", res_exp_izq_ejecutar.lista, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
                nuevo_entorno.agregar(simbolo_condicion)

                # Se ejecuta la expresion derecha y esta contendra todos los indices y la informacion que servira para hacer el 'SELECT'
                res_exp_der_ejecutar = self.expresion_derecha.Ejecutar(base_datos, nuevo_entorno)
                return res_exp_der_ejecutar
            else:
                RetornoError("Ha ocurrido un error al ejecutar la condicion.")

    def GraficarArbol(self, id_padre):
        return ""
