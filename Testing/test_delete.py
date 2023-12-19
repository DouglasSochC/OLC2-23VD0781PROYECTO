class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(

'''
DELETE FROM producto1 WHERE id > 100; -- ERROR: No existe la tabla en la BD
DELETE FROM producto WHERE test < 100; -- ERROR: No existe la columna 'test' en la tabla
DELETE FROM tipo_producto WHERE id <= 5; -- ERROR: Este ID esta siendo utilizado en otra tabla
DELETE FROM producto WHERE id <= 10; -- EXITO 10 ELIMINACIONES
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print(res)

