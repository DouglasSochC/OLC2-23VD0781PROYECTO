from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoArreglo, RetornoLiteral, RetornoError, TIPO_DATO

class Logico(Expresion):
    def __init__(self, id_nodo, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.id_nodo = id_nodo
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
            
    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "LOGICO")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        if self.expresion_derecha is not None:
            print("NO ES NONE")
            union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)
            resultado_derecha = self.expresion_derecha.GraficarArbol(id_padre)
        else:
            union_hijo_derecho = ""
            resultado_derecha = ""
        
        

        resultado_izquierda = self.expresion_izquierda.GraficarArbol(id_padre)
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "Op", self.operador)

        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "Op")

        return label_encabezado + union_hijo_izquierdo+resultado_izquierda +label_operador+union_enca_operador+ union_hijo_derecho  + resultado_derecha
    