from ..abstract.instrucciones import Instruccion
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..abstract.retorno import RetornoError, RetornoArreglo, RetornoLiteral, RetornoCorrecto, TIPO_DATO, TIPO_ENTORNO
from ..expresiones.expresion import Expresion
from ..expresiones.condicion import Condicion
from Funcionalidad.dml import DML

class Select(Instruccion):

    def __init__(self, id_nodo,lista_tablas: list[Expresion], lista_campos: list[Expresion], condicion: Condicion):
        self.id_nodo = id_nodo
        self.lista_tablas = lista_tablas
        self.lista_campos = lista_campos
        self.condicion = condicion

    # TODO: Falta implementar lo siguiente
        # Implementar BETWEEN
        # Implementar las siguientes funciones nativas: CONTAR, SUMA, CAS
    def Ejecutar(self, base_datos, entorno):

        if self.lista_tablas is None and self.condicion is None:

            for expresion in self.lista_campos:

                if expresion is not None:
                    res_ejecutar = expresion.Ejecutar(base_datos, entorno)
                    if isinstance(res_ejecutar, RetornoError):
                        return res_ejecutar
                    elif isinstance(res_ejecutar, RetornoLiteral):
                        return RetornoCorrecto(res_ejecutar.valor)
                    else:
                        return RetornoError("Ha ocurrido un problema durante la ejecución del comando 'SELECT'")

        if base_datos.valor == "":
            return "Para ejecutar el comando 'SELECT', es necesario seleccionar una base de datos."

        dml = DML()

        # Se obtienen el nombre de una tabla o los nombres de varias tablas
        informacion = {}
        for tabla in self.lista_tablas:

            res_tabla_ejecutar = tabla.Ejecutar(base_datos, entorno)

            if isinstance (res_tabla_ejecutar, RetornoError):
                return res_tabla_ejecutar
            elif isinstance(res_tabla_ejecutar, dict):
                # Se obtiene toda la informacion que esta en el XML de la tabla
                obtener_tabla = dml.obtener_datos_tabla(base_datos.valor, res_tabla_ejecutar['identificador'])
                if obtener_tabla.success:
                    informacion[res_tabla_ejecutar['identificador']] = obtener_tabla.lista
                else:
                    return RetornoError(obtener_tabla.valor)
            else:
                return RetornoError("Ha ocurrido un error al obtener la informacion de la(s) tabla(s).")

        # Se crea un nuevo entorno para almacenar la informacion de cada tabla y asi poder acceder a esas tablas desde el identificador cuando se este realizando la(s) condicion(es)
        nuevo_entorno = TablaDeSimbolos(entorno)
        simbolo = Simbolo('datos_tablas', informacion, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen todos los index's que cumplen con las condiciones dadas
        condiciones_obtenidas = []
        if len(informacion) > 1 and self.condicion is None:
            return RetornoError("Debido a que hay mas de una tabla por mostrar y no se ha dado una condicion especifica.")

        # Se obtienen todos los campos segun las condiciones dadas
        elif self.condicion is not None:
            res_ejecutar_condicion = self.condicion.Ejecutar(base_datos, nuevo_entorno)
            if isinstance (res_ejecutar_condicion, RetornoError):
                return res_ejecutar_condicion
            condiciones_obtenidas = res_ejecutar_condicion.lista

        # Se obtienen todos los campos de la tabla indicada en el caso que no hayan condiciones
        elif len(informacion) == 1 and self.condicion is None:
            condiciones_obtenidas = informacion[list(informacion.keys())[0]]

        # Se crea un nuevo entorno para obtener la informacion de cada columna
        simbolo = Simbolo('select_de_datos', condiciones_obtenidas, TIPO_DATO.NULL, -1, TIPO_ENTORNO.SENTENCIA_DML)
        nuevo_entorno.agregar(simbolo)

        # Se obtienen los campos que se van a mostrar a traves de los datos obtenidos por medio de las condiciones dadas
        resultado = { "encabezado": [], "data": []}
        indice_encabezado = 0
        for campo in self.lista_campos:

            if campo == '*':
                resultado = dml.obtener_informacion_completa(condiciones_obtenidas)
                continue

            res_ejecutar_campo = campo.Ejecutar(base_datos, nuevo_entorno)
            if isinstance (res_ejecutar_campo, RetornoError):
                return res_ejecutar_campo
            elif isinstance(res_ejecutar_campo, RetornoArreglo):

                # Se define el encabezado de la fila
                if res_ejecutar_campo.alias is None and res_ejecutar_campo.identificador is None:
                    resultado["encabezado"].append("encabezado{}".format(indice_encabezado))
                elif res_ejecutar_campo.alias is not None:
                    resultado["encabezado"].append(res_ejecutar_campo.alias)
                else:
                    resultado["encabezado"].append(res_ejecutar_campo.identificador)

                # Se formatea la informacion de la fila obtenida y se almacena en el resultado
                if res_ejecutar_campo.identificador is None:
                    dml.obtener_fila_de_auxiliar(res_ejecutar_campo.lista, resultado)
                elif res_ejecutar_campo.identificador is not None and res_ejecutar_campo.tabla_del_identificador is not None:
                    dml.obtener_fila_de_identificador(condiciones_obtenidas, res_ejecutar_campo.tabla_del_identificador, res_ejecutar_campo.identificador, resultado)
                elif res_ejecutar_campo.identificador is not None and res_ejecutar_campo.tabla_del_identificador is None:
                    dml.obtener_fila_de_auxiliar_funcion_nativa(res_ejecutar_campo.lista, resultado)
            else:
                RetornoError("Ha ocurrido un error al obtener la informacion de la(s) tabla(s).")

        return resultado 

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "SELECT")
        resultado = label_encabezado


        if self.lista_campos is not None:
            label_from = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo+"col", "COLUMNAS")
            unir_from = "\"{}\" -> \"{}\"\n".format(self.id_nodo, self.id_nodo+"col")
            resultado += label_from + unir_from
            if isinstance(self.lista_campos, list):
                aux = self.lista_campos[0]
                if(isinstance(aux, Expresion)):
                    for campo in self.lista_campos:
                        label_campo = campo.GraficarArbol(self.id_nodo)
                        unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo+"col", campo.id_nodo)
                        resultado += label_campo + unir_campo
                else:
                    label_campo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo+"todo", aux)
                    unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo+"col", self.id_nodo+"todo")
                    resultado += label_campo + unir_campo
            else:
                print("No es una lista")
        
        if self.lista_tablas is not None:
            label_from = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo+"from", "FROM")
            unir_from = "\"{}\" -> \"{}\"\n".format(self.id_nodo, self.id_nodo+"from")
            resultado += label_from + unir_from
            for tabla in self.lista_tablas:
                label_campo = tabla.GraficarArbol(self.id_nodo)
                unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo, tabla.id_nodo)
                resultado += label_campo + unir_campo
            
       
        if self.condicion is not None:

            label_condicion = self.condicion.GraficarArbol(self.id_nodo)
            unir_condicion = "\"{}\" -> \"{}\"\n".format(self.id_nodo, self.condicion.id_nodo)
            resultado += label_condicion + unir_condicion
        
        return resultado
