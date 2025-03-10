from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoCodigo

class Declare(Instruccion):

    def __init__(self, identificador: Identificador, tipo_dato: Tipo_Dato):
        self.identificador = identificador
        self.tipo_dato = tipo_dato

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        nombre_variable = res_identificador_ejecutar['identificador']

        # Se verifica que no exista la variable en un entorno
        obtener_simbolo = entorno.obtener(nombre_variable)
        if obtener_simbolo is not None:
            return RetornoError("La variable con nombre '{}' ya ha sido instanciada.".format(nombre_variable))

        # Se obtiene el tipo de dato
        res_tipo_dato_ejecutar = self.tipo_dato.Ejecutar(base_datos, entorno)
        tipo_dato = res_tipo_dato_ejecutar

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            if tipo_dato['dimension'] == -1:
                return RetornoCodigo("DECLARE {} {};\n".format(nombre_variable, tipo_dato['representacion']))
            else:
                return RetornoCodigo("DECLARE {} {}({});\n".format(nombre_variable, tipo_dato['representacion'], tipo_dato['dimension']))

        else:

            # Se almacena la variable en la tabla de simbolos
            simbolo_variable = Simbolo(nombre_variable, "", tipo_dato['tipo_dato'], tipo_dato['dimension'], None)
            entorno.agregar(simbolo_variable)

            return RetornoCorrecto()

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_declare = hash("DECLARE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_declare, "DECLARE")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_declare)
        result = label_encabezado + union

        # Se obtienen los nodos hijos que son el tipo de dato y el identificador
        result += self.identificador.GraficarArbol(id_nodo_declare, contador)
        result += self.tipo_dato.GraficarArbol(id_nodo_declare, contador)

        return result
