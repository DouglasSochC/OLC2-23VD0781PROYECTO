from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto, TIPO_DATO, TIPO_ENTORNO
from ..tablas.tabla_simbolo import Simbolo, TablaDeSimbolos
from ..expresiones.identificador import Identificador
from ..expresiones.condicion import Condicion
from ..expresiones.expresion import Expresion
from Funcionalidad.dml import DML

class Update(Instruccion):

    def __init__(self, id_nodo: str, identificador: Identificador, lista_expresiones: list[Expresion], condicion: Condicion):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones
        self.condicion = condicion

    def Ejecutar(self, base_datos, entorno):

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

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

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "UPDATE")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        resultado = label_encabezado + label_identificador

        if self.lista_expresiones is not None:
            for campo in self.lista_expresiones:
                label_campo = campo.GraficarArbol(self.id_nodo)
                unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo, campo.id_nodo)
                resultado += label_campo + unir_campo
        
        if self.condicion is not None and isinstance(self.condicion, Condicion):

            label_condicion = self.condicion.GraficarArbol(self.id_nodo)
            union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.condicion.id_nodo)
            resultado += label_condicion + union_tipo_accion_campo
        
        return resultado
