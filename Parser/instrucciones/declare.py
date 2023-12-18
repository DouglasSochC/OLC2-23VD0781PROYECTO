from Parser.expresiones.tipo_dato import Tipo_Dato
from Parser.tablas.tabla_simbolo import Simbolo
from ..abstract.instrucciones import Instruccion
from ..abstract.retorno import TIPO_DATO, TIPO_TOKEN, RetornoError, RetornoTipoDato
from ..expresiones.identificador import Identificador

class Declare(Instruccion):

    def __init__(self, id_nodo: int, identificador: Identificador, tipo_dato: RetornoTipoDato):
        self.id_nodo = id_nodo
        self.identificador = identificador
        self.tipo_dato = tipo_dato
 

    def Ejecutar(self, base_datos, entorno):
        id = entorno.obtener(self.id_nodo)
        if id is None:  
            simbolo = Simbolo(self.id_nodo, self.tipo_dato, TIPO_TOKEN.VARIABLE, self.identificador, entorno.entorno)
            entorno.agregar(simbolo)    
        else:
            return RetornoError("ERROR: YA HAY DECLARADA UNA VARIABLE CON EL MISMO NOMBRE")
    def GraficarArbol(self, id_padre):
        label_encabezado =  "\"{}\"[label=\"{}\"];\n".format(self.id_nodo, "DECLARE")
        constr_tipo_dato = self.tipo_dato.GraficarArbol(self.id_nodo)
        constr_identificador = self.identificador.GraficarArbol(self.id_nodo)
        return label_encabezado + constr_identificador + constr_tipo_dato