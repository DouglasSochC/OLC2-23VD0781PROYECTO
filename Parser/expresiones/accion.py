from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError
from ..expresiones.campo_table import Campo_Table
from ..expresiones.identificador import Identificador

class Accion(Expresion):

    def __init__(self, id_nodo, tipo_accion: str, accion: list[Campo_Table] | Identificador):
        self.id_nodo = id_nodo
        self.tipo_accion = tipo_accion
        self.accion = accion

    def Ejecutar(self, base_datos, entorno):

        if self.tipo_accion == 'add':

            respuesta = []

            for campo in self.accion:
                res_campo = campo.Ejecutar(base_datos, entorno)

                if 'not_null' in res_campo:
                    return RetornoError("No es posible agregar la restricción NOT NULL en la columna '{}', debido a que la columna se está agregando sin un valor predeterminado y contiene valores nulos existentes.".format(res_campo['name']))
                elif 'pk' in res_campo:
                    return RetornoError("No es posible agregar la restricción PRIMARY KEY en la columna '{}', debido a que la columna se está agregando sin un valor predeterminado y contiene valores nulos existentes.".format(res_campo['name']))

                # Se almacena el diccionario que contiene toda la informacion del nuevo campo a agregar en la tabla
                respuesta.append(res_campo)

            return respuesta

        elif self.tipo_accion == 'drop':

            res_accion = self.accion.Ejecutar(base_datos, entorno)
            nombre_columna = res_accion['identificador']
            return nombre_columna

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "ACCION")
        label_tipo_accion = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "C", self.tipo_accion)
        union_encabezado_tipo_accion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "C")
        result = label_encabezado + label_tipo_accion + union_encabezado_tipo_accion

        if isinstance(self.accion, list) and self.accion:
            primer_elemento = self.accion[0]
            if isinstance(primer_elemento, Campo_Table):
                for campo in self.accion:
                    label_campo = campo.GraficarArbol(self.id_nodo)
                    union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, campo.id_nodo)
                    result += label_campo + union_tipo_accion_campo
            else:
                label_tipo_dato = self.accion.GraficarArbol(self.id_nodo)
                result += label_tipo_dato
        else:
            label_tipo_dato = self.accion.GraficarArbol(self.id_nodo)
            result += label_tipo_dato

        return result
