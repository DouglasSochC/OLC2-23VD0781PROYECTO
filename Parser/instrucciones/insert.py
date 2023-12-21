from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoCorrecto
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from Funcionalidad.dml import DML

class Insert(Instruccion):

    def __init__(self, id_nodo: str, identificador: Identificador, lista_campos: list[Expresion], lista_valores: list[Expresion]):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_valores = lista_valores

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return "Para ejecutar el comando 'INSERT', es necesario seleccionar una base de datos."

        # Se obtiene el nombre de la tabla
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        # Se verifica que no si se esta construyendo un procedimiento o una funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:

            campos = []
            for campo in self.lista_campos:

                # En el caso que ocurra un error al obtener el listado de campos
                res = campo.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoCodigo):
                    campos.append(res.codigo)
                else:
                    return RetornoError("Ha ocurrido un error al definir el INSERT dentro de la creacion de un PROCEDURE o FUNCTION")

            valores = []
            for valor in self.lista_valores:

                # En el caso que ocurra un error al obtener el listado de valores
                res = valor.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoCodigo):
                    valores.append(res.codigo)
                else:
                    return RetornoError("Ha ocurrido un error al definir el INSERT dentro de la creacion de un PROCEDURE o FUNCTION")

            return RetornoCodigo("INSERT INTO {} ({}) VALUES ({});\n".format(nombre_tabla, ", ".join(campos), ", ".join(valores)))

        else:

            campos = []
            for campo in self.lista_campos:

                # En el caso que ocurra un error al obtener el listado de campos
                res = campo.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoError):
                    return res
                # Se almacena el campo en el array 'campos' en el caso que sea un 'identificador'
                elif isinstance(res, dict):
                    campos.append(res['identificador'])
                else:
                    return RetornoError("Hay un error al definir los campos del INSERT")

            valores = []
            for valor in self.lista_valores:

                # En el caso que ocurra un error al obtener los values del insert
                res = valor.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoError):
                    return res

                # Se almacena el value en el array 'valores'
                valores.append(res.valor)

            if len(campos) != len(valores):
                return RetornoError("La cantidad de columnas especificada en la declaración INSERT no coincide con la cantidad de valores proporcionados en la cláusula VALUES.")

            if len(campos) != len(set(campos)):
                return RetornoError("Una o más columnas han sido especificadas más de una vez en la declaración INSERT, lo cual no está permitido.")

            tupla = dict(zip(campos, valores))
            dml = DML()
            res_dml = dml.insertar_registro_tabla(base_datos.valor, nombre_tabla, tupla)

            return RetornoCorrecto(res_dml.valor) if res_dml.success else RetornoError(res_dml.valor)

    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "INSERT")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        resultado = label_encabezado + label_identificador

        if self.lista_campos is not None:
            for campo in self.lista_campos:
                label_campo = campo.GraficarArbol(self.id_nodo)
                unir_campo = "\"{}\" -> \"{}\"\n".format(self.id_nodo, campo.id_nodo)
                resultado += label_campo + unir_campo

        label_values = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo+"c", "VALUES")
        union_values = "\"{}\" -> \"{}\"\n".format(self.id_nodo, self.id_nodo+"c")
        resultado += label_values + union_values

        if self.lista_valores is not None:
            for valor in self.lista_valores:
                label_valor = valor.GraficarArbol(self.id_nodo)
                unir_valor = "\"{}\" -> \"{}\"\n".format(self.id_nodo, valor.id_nodo)
                resultado += label_valor + unir_valor

        return resultado