from ..abstract.instrucciones import Instruccion

class Use(Instruccion):
    def __init__(self, id_nodo: int,  identificador: any):
        self.id_nodo = id_nodo
        self.identificador = identificador
        pass

    def Ejecutar(self, base_datos, entorno):
        base_datos.valor = "bd1"
    
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "USE")
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador