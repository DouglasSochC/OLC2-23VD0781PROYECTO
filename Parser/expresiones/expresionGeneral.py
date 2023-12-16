from ..abstract.expresiones import Expresion

class ExpresionGeneral(Expresion):
    def __init__(self, id_nodo, *listaExp):
        self.id_nodo = id_nodo
        self.listaExp = listaExp


    def Ejecutar(self, base_datos, entorno):
        print("Expresion General")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXPRESION")
      
        resultado = label_encabezado 
        for parametro in self.listaExp:
            label_parametro = parametro.GraficarArbol(self.id_nodo)
            union_parametro = "\"{}\"->\"{}\";\n".format(self.id_nodo, parametro.id_nodo)
            resultado += label_parametro + union_parametro
        

        return resultado   