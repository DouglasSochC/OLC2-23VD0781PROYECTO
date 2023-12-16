from ..abstract.instrucciones import Instruccion
from Funcionalidad.administracion import Administracion

class Use(Instruccion):

    def __init__(self, id_nodo, identificador: str):
        self.id_nodo = id_nodo
        self.identificador = identificador
        pass

    def Ejecutar(self, base_datos, entorno):

        nombre = self.identificador
        nombre = nombre[1:-1]

        administracion = Administracion()

        res_admin = administracion.verificar_existencia_bd(nombre)

        if res_admin.success:
            base_datos.valor = nombre
            return res_admin.valor
        else:
            return "ERROR: {}".format(res_admin.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "USE")
        label_base_datos = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "DB", self.removeQuotes(self.identificador))
        constr_identificador = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "DB")
        return label_encabezado + label_base_datos + constr_identificador

    def removeQuotes(self, value):
        if isinstance(value, str):
            if value.startswith('"') and value.endswith('"'):
                mundo_without_quotes = value.strip('"')
            return mundo_without_quotes
        return value