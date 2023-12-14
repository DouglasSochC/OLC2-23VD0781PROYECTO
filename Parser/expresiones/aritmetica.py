from ..abstract.expresiones import Expresion

class Aritmetica(Expresion):
    def __init__(self, expresion_izq: any, operador: str, expresion_der: any):
        self.expresion_izq = expresion_izq
        self.operador = operador
        self.expresion_der = expresion_der

    def Ejecutar(self, base_datos, entorno):

        self.expresion_izq.Ejecutar(base_datos, entorno)
        self.expresion_der.Ejecutar(base_datos, entorno)

        return (self.expresion_izq, self.operador, self.expresion_der)

    def GraficarArbol(self, id_padre):
        return ""