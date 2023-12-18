from ..abstract.expresiones import Expresion

class Asignacion(Expresion):
    def __init__(self, id_nodo, identificador, expresion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.expresion = expresion 
        pass

    def Ejecutar(self, base_datos, entorno):
        print("ASIGNACION")

    def GraficarArbol(self, id_padre):
        print("GRAFICAR -> ASIGNASION")