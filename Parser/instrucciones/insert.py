from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError
from Funcionalidad.dml import DML

class Insert(Instruccion):

    def __init__(self, identificador, lista_campos: list, lista_valores: list):
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_valores = lista_valores

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("DELETE")

        # Se obtiene el nombre de la tabla
        nombre_tabla = self.identificador.Ejecutar(base_datos, entorno).identificador

        campos = []
        for campo in self.lista_campos:

            res = campo.Ejecutar(base_datos, entorno)

            if isinstance(res, RetornoError):
                return res.msg

            campos.append(res.identificador)

        valores = []
        for valor in self.lista_valores:
            res = valor.Ejecutar(base_datos, entorno)

            if isinstance(res, RetornoError):
                return res.msg

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

    def GraficarArbol(self, id_padre):
        return ""