from ..abstract.expresiones import Expresion

class Campo_Table(Expresion):
    def __init__(self):
        pass

    def Ejecutar(self, base_datos, entorno):
        print("Campo_Table")