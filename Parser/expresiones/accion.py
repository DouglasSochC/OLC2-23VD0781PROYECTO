from ..abstract.expresiones import Expresion
from ..expresiones.campo_table import Campo_Table

class Accion(Expresion):
    def __init__(self, id_nodo, tipo, elemento, *producciones):
        self.id_nodo = id_nodo
        self.tipo = tipo
        self.elemento = elemento
        self.producciones = producciones

    def Ejecutar(self, base_datos, entorno):
        print("Accion")

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ACCION")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", self.tipo)
        label_elemento = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "E", self.elemento)
        union_tipo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        union_elemento = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "E")
        resultado = label_encabezado + label_tipo + union_tipo + label_elemento+ union_elemento

        for produccion in self.producciones:
            if isinstance(produccion, Campo_Table):  # Si es la producción que tiene constrain
                label_constrain = produccion.GraficarArbol(self.id_nodo)
                union_constrain = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_constrain + union_constrain
            else:
                label_prod = produccion.GraficarArbol(self.id_nodo)
                union_prod = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_prod + union_prod
        
        return resultado