from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from Funcionalidad.administracion import Administracion

class Use(Instruccion):

    def __init__(self, id_nodo, texto: str):
        self.id_nodo = id_nodo
        self.texto = texto
        pass

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'USE' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'USE' dentro de la creacion de un PROCEDURE o FUNCTION")

        nombre = self.texto

        administracion = Administracion()

        res_admin = administracion.verificar_existencia_bd(nombre)

        if res_admin.success:
            base_datos.valor = nombre
            return RetornoCorrecto(res_admin.valor)
        else:
            return RetornoError(res_admin.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "USE")
        label_base_datos = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "DB", self.removeQuotes(self.texto))
        constr_identificador = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "DB")
        return label_encabezado + label_base_datos + constr_identificador

    def removeQuotes(self, value):
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                mundo_without_quotes = value.strip('"')
                return mundo_without_quotes
        return value