
from ..abstract.expresiones import Expresion
from ..expresiones.constrain import Constrain
class Campo_Table:
    def __init__(self, id_nodo: int, *producciones):
        self.id_nodo = id_nodo
        self.producciones = producciones

    def Ejecutar(self, tabla, arbol):
        pass

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CAMPOS_TABLE")
        if(id_padre != None):
            print('el id del padre es',id_padre)
        resultado = label_encabezado

        for produccion in self.producciones:
            if isinstance(produccion, Constrain):  # Si es la producción que tiene constrain
                label_constrain = produccion.GraficarArbol(self.id_nodo)
                union_constrain = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_constrain + union_constrain
            else:
                label_prod = produccion.GraficarArbol(self.id_nodo)
                union_prod = "\"{}\"->\"{}\";\n".format(self.id_nodo, produccion.id_nodo)
                resultado += label_prod + union_prod

        return resultado