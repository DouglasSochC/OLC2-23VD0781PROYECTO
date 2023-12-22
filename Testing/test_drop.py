class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
DROP TABLE producto1; -- ERROR: Esta tabla no existe
DROP TABLE tipo_producto; -- ERROR: No se puede eliminar ya que tiene algunos ID's en uso en otras tablas
DROP TABLE producto; -- EXITO
DROP PROCEDURE abc_test; -- ERROR: No existe el procedimiento
DROP PROCEDURE procedimiento_test; -- EXITO
DROP FUNCTION abc_test; -- ERROR: No existe la funcion
DROP FUNCTION funcion_test; -- ERROR: No existe la funcion
DROP DATABASE bd3; -- ERROR: No existe la BD
DROP DATABASE bd1; -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)
