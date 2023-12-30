from ..abstract.expresiones import Expresion
from ..expresiones.expresion import Expresion as Expresion_Normal
from ..abstract.retorno import RetornoLiteral, RetornoError, TIPO_DATO

class Logico(Expresion):

    def __init__(self, expresion_izquierda: Expresion_Normal, operador: str, expresion_derecha: Expresion_Normal):
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):
        if(self.expresion_izquierda != None):
            exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
            if isinstance(exp_izq, RetornoError):
                return exp_izq
        if(self.expresion_derecha != None):
            exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)
            if isinstance(exp_der, RetornoError):
                return exp_der
        ret = None
        if self.operador == "&&":
            print("AND")
            if((exp_izq.tipado == TIPO_DATO.BIT)and(exp_der.tipado == TIPO_DATO.BIT)):
                ret = exp_izq.valor and exp_der.valor
            else:
                return RetornoError("ERROR EN LA OPERACION LOGICA &&")
        elif self.operador == "||":
            print("OR")
            if((exp_izq.tipado == TIPO_DATO.BIT)and(exp_der.tipado == TIPO_DATO.BIT)):
                ret = exp_izq.valor or exp_der.valor
            else:
                return RetornoError("ERROR EN LA OPERACION LOGICA ||")
        elif self.operador == "!":
            print("NOT")
            if(exp_der.tipado == TIPO_DATO.BIT):
                ret = not exp_der.valor
                if(ret):
                    ret = 1
                else:
                    ret = 0
            else:
                return RetornoError("ERROR EN LA OPERACION LOGICA !")
        return RetornoLiteral(ret, TIPO_DATO.BIT, None)

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_logico = hash("LOGICO" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_logico, "LOGICO")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_logico)
        result = label_encabezado + union

        # Se crea el nodo de la expresion izquierda y se une con el nodo de logico
        result += self.expresion_izquierda.GraficarArbol(id_nodo_logico, contador)

        # Se crea el nodo del operador y se une con el nodo de logico
        contador[0] += 1
        id_nodo_operador = hash("OPERADOR" + str(contador[0]))
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_operador, self.operador)
        union_operador = "\"{}\"->\"{}\";\n".format(id_nodo_logico, id_nodo_operador)
        result += label_operador + union_operador

        # Se crea el nodo de la expresion derecha y se une con el nodo de logico
        result += self.expresion_derecha.GraficarArbol(id_nodo_logico, contador)

        return result
