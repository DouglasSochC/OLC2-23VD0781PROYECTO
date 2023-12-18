from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError
from ..expresiones.identificador import Identificador
from Funcionalidad.dml import DML

class Insert(Instruccion):

    def __init__(self, id_nodo, identificador: Identificador, lista_campos: list, lista_valores: list):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_valores = lista_valores

    def Ejecutar(self, base_datos, entorno):
        '''
        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("INSERT")

        # Se obtiene el nombre de la tabla
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador, RetornoError):
            return res_identificador.msg
        nombre_tabla = res_identificador.identificador

        campos = []
        for campo in self.lista_campos:

            # En el caso que ocurra un error al obtener el listado de campos
            res = campo.Ejecutar(base_datos, entorno)
            if isinstance(res, RetornoError):
                return res.msg

            # Se almacena el campo en el array 'campos'
            campos.append(res.identificador)

        valores = []
        for valor in self.lista_valores:

            # En el caso que ocurra un error al obtener los values del insert
            res = valor.Ejecutar(base_datos, entorno)
            if isinstance(res, RetornoError):
                return res.msg

            # Se almacena el value en el array 'valores'
            valores.append(res.valor)

        if len(campos) != len(valores):
            return "ERROR: La cantidad de columnas especificada en la declaración INSERT no coincide con la cantidad de valores proporcionados en la cláusula VALUES."

        if len(campos) != len(set(campos)):
            return "ERROR: Una o más columnas han sido especificadas más de una vez en la declaración INSERT, lo cual no está permitido."

        tupla = dict(zip(campos, valores))
        dml = DML()
        res_dml = dml.insertar_registro_tabla(base_datos.valor, nombre_tabla, tupla)

        if res_dml.success:
            return res_dml.valor
        else:
            return "ERROR: {}".format(res_dml.valor)
'''
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "INSERT")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        resultado = label_encabezado + label_identificador

        if self.lista_campos is not None:
            for campo in self.lista_campos:
                label_campo = campo.GraficarArbol(self.id_nodo)
                unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo, campo.id_nodo)
                resultado += label_campo + unir_campo
        
        label_values = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo+"c", "VALUES")
        union_values = "\"{}\" -> \"{}\"\n".format(self.id_nodo, self.id_nodo+"c")
        resultado += label_values + union_values
        
        if self.lista_valores is not None:
            for valor in self.lista_valores:
                label_valor = valor.GraficarArbol(self.id_nodo)
                unir_valor = "\"{}\" -> \"{}\"\n".format(self.id_nodo, valor.id_nodo)
                resultado += label_valor + unir_valor
        
        return resultado