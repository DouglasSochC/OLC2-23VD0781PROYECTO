from ...abstract.expresiones import Expresion


class IdentificadorLista(Expresion):

    def __init__(self, id_nodo, expresion: list):
        self.id_nodo = id_nodo
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):
        pass

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "INSTRUCCION")
        union_raiz_encabezado = "\"{}\"->\"{}\";\n".format("INICIO", self.id_nodo)
        resultado = label_encabezado + union_raiz_encabezado

        if isinstance(self.expresion, list):
            for instruccion in self.expresion:
                label_instruccion = instruccion.GraficarArbol(self.id_nodo) 
                union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
                resultado += label_instruccion + union_hijo_izquierdo
        else:
            label_instruccion = self.expresion.GraficarArbol(self.id_nodo)
            union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
            resultado += label_instruccion + union_hijo_izquierdo
       
        return resultado