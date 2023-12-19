from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoLiteral, TIPO_DATO, TIPO_ENTORNO

class Set(Instruccion):

    def __init__(self, id_nodo: int, identificador: Identificador, expresion: Expresion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador_ejecutar, RetornoError):
            return res_identificador_ejecutar.msg
        nombre_variable = res_identificador_ejecutar.identificador

        # Se obtiene el tipo de dato
        res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        if isinstance(res_expresion_ejecutar, RetornoError):
            return res_expresion_ejecutar.msg
        expresion = res_expresion_ejecutar

        # Se busca el nombre de la variable en el entorno
        simbolo_variable = entorno.obtener(nombre_variable)
        if simbolo_variable is None:
            return "ERROR: La variable '{}' no ha sido instanciada antes de su uso.".format(nombre_variable)

        if isinstance(expresion, RetornoLiteral):

            if simbolo_variable.tipo_dato != expresion.tipado:
                return "ERROR: No se puede realizar la operacion 'SET {} = {}' debido a que no son tipos de datos similares".format(nombre_variable, expresion.valor)
            elif simbolo_variable.tipo_dato in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) and (simbolo_variable.dimension < len(expresion.valor)):
                return "ERROR: No se puede realizar la operacion 'SET {} = {}' debido a que la cantidad de caracteres exceden lo que soporta la variable".format(nombre_variable, expresion.valor, nombre_variable)

            # Se almacena la variable en la tabla de simbolos
            simbolo_variable = Simbolo(nombre_variable, expresion.valor, simbolo_variable.tipo_dato, simbolo_variable.dimension, TIPO_ENTORNO.SENTENCIA_SSL)
            entorno.agregar(simbolo_variable)

        else:

            return "ERROR: Ha ocurrido un error al SETEAR un literal a la variable '{}'.".format(nombre_variable)

        return None

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DECLARE")
        constr_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador + constr_tipo_dato