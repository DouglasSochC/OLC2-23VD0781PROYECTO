from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador

class Constrain(Expresion):
    def __init__(self, id_nodo: int, tipo: str, valor: any = None, referencia: any = None):
        self.id_nodo = id_nodo
        self.tipo = tipo
        self.valor = valor  # Puede ser un identificador en el caso de REFERENCES
        self.referencia = referencia  # Identificador de referencia para REFERENCES
    
    def Ejecutar(self, base_datos, entorno):
        print("Constrain")

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CONSTRAIN")
        resultado = label_encabezado

        if self.valor is not None:
            label_valor = self.valor.GraficarArbol(self.id_nodo)
            resultado += label_valor 

        if self.referencia is not None:
            label_referencia = self.referencia.GraficarArbol(self.id_nodo)
            resultado += label_referencia 

        return resultado
    