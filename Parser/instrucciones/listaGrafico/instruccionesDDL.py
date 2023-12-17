from ...abstract.instrucciones import Instruccion

class InstruccionDDL(Instruccion):
    def __init__(self, id_nodo, *listaIns):
        self.id_nodo = id_nodo
        self.listaIns = listaIns
       

    def Ejecutar(self, base_datos, entorno):
        pass

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "SENTENCIA DDL")
      
        resultado = label_encabezado 
        for parametro in self.listaIns:
            label_parametro = parametro.GraficarArbol(self.id_nodo)
            union_parametro = "\"{}\"->\"{}\";\n".format(self.id_nodo, parametro.id_nodo)
            resultado += label_parametro + union_parametro
        

        return resultado   