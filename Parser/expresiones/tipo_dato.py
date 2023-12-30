from ..abstract.expresiones import Expresion
from ..abstract.retorno import TIPO_DATO

class Tipo_Dato(Expresion):

    def __init__(self, tipo_dato: TIPO_DATO, dimension: int):
        self.tipo_dato = tipo_dato
        self.dimension = dimension

    def Ejecutar(self, base_datos, entorno):

        representacion = ""
        if self.tipo_dato == TIPO_DATO.BIT:
            representacion = "bit"
        elif self.tipo_dato == TIPO_DATO.INT:
            representacion = "int"
        elif self.tipo_dato == TIPO_DATO.DECIMAL:
            representacion = "decimal"
        elif self.tipo_dato == TIPO_DATO.DATE:
            representacion = "date"
        elif self.tipo_dato == TIPO_DATO.DATETIME:
            representacion = "datetime"
        elif self.tipo_dato == TIPO_DATO.NCHAR:
            representacion = "nchar"
        elif self.tipo_dato == TIPO_DATO.NVARCHAR:
            representacion = "nvarchar"

        return {'tipo_dato': self.tipo_dato, 'representacion': representacion, 'dimension': self.dimension}

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_tipo_dato = hash("TIPO_DATO" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_tipo_dato, "TIPO_DATO")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_tipo_dato)
        result = label_encabezado + union

        # Se obtiene el nombre del tipo de dato
        contador[0] += 1
        id_nodo_nombre_tipo_dato = hash("NOMBRE_TIPO_DATO" + str(contador[0]))
        label_nombre_tipo_dato = "\"{}\"[label=\"{}\"];\n".format(id_nodo_nombre_tipo_dato, self.tipo_dato.name)
        union_nombre_tipo_dato = "\"{}\"->\"{}\";\n".format(id_nodo_tipo_dato, id_nodo_nombre_tipo_dato)
        result += label_nombre_tipo_dato + union_nombre_tipo_dato

        # Se obtiene la dimension del tipo de dato
        if self.tipo_dato != -1:
            contador[0] += 1
            id_nodo_dimension_tipo_dato = hash("DIMENSION_TIPO_DATO" + str(contador[0]))
            label_dimension_tipo_dato = "\"{}\"[label=\"{}\"];\n".format(id_nodo_dimension_tipo_dato, self.dimension)
            union_dimension_tipo_dato = "\"{}\"->\"{}\";\n".format(id_nodo_tipo_dato, id_nodo_dimension_tipo_dato)
            result += label_dimension_tipo_dato + union_dimension_tipo_dato

        return result
