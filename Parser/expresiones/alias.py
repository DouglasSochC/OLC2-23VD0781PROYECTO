from ..abstract.expresiones import Expresion

class Alias(Expresion):
    def __init__(self, id_nodo ,expresion_izquierda: any, operador: str, identificador: any= None):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.identificador = identificador 

    def Ejecutar(self, base_datos, entorno):
        print("Logico")

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "ALIAS")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)

        
        resultado_izquierda = self.expresion_izquierda.GraficarArbol(id_padre)
        
        if(self.operador.lower() != "as"):
            label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "as", self.operador)
            union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "as")
            return label_encabezado + union_hijo_izquierdo+resultado_izquierda +label_operador+union_enca_operador

        else:
            label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "al", self.operador)
            union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "al")
            label_operador2 = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "I", self.identificador)
            union_enca_operador2 = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "I")
            return label_encabezado + union_hijo_izquierdo+resultado_izquierda +label_operador+union_enca_operador + label_operador2 + union_enca_operador2
    

   