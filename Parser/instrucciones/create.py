from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import RetornoError
from ..expresiones.identificador import Identificador
from ..expresiones.campo_table import Campo_Table
from Funcionalidad.ddl import DDL

class Create(Instruccion):

    def __init__(self, id_nodo,instruccion: str, identificador: Identificador, campos_table: list[Campo_Table]):
        self.id_nodo = id_nodo
        self.instruccion = instruccion
        self.identificador = identificador
        self.campos_table = campos_table

    # TODO: Falta implementar lo siguiente
        # Crear un procedimiento
        # Crear una funcion
    def Ejecutar(self, base_datos, entorno):
        ''''
        ddl = DDL()

        # Se obtiene el nombre
        res_identificador = self.identificador.Ejecutar(base_datos, entorno)
        if isinstance(res_identificador, RetornoError):
            return res_identificador.msg
        nombre = res_identificador.identificador

        if self.instruccion == 'database':
            res = ddl.crear_base_de_datos(nombre)
            return res.valor if res.success else "ERROR: {}".format(res.valor)
        else:

            if base_datos.valor == "":
                return "Para ejecutar la consulta '{}', es necesario seleccionar una base de datos.".format("CREATE")

            if self.instruccion == 'table':

                campos = [] # En esta variable se almacenan todos los campos que se definiran al construir la tabla
                for campo in self.campos_table:

                    res_ejecutar = campo.Ejecutar(base_datos, entorno)
                    if isinstance(res_ejecutar, RetornoError):
                        return res_ejecutar.msg

                    campos.append(res_ejecutar)

                res = ddl.crear_tabla(base_datos.valor, nombre, campos)
                return res.valor if res.success else "ERROR: {}".format(res.valor)
        '''
    def GraficarArbol(self, id_padre):
        #TODO: Falta implementar lo siguiente
        # GRAFICAR UN PROCEDIMIENTO
        # GRAFICAR UNA FUNCION
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "CREATE")
        label_instruccion = "\"{}\"[label=\"{}\"];\n".format(self.id_nodo + "CR", self.instruccion)
        union_encabezado_instruccion = "\"{}\" -> \"{}\";\n".format(self.id_nodo, self.id_nodo + "CR")
        label_identificador = self.identificador.GraficarArbol(self.id_nodo)
        result = label_encabezado + label_instruccion + union_encabezado_instruccion + label_identificador

        if isinstance(self.campos_table, list) and self.campos_table:
            primer_elemento = self.campos_table[0]
            if isinstance(primer_elemento, Campo_Table):
                for campo in self.campos_table:
                    label_campo = campo.GraficarArbol(self.id_nodo)
                    union_tipo_accion_campo = "\"{}\" -> \"{}\";\n".format(self.id_nodo, campo.id_nodo)
                    result += label_campo + union_tipo_accion_campo
            else:
                label_tipo_dato = self.campos_table.GraficarArbol(self.id_nodo)
                result += label_tipo_dato 
           
        return result
