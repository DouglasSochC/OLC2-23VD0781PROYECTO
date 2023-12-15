from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_TOKEN, RetornoIdentificador, RetornoError
from Funcionalidad.dml import DML

class Identificador(Expresion):

    def __init__(self, id_nodo: int, valor: any, alias_tabla: any = None, alias_nombre: any = None):
        self.id_nodo = id_nodo
        self.valor = valor
        self.alias_tabla = alias_tabla
        self.alias_nombre = alias_nombre

    def Ejecutar(self, base_datos, entorno):

        # Debido a que la informacion de la tabla se obtendra desde aqui, es necesario determinar si ya existe el nombre de la tabla en la tabla de simbolos
        tabla = entorno.obtener('nombre_tabla')
        if tabla is not None:

            # Si es un SELECT, se obtendra toda la informacion del campo (self.valor) de la tabla
            if tabla.tipo_token == TIPO_TOKEN.SELECT:
                dml = DML()
                res = dml.seleccionar_columna_tabla(base_datos.valor, tabla.valor, self.valor)

                if res.success:
                    return RetornoIdentificador(self.valor, res.valor, res.lista, self.alias_nombre)
                else:
                    return RetornoError(res.valor)

        return RetornoIdentificador(self.valor, None, [], self.alias_nombre)

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "IDENTIFICADOR")
        label_valor = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.valor)
        union_hijo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
        return label_encabezado + label_valor + union_hijo 