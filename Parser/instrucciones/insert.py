from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCodigo, RetornoCorrecto
from ..expresiones.identificador import Identificador
from ..expresiones.expresion import Expresion
from Funcionalidad.dml import DML

class Insert(Instruccion):

    def __init__(self, identificador: Identificador, lista_campos: list[Expresion], lista_valores: list[Expresion]):
        self.identificador = identificador
        self.lista_campos = lista_campos
        self.lista_valores = lista_valores

    def Ejecutar(self, base_datos, entorno):

        if base_datos.valor == "":
            return RetornoError("Para ejecutar el comando 'INSERT', es necesario seleccionar una base de datos.")

        # Se obtiene el nombre de la tabla
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        nombre_tabla = res_identificador['identificador']

        # Se verifica que no se este utilizando el comando 'INSERT' dentro de la creacion de una funcion
        construir_funcion = entorno.obtener("construir_funcion")
        if construir_funcion is not None:
            return RetornoError("No es posible realizar una instrucción 'INSERT' dentro del cuerpo del FUNCTION.")

        # Se verifica si el comando 'INSERT' esta siendo utilizado en la creacion de un procedimiento
        construir_procedimiento = entorno.obtener("construir_procedimiento")
        if construir_procedimiento is not None:

            campos = []
            for campo in self.lista_campos:

                # En el caso que ocurra un error al obtener el listado de campos
                res = campo.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoCodigo):
                    campos.append(res.codigo)
                else:
                    return RetornoError("Se produjo un error al intentar definir la instrucción 'INSERT' dentro de la creación del PROCEDURE.")

            valores = []
            for valor in self.lista_valores:

                # En el caso que ocurra un error al obtener el listado de valores
                res = valor.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoCodigo):
                    valores.append(res.codigo)
                else:
                    return RetornoError("Se produjo un error al intentar definir la instrucción 'INSERT' dentro de la creación del PROCEDURE.")

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
                    return RetornoError("Hay un error al definir los campos del 'INSERT'")

            valores = []
            for valor in self.lista_valores:

                # En el caso que ocurra un error al obtener los values del insert
                res = valor.Ejecutar(base_datos, entorno)
                if isinstance(res, RetornoError):
                    return res

                # Se almacena el value en el array 'valores'
                valores.append(res.valor)

            if len(campos) != len(valores):
                return RetornoError("La cantidad de columnas especificada en el comando 'INSERT' no coincide con la cantidad de valores proporcionados en la cláusula VALUES.")

            if len(campos) != len(set(campos)):
                return RetornoError("Una o más columnas han sido especificadas más de una vez en la declaración 'INSERT', lo cual no está permitido.")

            tupla = dict(zip(campos, valores))
            dml = DML()
            res_dml = dml.insertar_registro_tabla(base_datos.valor, nombre_tabla, tupla)

            return RetornoCorrecto(res_dml.valor) if res_dml.success else RetornoError(res_dml.valor)

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_insert = hash("INSERT" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_insert, "INSERT")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_insert)
        result = label_encabezado + union

        # Se crea el nodo del nombre de la tabla y se une con el nodo de insert
        result += self.identificador.GraficarArbol(id_nodo_insert, contador)

        # Se crea el nodo de los campos y se une con el nodo de insert
        if self.lista_campos is not None:
            contador[0] += 1
            id_nodo_campos = hash("CAMPOS" + str(contador[0]))
            label_campos = "\"{}\"[label=\"{}\"];\n".format(id_nodo_campos, "CAMPOS")
            union_campos = "\"{}\"->\"{}\";\n".format(id_nodo_insert, id_nodo_campos)
            result += label_campos + union_campos

            for campo in self.lista_campos:
                result += campo.GraficarArbol(id_nodo_campos, contador)

        # Se crea el nodo de los valores y se une con el nodo de insert
        if self.lista_valores is not None:
            contador[0] += 1
            id_nodo_valores = hash("VALUES" + str(contador[0]))
            label_valores = "\"{}\"[label=\"{}\"];\n".format(id_nodo_valores, "VALUES")
            union_valores = "\"{}\"->\"{}\";\n".format(id_nodo_insert, id_nodo_valores)
            result += label_valores + union_valores

            for valor in self.lista_valores:
                result += valor.GraficarArbol(id_nodo_valores, contador)

        return result
