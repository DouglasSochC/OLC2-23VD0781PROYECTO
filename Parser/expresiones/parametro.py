from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato

class Parametro(Expresion):

    def __init__(self, identificador: Identificador, tipo_dato: Tipo_Dato):
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

    def GraficarArbol(self,  id_nodo_padre: int, contador: list):
        contador[0] += 1
        id_nodo_parametro = hash("PARAMETROS" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_parametro, "PARAMETROS")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_parametro)
        result = label_encabezado + union


        result += self.identificador.GraficarArbol(id_nodo_parametro, contador)

        result += self.tipo_dato.GraficarArbol(id_nodo_parametro, contador)

        return result