from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from ..tablas.tabla_simbolo import Simbolo
from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoLiteral, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO

class Set(Instruccion):

    def __init__(self, id_nodo: int, identificador: Identificador, expresion: Expresion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre de la variable
        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        nombre_variable = res_identificador_ejecutar['identificador']

        # Se obtiene el tipo de dato
        res_expresion_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
        if isinstance(res_expresion_ejecutar, RetornoError):
            return res_expresion_ejecutar
        expresion = res_expresion_ejecutar

        # Se verifica que no se este construyendo un procedimiento o una funcion para realizar su funcionalidad
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            if isinstance(expresion, RetornoCodigo):
                return RetornoCodigo("SET {} = {};\n".format(nombre_variable, expresion.codigo))
            else:
                return RetornoError("Ha ocurrido un error al SETEAR un literal a la variable '{}'.".format(nombre_variable))

        else:

            # Se busca el nombre de la variable en el entorno
            simbolo_variable = entorno.obtener(nombre_variable)
            if simbolo_variable is None:
                return RetornoError("La variable '{}' no ha sido instanciada antes de su uso.".format(nombre_variable))

            if isinstance(expresion, RetornoLiteral):

                if simbolo_variable.tipo_dato != expresion.tipado:
                    #aqui validamos que el tipo de dato del simbolo en la tabla de simbolos sea del mismo tipo que el que tiene la expresion, ahora validamos con el valor para los tipos especiales
                    simbolo_variable.tipo_dato = self.expresion.DominanteAsignacion(simbolo_variable.tipo_dato, expresion.tipado)
                    if(simbolo_variable.tipo_dato == TIPO_DATO.NULL):
                        return RetornoError("No se puede realizar la operacion 'SET {} = {}' debido a que no son tipos de datos similares".format(nombre_variable, expresion.valor))
                elif simbolo_variable.tipo_dato in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) and (simbolo_variable.dimension < len(expresion.valor)):
                    return RetornoError("No se puede realizar la operacion 'SET {} = {}' debido a que la cantidad de caracteres exceden lo que soporta la variable".format(nombre_variable, expresion.valor, nombre_variable))

                # Se almacena la variable en la tabla de simbolos
                simbolo_variable = Simbolo(nombre_variable, expresion.valor, simbolo_variable.tipo_dato, simbolo_variable.dimension, TIPO_ENTORNO.SENTENCIA_SSL)
                entorno.agregar(simbolo_variable)

            else:

                return RetornoError("Ha ocurrido un error al SETEAR un literal a la variable '{}'.".format(nombre_variable))

            return RetornoCorrecto()

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DECLARE")
        constr_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador + constr_tipo_dato