from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError
from ..expresiones.identificador import Identificador
from Funcionalidad.ddl import DDL

class Truncate(Instruccion):

    def __init__(self, id_nodo, identificador: any):
        self.id_nodo = id_nodo
        self.identificador = identificador

    def Ejecutar(self, base_datos, entorno):
        
        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("TRUNCATE")

        # Se obtiene el nombre de la tabla
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador, RetornoError):
            return res_identificador.msg

        nombre_tabla = res_identificador.identificador

        ddl = DDL()
        res_truncate = ddl.truncate_tabla(base_datos.valor, nombre_tabla)

        if res_truncate.success:
            return res_truncate.valor
        else:
            return "ERROR: {}".format(res_truncate.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "TRUNCATE")
        result = label_encabezado
        if(isinstance(self.identificador, Identificador)):
            label_identificador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.identificador.valor)
            union_identificador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
            result += label_identificador + union_identificador
        return result