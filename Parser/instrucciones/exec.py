from ..abstract.instrucciones import Instruccion
from ..expresiones.expresion import Expresion
from ..expresiones.identificador import Identificador
from ..abstract.retorno import RetornoError, RetornoLiteral, RetornoCorrecto, RetornoMultiplesInstrucciones
from ..tablas.tabla_simbolo import TablaDeSimbolos
from Funcionalidad.ssl import SSL

class Exec(Instruccion):

    def __init__(self, id_nodo: str, identificador: Identificador, lista_expresiones: list[Expresion]):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'EXEC' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'EXEC' dentro de la creacion de un PROCEDURE o FUNCTION")

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'EXEC', es necesario seleccionar una base de datos.")

        res_identificador_ejecutar = self.identificador.Ejecutar(base_datos, entorno)
        nombre_procedimiento = res_identificador_ejecutar['identificador']

        valores_parametros = []
        for expresion in self.lista_expresiones:
            res_expresion = expresion.Ejecutar(base_datos, entorno)
            if isinstance(res_expresion, RetornoError):
                return res_expresion
            elif isinstance(res_expresion, RetornoLiteral):
                valores_parametros.append({'valor': str(res_expresion.valor), 'tipado': res_expresion.tipado})
            else:
                return RetornoError("El valor de un parametro debe ser un literal.")

        ssl = SSL()

        # Se valida que los parametros sean correctos para ser utilizados al ejecutar el procedimiento
        validar_parametros = ssl.verificar_parametros_procedimiento_y_obtener_query(base_datos.valor, nombre_procedimiento, valores_parametros)
        if validar_parametros.success is False:
            return RetornoError(validar_parametros.valor)

        # Se obtiene el query del procedimiento
        query = validar_parametros.valor

        # Se genera un nuevo entorno para el procedimiento
        nuevo_entorno = TablaDeSimbolos(entorno, [], "EXEC")

        # Se realiza el parseo del query que tiene el procedimiento
        from Parser.parser import parse
        instrucciones = parse(query)

        # Se revisa que se haya obtenido una instrucciones
        if instrucciones is not None:

            if isinstance(instrucciones, str):
                return RetornoError("No se pudo ejecutar el procedimiento '{}' debido al siguiente error: {}.".format(nombre_procedimiento, instrucciones))
            else:

                # Variables para el retorno del If
                arreglo_mensajes = []
                arreglo_arreglos = []

                for instr in instrucciones:
                    res = instr.Ejecutar(base_datos, nuevo_entorno)
                    if isinstance(res, RetornoError):
                        arreglo_mensajes.append("ERROR: {}".format(res.msg))
                    elif isinstance(res, RetornoCorrecto) and res.msg is not None:
                        arreglo_mensajes.append(res.msg)
                    elif isinstance(res, RetornoCorrecto) and res.msg is None:
                        pass
                    elif isinstance(res, dict):
                        arreglo_arreglos.append(res)
                    elif isinstance(res, RetornoLiteral):
                        return res
                    elif isinstance(res, RetornoMultiplesInstrucciones):
                        arreglo_mensajes += res.arreglo_mensajes
                        arreglo_arreglos += res.arreglo_arreglos
                    else:
                            return RetornoError("Ha ocurrido un error al evaluar la instrucción EXEC")

                entorno.agregar_hijo(nuevo_entorno)
                return RetornoMultiplesInstrucciones(arreglo_mensajes, arreglo_arreglos)

        entorno.agregar_hijo(nuevo_entorno)
        return RetornoCorrecto("El procedimiento '{}' se ha ejecutado correctamente.".format(nombre_procedimiento))

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXEC")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_identificador

        if isinstance(self.lista_expresiones, list) and self.lista_expresiones:
            primer_elemento = self.lista_expresiones[0]
            if isinstance(primer_elemento, Expresion):
                 for campo in self.lista_expresiones:
                    label_campo = campo.GraficarArbol(self.id_nodo)
                    union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, campo.id_nodo)
                    result += label_campo + union_tipo_accion_campo
            else:
                label_tipo_dato = self.lista_expresiones.GraficarArbol(self.id_nodo)
                result += label_tipo_dato

        return result