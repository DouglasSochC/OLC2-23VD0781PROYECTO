from ..abstract.instrucciones import Instruccion
from ..expresiones.identificador import Identificador
from Funcionalidad.ddl import DDL

class Drop(Instruccion):

    def __init__(self, id_nodo, tipo_eliminacion: any, identificador: any):
        self.id_nodo = id_nodo
        self.tipo_eliminacion = tipo_eliminacion
        self.identificador = identificador

    # TODO: Falta implementar lo siguiente
        # Eliminar un procedimiento
        # Eliminar una funcion
    def Ejecutar(self, base_datos, entorno):
        print("Ejecutando Drop")
    '''
        if base_datos.valor == "":
            return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("DROP")

        nombre = self.identificador.Ejecutar(base_datos, entorno).identificador

        dll = DDL()
        respuesta = None
        if self.tipo_eliminacion == 'database':
            respuesta = dll.eliminar_base_de_datos(nombre)
            if nombre == base_datos.valor:
                base_datos.valor = ""
        elif self.tipo_eliminacion == 'table':
            respuesta = dll.eliminar_tabla(base_datos.valor, nombre)
        elif self.tipo_eliminacion == 'procedure':
            return "FALTA IMPLEMENTAR EL PROCEDURE"
        elif self.tipo_eliminacion == 'function':
            return "FALTA IMPLEMENTAR EL FUNCTION"

        if respuesta.success:
            return respuesta.valor
        else:
            return "ERROR: {}".format(respuesta.valor)
    '''
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DROP")
        label_tipo = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "T", self.tipo_eliminacion)
        union_tipo = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "T")
        result = label_encabezado + label_tipo + union_tipo
       
        if(isinstance(self.identificador, Identificador)):
            label_identificador = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "I", self.identificador.valor)
            union_identificador = "\"{}\"->\"{}\";\n".format(self.id_nodo, self.id_nodo + "I")
            result += label_identificador + union_identificador
        
        return result 