from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import TIPO_TOKEN, RetornoError
from ..expresiones.identificador import Identificador
from Funcionalidad.dml import DML

class Select(Instruccion):

    def __init__(self, identificador: str, lista_campos: list, lista_condiciones: list):
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_condiciones = lista_condiciones

    # TODO: Falta implementar lo siguiente
        # Implementar BETWEEN
        # Implementar funciones nativas en el donde se obtienen las columnas y en donde se realiza las condiciones (WHERE)
    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("SELECT")

        nuevo_entorno = TablaDeSimbolos({})

        # Se obtiene el nombre de la tabla
        nombre_tabla = self.identificador.Ejecutar(base_datos, nuevo_entorno).identificador

        # Se almacena la tabla para poder acceder a ella desde un identificador y asi poder obtener la informacion completa de la tabla
        simbolo = Simbolo('nombre_tabla', None, TIPO_TOKEN.SELECT, nombre_tabla, None)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen la lista de condiciones que se debe de aplicar al SELECT y se almacenan en la variable 'listado_condiciones'
        listado_condiciones = []
        if len(self.lista_condiciones) > 0:
            for condicion in self.lista_condiciones:

                res = condicion.Ejecutar(base_datos, nuevo_entorno)

                if isinstance (res, RetornoError):
                    return res.msg

                # Se obtienen los indices que cumplen con las condiciones
                listado_condiciones.append(res)
                listado_condiciones.append('AND')

            listado_condiciones.pop()

        dml = DML()

        if self.lista_campos[0] == '*':
            self.lista_campos.pop()
            columnas = dml.obtener_todas_las_columnas_tabla(base_datos.valor, nombre_tabla)
            for columna in columnas:
                self.lista_campos.append(Identificador(-1, columna))

        # Se obtienen los indices que son validos segun las condiciones dadas
        lista_indices = dml.obtener_indices_segun_condiciones(base_datos.valor, nombre_tabla, listado_condiciones)

        resultado = { "encabezado": [], "data": []}
        temp_dimensional = -1 # Esta variable verifica que toda la informacion obtenida a traves de los campos sea de la misma dimensional
        for expr in self.lista_campos:

            res_ejecutar = expr.Ejecutar(base_datos, nuevo_entorno)

            if isinstance(res_ejecutar, RetornoError):
                return res_ejecutar.msg

            if temp_dimensional == -1:
                temp_dimensional = len(res_ejecutar.lista)
            elif temp_dimensional != len(res_ejecutar.lista):
                return "ERROR: No se puede realizar el 'SELECT' debido a problemas con las dimensionales de cada campo solicitado"

            identificador = res_ejecutar.identificador if res_ejecutar.alias is None else res_ejecutar.alias
            resultado['encabezado'].append(identificador)
            res_aplicar_condiciones = dml.sintetizar_condiciones(res_ejecutar.lista, lista_indices)
            if (len(resultado['data']) == 0):
                for valor in res_aplicar_condiciones.lista:
                    resultado['data'].append([valor])
            else:
                for indice, matriz in enumerate(resultado['data']):
                    resultado['data'][indice].append(res_aplicar_condiciones.lista[indice])

        return resultado

    def GraficarArbol(self, id_padre):
        return ""
