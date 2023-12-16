from ..abstract.expresiones import Expresion

class Asignacion(Expresion):
    def __init__(self, id_nodo ,expresion_izquierda: any, operador: str, expresion_derecha: any):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):
        print("Asignacion")

    def GraficarArbol(self, id_padre):
        pass