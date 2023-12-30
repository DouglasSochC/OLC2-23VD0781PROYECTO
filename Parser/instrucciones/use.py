from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError, RetornoCorrecto
from Funcionalidad.administracion import Administracion

class Use(Instruccion):

    def __init__(self, texto: str):
        self.texto = texto

    def Ejecutar(self, base_datos, entorno):

        # Se verifica que no se este utilizando este 'USE' dentro de la creacion de un procedimiento o funcion
        construccion = entorno.obtener("construir_procedimiento")
        construccion = construccion if construccion is not None else entorno.obtener("construir_funcion")
        if construccion is not None:
            return RetornoError("No puede utilizar el comando 'USE' dentro de la creacion de un PROCEDURE o FUNCTION")

        nombre = self.texto

        administracion = Administracion()

        res_admin = administracion.verificar_existencia_bd(nombre)

        if res_admin.success:
            base_datos.valor = nombre
            return RetornoCorrecto(res_admin.valor)
        else:
            return RetornoError(res_admin.valor)

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_use = hash("USE" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_use, "USE")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_use)
        result = label_encabezado + union

        # Se crea el nodo del texto y se une con el nodo de use
        contador[0] += 1
        id_nodo_texto = hash("TEXTO" + str(contador[0]))
        label_texto = "\"{}\"[label=\"{}\"];\n".format(id_nodo_texto, self.texto)
        union_texto = "\"{}\"->\"{}\";\n".format(id_nodo_use, id_nodo_texto)
        result += label_texto + union_texto

        return result
