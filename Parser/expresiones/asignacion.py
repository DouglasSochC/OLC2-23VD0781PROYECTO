from ..abstract.expresiones import Expresion

class Asignacion(Expresion):
    def __init__(self, id_nodo ,expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):
        print("Asignacion")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        label_exp_izq = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "AIZQ", self.expresion_izquierda)
        union_enca_exp_izq = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "AIZQ")
        
        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "op", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "op")
        resultado_exp = ""
       

        if isinstance(self.expresion_derecha, list):
            print("es lista")
            for exp in self.expresion_derecha:
                union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, exp.id_nodo)
                resultado_izquierda = exp.GraficarArbol(self.id_nodo)
                resultado_exp += union_hijo_izquierdo + resultado_izquierda
        else:
            union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion_derecha.id_nodo)
            resultado_izquierda = self.expresion_derecha.GraficarArbol(self.id_nodo)
            resultado_exp += union_hijo_izquierdo + resultado_izquierda
      
      
        return label_encabezado+ label_exp_izq+union_enca_exp_izq +label_operador + union_enca_operador+ resultado_exp


   