from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto, RetornoCodigo, TIPO_DATO, TIPO_ENTORNO
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..expresiones.identificador import Identificador
from ..expresiones.condicion import Condicion
from ..expresiones.expresion import Expresion
from Funcionalidad.dml import DML

class Update(Instruccion):

    def __init__(self, identificador: Identificador, lista_expresiones: list[Expresion], condicion: Condicion):
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones
        self.condicion = condicion

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'UPDATE', es necesario seleccionar una base de datos.")

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        # Se verifica que no se este utilizando el comando 'UPDATE' dentro de la creacion de una funcion
        construir_funcion = entorno.obtener("construir_funcion")
        if construir_funcion is not None:
            return RetornoError("No es posible realizar una instrucción 'UPDATE' dentro del cuerpo del FUNCTION.")

        # Se verifica si el comando 'UPDATE' esta siendo utilizado en la creacion de un procedimiento
        construir_procedimiento = entorno.obtener("construir_procedimiento")
        if construir_procedimiento is not None:

            expresiones = []
            for expresion in self.lista_expresiones:

                # En el caso que ocurra un error al obtener el listado de expresiones
                res_expresion_codigo = expresion.Ejecutar(base_datos, entorno)
                if isinstance(res_expresion_codigo, RetornoCodigo):
                    expresiones.append(res_expresion_codigo.codigo)
                else:
                    return RetornoError("Se produjo un error al intentar definir la instrucción 'UPDATE' dentro de la creación del PROCEDURE.")

            # En el caso que ocurra un error al obtener la condicion
            res_condicion_codigo = self.condicion.Ejecutar(base_datos, entorno)
            if isinstance(res_condicion_codigo, RetornoCodigo):
                return RetornoCodigo("UPDATE {} SET {} WHERE {};\n".format(nombre_tabla, ", ".join(expresiones), res_condicion_codigo.codigo))
            else:
                return RetornoError("Se produjo un error al intentar definir la instrucción 'UPDATE' dentro de la creación del PROCEDURE.")

        else:

            # Se inicializa la clase que sera utilizada para realizar el proceso del delete
            dml = DML()

            # Se obtiene toda la informacion que esta en el XML de la tabla
            informacion = {}
            obtener_tabla = dml.obtener_datos_tabla(base_datos.valor, nombre_tabla)
            if obtener_tabla.success:
                informacion[nombre_tabla] = obtener_tabla.lista
            else:
                return RetornoError(obtener_tabla.valor)

            # Se crea un nuevo entorno para almacenar la informacion de cada tabla y asi poder acceder a esas tablas desde el identificador cuando se este realizando la(s) condicion(es)
            nuevo_entorno = TablaDeSimbolos(entorno)
            simbolo = Simbolo('datos_tablas', informacion, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
            nuevo_entorno.agregar(simbolo)

            # Se obtienen todos los campos segun las condiciones dadas
            res_ejecutar_condicion = self.condicion.Ejecutar(base_datos, nuevo_entorno)
            if isinstance (res_ejecutar_condicion, RetornoError):
                return res_ejecutar_condicion
            condiciones_obtenidas = res_ejecutar_condicion.lista

            indices_a_actualizar = []
            for tupla in condiciones_obtenidas:
                indices_a_actualizar.append(tupla["{}.{}".format(nombre_tabla,'@index')])

            # Se obtienen los campos que se van a actualizar
            campos_actualizar = []
            for expresion in self.lista_expresiones:
                res_ejecutar_expresion = expresion.Ejecutar(base_datos, entorno)
                if isinstance (res_ejecutar_expresion, RetornoError):
                    return res_ejecutar_expresion
                campos_actualizar.append({"columna": res_ejecutar_expresion.identificador, "tipado": res_ejecutar_expresion.tipado,  "valor": res_ejecutar_expresion.valor})

            # Se actualizan los campos
            res_actualizar = dml.actualizar_datos_tabla(base_datos.valor, nombre_tabla, campos_actualizar, indices_a_actualizar)

            # Respuesta
            return RetornoCorrecto(res_actualizar.valor) if res_actualizar.success else RetornoError(res_actualizar.valor)

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_update = hash("UPDATE" + str(contador[0]))
        label_update = "\"{}\"[label=\"{}\"];\n".format(id_nodo_update, "UPDATE")
        union_update = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_update)
        result = label_update + union_update

        # Se obtiene el nombre de la tabla
        result += self.identificador.GraficarArbol(id_nodo_update, contador)

        # Se obtiene la lista de expresiones
        for expresion in self.lista_expresiones:
            result += expresion.GraficarArbol(id_nodo_update, contador)

        # Se obtiene la condicion
        result += self.condicion.GraficarArbol(id_nodo_update, contador)

        return result
