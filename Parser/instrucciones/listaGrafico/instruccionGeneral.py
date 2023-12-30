from ...abstract.instrucciones import Instruccion

class InstruccionGeneral(Instruccion):

    def __init__(self, instruccion: any):
        self.instruccion = instruccion

    def Ejecutar(self, base_datos, entorno):
        res_ejecutar_instruccion = self.instruccion.Ejecutar(base_datos, entorno)
        return res_ejecutar_instruccion

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo de instruccion y se realiza la union con el padre
        contador[0] += 1
        id_nodo_instruccion = hash("INSTRUCCION" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_instruccion, "INSTRUCCION")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_instruccion)
        result = label_encabezado + union

        # Se obtienen los nodos de la instruccion en el caso de que exista
        if self.instruccion is not None:
            result += self.instruccion.GraficarArbol(id_nodo_instruccion, contador)

        return result
