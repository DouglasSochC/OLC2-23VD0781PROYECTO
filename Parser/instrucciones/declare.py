from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.retorno import RetornoError

class Declare(Instruccion):

    def __init__(self, id_nodo: int, identificador: Identificador, tipo_dato: Tipo_Dato):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.tipo_dato = tipo_dato

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador_ejecutar, RetornoError):
            return res_identificador_ejecutar.msg
        nombre_variable = res_identificador_ejecutar.identificador

        # Se verifica que no exista la variable en un entorno
        obtener_simbolo = entorno.obtener(nombre_variable)
        if obtener_simbolo is not None:
            return "ERROR: La variable con nombre '{}' ya ha sido instanciada.".format(nombre_variable)

        # Se obtiene el tipo de dato
        res_tipo_dato_ejecutar = self.tipo_dato.Ejecutar(base_datos, entorno)
        if isinstance(res_tipo_dato_ejecutar, RetornoError):
            return res_tipo_dato_ejecutar.msg
        tipo_dato = res_tipo_dato_ejecutar

        # Se almacena la variable en la tabla de simbolos
        simbolo_variable = Simbolo(nombre_variable, "", tipo_dato['tipo_dato'], tipo_dato['dimension'], None)
        entorno.agregar(simbolo_variable)

        return None

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DECLARE")
        constr_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador + constr_tipo_dato