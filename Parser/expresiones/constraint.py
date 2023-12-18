from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError
from ..expresiones.identificador import Identificador

class Constraint(Expresion):

    def __init__(self, id_nodo, tipo_constraint: str, tabla_referencia: Identificador, campo_referencia: Identificador):
        self.id_nodo = id_nodo
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
            if isinstance(res_tabla_referencia, RetornoError):
                return res_tabla_referencia
            nombre_tabla = res_tabla_referencia.identificador

            res_campo_referencia = self.campo_referencia.Ejecutar(base_datos, entorno)
            if isinstance(res_campo_referencia, RetornoError):
                return res_campo_referencia
            nombre_campo = res_campo_referencia.identificador

            return {'fk_table':nombre_tabla, 'fk_attribute':nombre_campo}
        else:
            return RetornoError("Ha ocurrido un error al definir el constraint.")
        
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CONSTRAIN")
        label_tipo_constraint = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "C", self.tipo_constraint)
        union_encabezado_tipo_constraint = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "C")
        result = label_encabezado + label_tipo_constraint + union_encabezado_tipo_constraint
        
        if self.tabla_referencia is not None:
            tabla_referencia = self.tabla_referencia.GraficarArbol(self.id_nodo)
            result += tabla_referencia
        if self.campo_referencia is not None:
            campo_referencia = self.campo_referencia.GraficarArbol(self.id_nodo)
            result += campo_referencia
        return result 
        
