from ..abstract.instrucciones import Instruccion
from ..expresiones.accion import Accion
class Alter(Instruccion):
    def __init__(self, id_nodo, tipo, elemento, *producciones):
        self.id_nodo = id_nodo
        self.tipo = tipo
        self.elemento = elemento
        self.producciones = producciones


    def Ejecutar(self, base_datos, entorno):
        print("Alter")

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ALTER_INSTRUCTION")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", self.tipo)
        label_elemento = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "E", self.elemento)
        union_tipo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        union_elemento = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "E")
        resultado = label_encabezado + label_tipo + union_tipo + label_elemento+ union_elemento

        for produccion in self.producciones:
            if isinstance(produccion, Accion):
                label_accion = produccion.GraficarArbol(self.id_nodo)
                union_accion = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_accion + union_accion
            else:
                label_prod = produccion.GraficarArbol(self.id_nodo)
                union_prod = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_prod + union_prod
        
        return resultado