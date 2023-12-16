from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoIdentificador, RetornoLiteral, RetornoError, TIPO_DATO

class Logico(Expresion):
    def __init__(self, id_nodo, expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoError):
            return exp_izq
        elif isinstance(exp_der, RetornoError):
            return exp_der

        if self.operador == "&&":
            if isinstance(exp_izq, RetornoIdentificador) and isinstance(exp_der, RetornoIdentificador):
                for indice, diccionario in enumerate(exp_izq.lista):

                    diccionario['temporal'] = diccionario['temporal'] and exp_der.lista[indice]['temporal']

                return RetornoIdentificador(exp_izq.identificador, TIPO_DATO.BOOLEAN, exp_izq.lista)
            
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
    