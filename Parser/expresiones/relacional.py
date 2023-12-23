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

            return RetornoError("No se puede realizar una operacion relacional entre arreglos de datos.")

        elif isinstance(exp_izq, RetornoArreglo) and isinstance(exp_der, RetornoLiteral):

            if self.operador == "==":
                return RetornoError("No se puede utilizar el operador '==' para aplicar una condicion.")

            # Almacena todos los datos que cumplen con la condicion (lo importante aqui es que posee el indice de cada dato)
            respuesta = []
            arreglo_izquierdo = None
            llave_izquierda = None

            # Se basa en los arreglos exp_izq y exp_der para realizar la operacion aritmetica estos arreglos deben tener una misma dimension y deben de ser la misma tabla
            simbolo = entorno.obtener("condicion")
            if simbolo is None:
                # Se setean los valores que seran utilizados para realizar el calculo
                arreglo_izquierdo = exp_izq
                llave_izquierda = "{}.{}".format(arreglo_izquierdo.tabla_del_identificador, arreglo_izquierdo.identificador) if arreglo_izquierdo.identificador is not None else "auxiliar"
            else:
                # Se setean los valores que seran utilizados para realizar el calculo
                llave_izquierda = "{}.{}".format(exp_izq.tabla_del_identificador, exp_izq.identificador) if exp_izq.identificador is not None else "auxiliar"
                arreglo_izquierdo = exp_izq if llave_izquierda == "auxiliar" else simbolo.valor

            for llave, tupla in enumerate(arreglo_izquierdo.lista):

                # Se verifica que existan las llaves
                if llave_izquierda not in tupla:
                    continue

                # Se obtiene los valores que seran utilizados para realizar el calculo
                valor_izquierdo = arreglo_izquierdo.lista[llave][llave_izquierda]
                valor_derecho = exp_der

                # Se verifica si el valor es None para no realizar la operacion
                if valor_izquierdo['valor'] is None:
                    continue

                # Se verifica si se puede realizar la operacion segun el dominante
                dominante = None
                if valor_izquierdo['tipado'] == TIPO_DATO.DATE and valor_derecho.tipado == TIPO_DATO.DATE:
                    dominante = TIPO_DATO.DATE
                elif valor_izquierdo['tipado'] == TIPO_DATO.DATETIME and valor_derecho.tipado == TIPO_DATO.DATETIME:
                    dominante = TIPO_DATO.DATETIME
                else:
                    dominante = self.DominanteSuma(valor_izquierdo['tipado'], valor_derecho.tipado)

                if dominante == TIPO_DATO.NULL:
                    return RetornoError("No se puede realizar la operacion relacional '{} {} {}' debido a que no poseen el mismo tipo de dato.".format(valor_izquierdo['valor'], self.operador, ('"{}"'.format(exp_der.valor) if exp_der.tipado in (TIPO_DATO.NCHAR, TIPO_DATO.NVARCHAR) else exp_der.valor)))

                # Valores de la llave auxiliar
                auxiliar = 0

                try:
                    auxiliar = eval(f"valor_izquierdo['valor'] {self.operador} valor_derecho.valor")
                except Exception as e:
                    return RetornoError("No se puede realizar la operacion aritmetica '{} {} {}' debido a los valores de los operandos.".format(valor_izquierdo['valor'], self.operador, valor_derecho.valor))

                if auxiliar:
                    tupla_homologacion = {}
                    tupla_homologacion.update(tupla)
                    respuesta.append(tupla_homologacion)

            return RetornoArreglo(None, arreglo_izquierdo.tabla_del_identificador, respuesta, None)

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