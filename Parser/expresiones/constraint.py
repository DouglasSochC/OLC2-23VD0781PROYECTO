from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador

class Constraint(Expresion):

    def __init__(self, tipo_constraint: str, tabla_referencia: Identificador, campo_referencia: Identificador):
        self.tipo_constraint = tipo_constraint
        self.tabla_referencia = tabla_referencia
        self.campo_referencia = campo_referencia

    def Ejecutar(self, base_datos, entorno):

        if self.tipo_constraint == 'primary key':

            return {"pk":""}

        elif self.tipo_constraint == 'not null':

            return {"not_null":""}

        elif self.tipo_constraint == 'references':

            res_tabla_referencia = self.tabla_referencia.Ejecutar(base_datos, entorno)
            nombre_tabla = res_tabla_referencia['identificador']

            res_campo_referencia = self.campo_referencia.Ejecutar(base_datos, entorno)
            nombre_campo = res_campo_referencia['identificador']

            return {'fk_table':nombre_tabla, 'fk_attribute':nombre_campo}

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_constraint = hash("CONSTRAINT" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_constraint, "CONSTRAINT")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_constraint)
        result = label_encabezado + union

        # Se crea el nodo del tipo de constraint y se une con el nodo de constraint
        contador[0] += 1
        id_nodo_tipo_constraint = hash("TIPO_CONSTRAINT" + str(contador[0]))
        label_tipo_constraint = "\"{}\"[label=\"{}\"];\n".format(id_nodo_tipo_constraint, self.tipo_constraint)
        union_tipo_constraint = "\"{}\"->\"{}\";\n".format(id_nodo_constraint, id_nodo_tipo_constraint)
        result += label_tipo_constraint + union_tipo_constraint

        # Se obtiene el cuerpo del nodo tabla referencia
        if self.tabla_referencia is not None:
            result += self.tabla_referencia.GraficarArbol(id_nodo_constraint, contador)

        # Se obtiene el cuerpo del nodo campo referencia
        if self.campo_referencia is not None:
            result += self.campo_referencia.GraficarArbol(id_nodo_constraint, contador)

        return result
