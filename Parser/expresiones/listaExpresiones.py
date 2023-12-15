from ..abstract.expresiones import Expresion

class ListaExpresiones(Expresion):
    def __init__(self, id_nodo,  *expresiones):
        self.id_nodo = id_nodo
        self.expresiones = expresiones
        
    def agregar_expresion(self, expresion):
        self.expresiones.append(expresion)
    
    def Ejecutar(self, base_datos, entorno):
        print("Lista Expresiones")

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "LISTA_EXPRESIONES")
        resultado = label_encabezado

        for expresion in self.expresiones:
            label_expresion = expresion.GraficarArbol(self.id_nodo)
            union_expresion = "\"{}\"->\"{}\";\n".format(self.id_nodo, expresion.id_nodo)
            resultado += label_expresion + union_expresion

        return resultado