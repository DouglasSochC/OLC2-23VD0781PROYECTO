from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import TIPO_TOKEN, RetornoError

class Select_Print(Instruccion):
    def __init__(self, lista_expresiones: list):
        self.lista_expresiones = lista_expresiones
    
    def Ejecutar(self, base_datos, entorno):
        for expresion in self.lista_expresiones:
            if(expresion is not None):
                print(expresion.Ejecutar(base_datos, entorno).valor)

    def GraficarArbol(self, id_padre):
        return ""