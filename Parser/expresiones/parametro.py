from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato

class Parametro(Expresion):

    def __init__(self, id_nodo, identificador: Identificador, tipo_dato: Tipo_Dato):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.tipo_dato = tipo_dato

    def Ejecutar(self, base_datos, entorno):

        respuesta = {}

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        respuesta.update({'name': res_identificador['identificador']})

        # Se obtiene la informacion del tipo de dato
        res_tipo_dato = self.tipo_dato.Ejecutar(base_datos, entorno)
        respuesta.update({"type": res_tipo_dato['representacion']})

        if res_tipo_dato['dimension'] >= 0:
            respuesta.update({"length": res_tipo_dato['dimension']})

        return respuesta

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "PARAMETRO")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        label_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_identificador + label_tipo_dato
        return result