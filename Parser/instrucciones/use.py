from ..abstract.instrucciones import Instruccion
from Funcionalidad.administracion import Administracion

class Use(Instruccion):

    def __init__(self, identificador: str):
        self.identificador = identificador
        pass

    def Ejecutar(self, base_datos, entorno):

        nombre = self.identificador
        nombre = nombre[1:-1]

        administracion = Administracion()

        res_admin = administracion.verificar_existencia_bd(nombre)

        if res_admin.success:
            base_datos.valor = nombre
            return res_admin.valor
        else:
            return "ERROR: {}".format(res_admin.valor)

    def GraficarArbol(self, id_padre):
        pass