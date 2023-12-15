from ..abstract.instrucciones import Instruccion

class Exec(Instruccion):
    def __init__(self, id_nodo, objeto , identificador, * parametros):
        self.id_nodo = id_nodo
        self.objeto = objeto
        self.identificador = identificador
        self.parametros = parametros


    def Ejecutar(self, base_datos, entorno):
        print("Exec")
    
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "LLAMADA_PROCEDURE")
        label_objeto = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "EX", self.objeto)
        union_objeto = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "EX")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        union_identificador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.identificador.id_nodo)

        for parametro in self.parametros:
            label_parametro = parametro.GraficarArbol(self.id_nodo)
            union_parametro = "\"{}\"->\"{}\";\n".format(self.id_nodo, parametro.id_nodo)
            label_identificador += label_parametro + union_parametro


        return label_encabezado + label_objeto + union_objeto+ label_identificador + union_identificador  