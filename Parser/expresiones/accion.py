from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoError
from ..expresiones.campo_table import Campo_Table
from ..expresiones.identificador import Identificador

class Accion(Expresion):

    def __init__(self, tipo_accion: str, accion: list[Campo_Table] | Identificador):
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

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_accion = hash("ACCION" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_accion, "ACCION")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_accion)
        result = label_encabezado + union

        # Se crea el nodo del tipo de accion y se une con el nodo de accion
        contador[0] += 1
        id_nodo_tipo_accion = hash("TIPO_ACCION" + str(contador[0]))
        label_tipo_accion = "\"{}\"[label=\"{}\"];\n".format(id_nodo_tipo_accion, self.tipo_accion)
        union_tipo_accion = "\"{}\"->\"{}\";\n".format(id_nodo_accion, id_nodo_tipo_accion)
        result += label_tipo_accion + union_tipo_accion

        # Se obtiene el cuerpo del nodo accion
        if self.accion is not None:

            # En el caso que sea campo_table
            if isinstance(self.accion, list):
                primer_elemento = self.accion[0]
                if isinstance(primer_elemento, Campo_Table):
                    for campo in self.accion:
                        result += campo.GraficarArbol(id_nodo_accion, contador)

            # En el caso que sea identificador
            else:
                result += self.accion.GraficarArbol(id_nodo_accion, contador)

        return result
