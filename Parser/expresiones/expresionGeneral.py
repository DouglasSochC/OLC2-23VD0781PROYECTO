from ..abstract.expresiones import Expresion

class ExpresionGeneral(Expresion):
    def __init__(self, id_nodo, *listaExp):
        self.id_nodo = id_nodo
        self.listaExp = listaExp


    def Ejecutar(self, base_datos, entorno):
        print("Expresion General")

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXPRESION")
        resultado_expresion = self.listaExp.GraficarArbol(self.id_nodo)

        return label_encabezado  + resultado_expresion