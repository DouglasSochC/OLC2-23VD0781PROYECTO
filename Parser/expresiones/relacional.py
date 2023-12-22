from ..abstract.expresiones import Expresion
from ..abstract.retorno import RetornoArreglo, RetornoLiteral, RetornoError, TIPO_DATO

class Relacional(Expresion):

    def __init__(self,id_nodo, expresion_izquierda: RetornoArreglo | RetornoLiteral, operador: str, expresion_derecha: RetornoArreglo | RetornoLiteral):
        self.id_nodo = id_nodo
        self.expresion_izquierda = expresion_izquierda
        self.operador = operador
        self.expresion_derecha = expresion_derecha

    def Ejecutar(self, base_datos, entorno):

        exp_izq = self.expresion_izquierda.Ejecutar(base_datos, entorno)
        exp_der = self.expresion_derecha.Ejecutar(base_datos, entorno)

        if isinstance(exp_izq, RetornoError):
            return exp_izq
        elif isinstance(exp_der, RetornoError):
            return exp_der

        if isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoArreglo):

            if self.operador == "==":
                return RetornoError("No se puede utilizar el operador '==' para aplicar una condicion.")

            return RetornoError("No se puede realizar una operacion relacional entre dos columnas.")

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoLiteral):

            if self.operador == "==":
                return RetornoError("No se puede utilizar el operador '==' para aplicar una condicion.")

            # Almacena todos los datos que cumplen con la condicion (lo importante aqui es que posee el indice de cada dato)
            respuesta = []

            # Se busca en la tabla de simbolos el nombre de la variable en el caso que ocurra una condicion
            simbolo = entorno.obtener("condicion")
            arreglo = None
            if simbolo is None:
                arreglo = exp_izq
            else:
                arreglo = RetornoArreglo(exp_izq.identificador, exp_izq.tabla_del_identificador, simbolo.valor)

            for item in arreglo.lista:

                if "{}.{}".format(arreglo.tabla_del_identificador, arreglo.identificador) not in item:
                    continue

                valor_item = item["{}.{}".format(arreglo.tabla_del_identificador, arreglo.identificador)]
                if valor_item['tipado'] != exp_der.tipado:
                    return RetornoError("No se puede realizar la operacion relacional '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(arreglo.identificador, self.operador, ('"{}"'.format(exp_der.valor) if exp_der.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_der.valor)))

                if valor_item['valor'] is not None:
                    comparacion = eval(f"valor_item['valor'] {self.operador} exp_der.valor")
                    if comparacion:
                        respuesta.append(item)

            return RetornoArreglo(arreglo.identificador, arreglo.tabla_del_identificador, respuesta, arreglo.alias)

        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoArreglo):
            return RetornoError("La operación relacional '{} {} {}' es invalida.".format(exp_izq.valor, self.operador, exp_der.identificador))
        elif isinstance(exp_izq, RetornoLiteral) and isinstance(exp_der, RetornoLiteral):

            if exp_izq.tipado != exp_der.tipado:
                return RetornoError("No se puede realizar la operacion relacional '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(exp_izq.valor, self.operador, ('"{}"'.format(exp_der.valor) if exp_der.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_der.valor)))

            resultado = eval(f"exp_izq.valor {self.operador} exp_der.valor")
            resultado = 1 if resultado else 0
            return RetornoLiteral(resultado, TIPO_DATO.BIT)
        else:
            return RetornoError("La operación relacional con '{}' es invalida".format(self.operador))

    def GraficarArbol(self, id_padre):
        id_nodo_actual = self.id_nodo if self.id_nodo is not None else id_padre
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual, "RELACIONAL")
        union_hijo_izquierdo = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_izquierda.id_nodo)
        union_hijo_derecho = "\"{}\"->\"{}\";\n".format(id_nodo_actual, self.expresion_derecha.id_nodo)
        resultado_izquierda = self.expresion_izquierda.GraficarArbol(self.id_nodo)
        label_operador = "\"{}\"[label=\"{}\"];\n".format(id_nodo_actual + "Op", self.operador)
        union_enca_operador = "\"{}\"->\"{}\";\n".format(id_nodo_actual, id_nodo_actual + "Op")
        resultado_derecha = self.expresion_derecha.GraficarArbol(self.id_nodo)
        return label_encabezado + union_hijo_izquierdo  + resultado_izquierda + label_operador +union_enca_operador +resultado_derecha + union_hijo_derecho