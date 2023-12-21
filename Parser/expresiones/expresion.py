from ..abstract.expresiones import Expresion
from ..expresiones.identificador import Identificador
from ..expresiones.literal import Literal
from ..abstract.retorno import RetornoCodigo, RetornoArreglo, RetornoError, TIPO_DATO
from Funcionalidad.dml import DML

# Esta clase se encarga de retornar una instancia 'RetornoXYZ' y atraves de esto pueda validarse cada comando o instruccion del lenguaje
class Expresion(Expresion):

    def __init__(self, id_nodo: str, expresion: any):
        self.id_nodo = id_nodo
        self.expresion = expresion

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no si se esta construyendo un procedimiento o una funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            if isinstance(self.expresion, Identificador):
                res_expresion = self.expresion.Ejecutar(base_datos, entorno)
                return RetornoCodigo(res_expresion['identificador'])
            elif isinstance(self.expresion, Literal):
                res_expresion = self.expresion.Ejecutar(base_datos, entorno)
                if self.expresion.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR):
                    return RetornoCodigo("'{}'".format(res_expresion.valor))
                else:
                    return RetornoCodigo(str(res_expresion.valor))
            else:
                res_expresion = self.expresion.Ejecutar(base_datos, entorno)
                return RetornoCodigo(res_expresion.codigo)
        else:

            if isinstance(self.expresion, Identificador):
                res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)

                # Se busca en la tabla de simbolos el nombre de la variable
                simbolo = entorno.obtener(res_ejecutar['identificador'])

                if simbolo is None:

                    # Se evalua si se retorna como RetornarArreglo | dict (identificador)
                    simbolo_datos_tablas = entorno.obtener("datos_tablas")
                    if simbolo_datos_tablas is None:
                        return res_ejecutar
                    else:
                        dml = DML()
                        datos = dml.verificar_columna_tabla(base_datos.valor, simbolo_datos_tablas.valor, res_ejecutar['identificador'], res_ejecutar['referencia_tabla'])
                        if datos.success:
                            return RetornoArreglo(res_ejecutar['identificador'], datos.valor, datos.lista)
                        else:
                            return RetornoError(datos.valor)
                else:
                    return Literal(None, simbolo.valor, simbolo.tipo_dato, simbolo.id).Ejecutar(base_datos, entorno)
            else:
                res_ejecutar = self.expresion.Ejecutar(base_datos, entorno)
                return res_ejecutar

    def GraficarArbol(self, id_padre):
        label_encabezado = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "EXPRESION")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.expresion.id_nodo)
        resultado_izquierda = self.expresion.GraficarArbol(self.id_nodo)
        return label_encabezado + union_hijo_izquierdo + resultado_izquierda