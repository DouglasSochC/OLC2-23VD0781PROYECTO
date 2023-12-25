from ...abstract.instrucciones import Instruccion

class InstruccionGeneral(Instruccion):

    def __init__(self, id_nodo: str, instruccion: any):
        self.id_nodo = id_nodo
        self.instruccion = instruccion

    def Ejecutar(self, base_datos, entorno):
        res_ejecutar_instruccion = self.instruccion.Ejecutar(base_datos, entorno)
        return res_ejecutar_instruccion

    def GraficarArbol(self, id_padre):
        label_inicio = "\"{}\"[label=\"{}\"];\n".format("0INICIO", "INICIO")
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "INSTRUCCION")
        union_root = "\"{}\"->\"{}\";\n".format("0INICIO", self.id_nodo)
        result = label_encabezado + union_root + label_inicio
        if self.instruccion is not None:
            label_instruccion = self.instruccion.GraficarArbol(self.id_nodo)
            union_instruccion_encabezado = "\"{}\"->\"{}\"\n".format(self.id_nodo, self.instruccion.id_nodo)
            result += label_instruccion + union_instruccion_encabezado
        return result