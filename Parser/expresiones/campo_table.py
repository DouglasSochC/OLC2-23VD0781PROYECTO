from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.tipo_dato import Tipo_Dato
from ..expresiones.constraint import Constraint

class Campo_Table(Expresion):

    def __init__(self, identificador: Identificador, tipo_dato: Tipo_Dato, constraint: Constraint):
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

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_campo_table = hash("CAMPO_TABLE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_campo_table, "CAMPO_TABLE")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_campo_table)
        result = label_encabezado + union

        # Se obtiene el cuerpo del nodo identificador
        result += self.identificador.GraficarArbol(id_nodo_campo_table, contador)

        # Se obtiene el cuerpo del nodo tipo de dato
        result += self.tipo_dato.GraficarArbol(id_nodo_campo_table, contador)

        # Se obtiene el cuerpo del nodo constraint
        if self.constraint is not None:
            result += self.constraint.GraficarArbol(id_nodo_campo_table, contador)

        return result
