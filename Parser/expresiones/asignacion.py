from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from ..abstract.retorno import RetornoError, RetornoAsignacion

class Asignacion(Expresion):

    def __init__(self, id_nodo, identificador: Identificador, expresion: Expresion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador_ejecutar, RetornoError):
            return res_identificador_ejecutar.msg
        nombre = res_identificador_ejecutar.identificador

        # Se obtiene la expresion
        res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        if isinstance(res_expresion_ejecutar, RetornoError):
            return res_expresion_ejecutar.msg

        return RetornoAsignacion(nombre, res_expresion_ejecutar)

    # TODO: Corregir el graficado del arbol debido a que se han modificado los parametros que se solicitan en la asignacion
    def GraficarArbol(self, id_padre):
        return ""
        # label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        # label_exp_izq = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "AIZQ", self.expresion_izquierda)
        # union_enca_exp_izq = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "AIZQ")

        # label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "op", self.operador)
        # union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "op")
        # resultado_exp = ""

        # if isinstance(self.expresion, list):
        #     print("es lista")
        #     for exp in self.expresion:
        #         union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
        #         resultado_izquierda = exp.GraficarArbol(self.id_nodo)
        #         resultado_exp += union_hijo_izquierdo + resultado_izquierda
        # else:
        #     union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        #     resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
        #     resultado_exp += union_hijo_izquierdo + resultado_izquierda

        # return label_encabezado+ label_exp_izq+union_enca_exp_izq +label_operador + union_enca_operador+ resultado_exp
