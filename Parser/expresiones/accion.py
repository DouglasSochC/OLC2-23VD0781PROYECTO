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
                if isinstance(res_campo, RetornoError):
                    return res_campo

                if 'not_null' in res_campo:
                    return RetornoError("No es posible agregar la restricción NOT NULL en la columna '{}', debido a que la columna se está agregando sin un valor predeterminado y contiene valores nulos existentes.".format(res_campo['name']))

                # Se almacena el diccionario que contiene toda la informacion del nuevo campo a agregar en la tabla
                respuesta.append(res_campo)

            return respuesta

        elif self.tipo_accion == 'drop':

            res_accion = self.accion.Ejecutar(base_datos, entorno)
            if isinstance(res_accion, RetornoError):
                return res_accion

            nombre_columna = res_accion.identificador
            return nombre_columna

    def GraficarArbol(self, id_padre):
        return ""