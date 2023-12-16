from ..abstract.expresiones import Expresion

class ListaExpresiones(Expresion):
    def __init__(self,id_nodo, *expresiones):
        self.id_nodo = id_nodo
        self.expresiones = expresiones

    
    def Ejecutar(self, base_datos, entorno):
        print("Insert")

    def GraficarArbol(self, id_padre=None):
        id_nodo_actual = self.id_nodo or (id_padre + "_ListaExpresiones" if id_padre is not None else "ListaExpresiones")

        label_lista_expresiones = "\"{}\"[label=\"ListaExpresiones\"];\n".format(id_nodo_actual)
        
        union_hijo = ""

        for i, expresion in enumerate(self.expresiones):
            union_hijo += "\"{}\"->\"{}\";\n".format(id_nodo_actual, expresion.GraficarArbol(id_nodo_actual + f"_exp{i + 1}"))

        return label_lista_expresiones + union_hijo