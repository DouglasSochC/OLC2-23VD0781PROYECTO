from ..abstract.expresiones import Expresion
from ..expresiones.listasGrafico.expresionGenera import ExpresionGeneral
class Asignacion(Expresion):
    def __init__(self, id_nodo, accion:str, expresion:any):
        self.id_nodo = id_nodo
        self.accion = accion
        self.expresion = expresion


    def Ejecutar(self, base_datos, entorno):
        print("Asignacion")

    def GraficarArbol(self, id_padre):
       
        
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ASIGNACION")
         
        
        return label_encabezado
