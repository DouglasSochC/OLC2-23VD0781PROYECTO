from ..abstract.expresiones import Expresion

class Funcion_Nativa(Expresion):
    def __init__(self, id_nodo, operador: str, expresion: any):
        self.id_nodo = id_nodo
        self.operador = operador
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):
        print("Funcion_Nativa")
    
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "FUNCION NATIVA")
        label_operador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "O", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "O")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)

        resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
     

        return label_encabezado+ label_operador + union_enca_operador+ union_hijo_izquierdo  + resultado_izquierda 

     