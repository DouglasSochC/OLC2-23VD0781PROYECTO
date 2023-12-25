from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from Funcionalidad.administracion import Administracion

class Use(Instruccion):

    def __init__(self, id_nodo, texto: str):
        self.id_nodo = id_nodo
        self.texto = texto
        pass

    def Ejecutar(self, base_datos, entorno):
        pass

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