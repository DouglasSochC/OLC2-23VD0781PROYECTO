from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..expresiones.constraint import Constraint

class Campo_Table(Expresion):

    def __init__(self, id_nodo: str, identificador: Identificador, tipo_dato: Tipo_Dato, constraint: Constraint):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.tipo_dato = tipo_dato
        self.constraint = constraint

    def Ejecutar(self, base_datos, entorno):

        respuesta = {}

        # Se obtiene el nombre del campo y se agrega a la respuesta
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_campo = res_identificador['identificador']
        respuesta.update({"name": nombre_campo})

        # Se obtiene el tipo de dato del campo y se agrega a la respuesta
        res_tipo_dato = self.tipo_dato.Ejecutar(base_datos, entorno)
        respuesta.update({"type": res_tipo_dato['representacion']})

        if res_tipo_dato['dimension'] >= 0:
            respuesta.update({"length": res_tipo_dato['dimension']})

        # Se obtiene un diccionario con el constraint y se agrega a la respuesta
        if self.constraint is not None:
            res_constraint = self.constraint.Ejecutar(base_datos, entorno)
            respuesta.update(res_constraint)

        return respuesta

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CAMPOS_TABLE")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        label_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_identificador + label_tipo_dato
        if self.constraint is not None:
            label_constraint = self.constraint.GraficarArbol(self.id_nodo)
            union_constrain = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.constraint.id_nodo)
            result+= label_constraint + union_constrain

        return result
