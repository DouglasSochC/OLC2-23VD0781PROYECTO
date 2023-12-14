from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import TIPO_TOKEN, RetornoError
from Funcionalidad.dml import DML

class Select(Instruccion):

    def __init__(self, identificador: str, lista_campos: list, lista_condiciones: list):
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_condiciones = lista_condiciones

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("SELECT")

        nuevo_entorno = TablaDeSimbolos()

        # Se obtiene el nombre de la tabla
        nombre_tabla = self.identificador.Ejecutar(base_datos, nuevo_entorno).identificador

        # Se obtienen la lista de condiciones que se debe de aplicar al SELECT y se almacenan en la variable 'listado_condiciones'
        listado_condiciones = []
        if (len(self.lista_condiciones) > 0):
            for condicion in self.lista_condiciones:

                res = condicion.Ejecutar(base_datos, nuevo_entorno)
                if isinstance (res, RetornoError):
                    return res.msg
                listado_condiciones.append(res)
                listado_condiciones.append('AND')

            listado_condiciones.pop()

        # Se almacena la tabla para poder acceder a ella desde un identificador y asi poder obtener la informacion completa de la tabla
        simbolo = Simbolo('nombre_tabla', None, TIPO_TOKEN.SELECT, nombre_tabla, None)
        nuevo_entorno.agregar(simbolo)

        temp_dimensional = -1 # Esta variable verifica que toda la informacion obtenida a traves de los campos sea de la misma dimensional
        resultado = { "encabezado": [], "data": []}
        dml = DML()
        for expr in self.lista_campos:

            res_ejecutar = expr.Ejecutar(base_datos, nuevo_entorno)

            if isinstance(res_ejecutar, RetornoError):
                return res_ejecutar.msg

            if temp_dimensional == -1:
                temp_dimensional = len(res_ejecutar.lista)
            elif temp_dimensional != len(res_ejecutar.lista):
                return "ERROR: No se puede realizar el 'SELECT' debido a problemas con las dimensionales de cada campo solicitado"

            resultado['encabezado'].append(res_ejecutar.identificador)
            res_aplicar_condiciones = dml.aplicar_condiciones(res_ejecutar.lista, listado_condiciones)
            if (len(resultado['data']) == 0):
                for valor in res_aplicar_condiciones.lista:
                    resultado['data'].append([valor])
            else:
                for indice, matriz in enumerate(resultado['data']):
                    resultado['data'][indice].append(res_aplicar_condiciones.lista[indice])

        return resultado

    def GraficarArbol(self, id_padre):
        return ""
