from ...abstract.instrucciones import Instruccion
from ..listaGrafico.instruccionGeneral import InstruccionGeneral

class InstruccionesLista(Instruccion):

    def __init__(self, id_nodo: int, instrucciones: list[InstruccionGeneral]):
        self.id_nodo = id_nodo
        self.instrucciones = instrucciones
       

    def Ejecutar(self, base_datos, entorno):
        pass
    def GraficarArbol(self, id_padre):
        label_inicio = "\"{}\"[label=\"{}\"];\n".format("0INICIO", "INICIO")
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "INSTRUCCIONES")
        union_root = "\"{}\"->\"{}\";\n".format("0INICIO", self.id_nodo)
        resultado = label_encabezado + union_root + label_inicio
        if self.instrucciones is not None:
            if isinstance(self.instrucciones, list):
                for instr in self.instrucciones:
                    resultado += instr.GraficarArbol(self.id_nodo)
                    union = "\"{}\" -> \"{}\";\n".format(self.id_nodo, instr.id_nodo)
                    resultado += union
            else:
                resultado += self.instrucciones.GraficarArbol(self.id_nodo)
                union = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.instrucciones.id_nodo)
                resultado += union
                
        return resultado