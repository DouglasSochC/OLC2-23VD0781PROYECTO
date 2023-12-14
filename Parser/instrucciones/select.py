from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.retorno import TIPO_DATO, TIPO_TOKEN

class Select(Instruccion):

    def __init__(self, identificador: str, lista_expresiones: list):
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la tabla
        nombre_tabla = self.identificador.Ejecutar(base_datos, entorno)

        # Se almacena la tabla para poder acceder a ella desde un identificador y asi poder obtener la informacion completa de la tabla
        simbolo = Simbolo('nombre_tabla', None, TIPO_TOKEN.SELECT, nombre_tabla, None)
        entorno.agregar(simbolo)

        for expr in self.lista_expresiones:
            res = expr.Ejecutar(base_datos, entorno)

    def GraficarArbol(self, id_padre):
        return ""
