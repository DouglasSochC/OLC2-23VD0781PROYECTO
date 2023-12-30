from ..abstract.expresiones import Expresion

class Identificador(Expresion):

    def __init__(self, valor: str, referencia_tabla: str = None):
        self.valor = valor
        self.referencia_tabla = referencia_tabla

    def Ejecutar(self, base_datos, entorno):

        return {'identificador': self.valor, 'referencia_tabla': self.referencia_tabla}

    def GraficarArbol(self, id_nodo_padre: int, contador: list):

        # Se crea el nodo y se realiza la union con el padre
        contador[0] += 1
        id_nodo_identificador = hash("IDENTIFICADOR" + str(contador[0]))
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_identificador, "IDENTIFICADOR")
        union = "\"{}\"->\"{}\";\n".format(id_nodo_padre, id_nodo_identificador)
        result = label_encabezado + union

        # Se crea el nodo de la referencia de la tabla y se une con el nodo de identificador
        if self.referencia_tabla is not None:
            contador[0] += 1
            id_nodo_referencia_tabla = hash("REFERENCIA_TABLA" + str(contador[0]))
            label_referencia_tabla = "\"{}\"[label=\"{}\"];\n".format(id_nodo_referencia_tabla, self.referencia_tabla)
            union_referencia_tabla = "\"{}\"->\"{}\";\n".format(id_nodo_identificador, id_nodo_referencia_tabla)
            result += label_referencia_tabla + union_referencia_tabla

            # Se crea el nodo del punto y se une con el nodo de identificador
            contador[0] += 1
            id_nodo_punto = hash("PUNTO" + str(contador[0]))
            label_punto = "\"{}\"[label=\"{}\"];\n".format(id_nodo_punto, ".")
            union_punto = "\"{}\"->\"{}\";\n".format(id_nodo_identificador, id_nodo_punto)
            result += label_punto + union_punto

        # Se obtiene el nombre del identificador
        contador[0] += 1
        id_nodo_nombre_identificador = hash("NOMBRE_IDENTIFICADOR" + str(contador[0]))
        label_nombre_identificador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_nombre_identificador, self.valor)
        union_nombre_identificador = "\"{}\"->\"{}\";\n".format(id_nodo_identificador, id_nodo_nombre_identificador)
        result += label_nombre_identificador + union_nombre_identificador

        return result
