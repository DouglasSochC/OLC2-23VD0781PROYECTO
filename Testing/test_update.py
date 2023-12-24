class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError

ts_global_1 = TablaDeSimbolos()
base_datos_1 = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
UPDATE producto SET nombre = 'TESTING', campo_x = 'Hola :D' WHERE id_tipo_producto = 1; -- ERROR: No existe el campo 'campo_x'
UPDATE producto SET nombre = 'NUEVO NOMBRE', id_tipo_producto = 20 WHERE id_tipo_producto = 1; -- ERROR: No existe el valor 100 en la tabla 'tipo_producto'
UPDATE test SET nombre = 'NUEVO NOMBRE' WHERE id = 1; -- ERROR: No existe la tabla 'test'
UPDATE producto SET nombre = 1 WHERE id = 1; -- ERROR: El tipo de dato de la columna 'nombre' no es el mismo que el valor a actualizar
UPDATE producto SET nombre = 'NUEVO NOMBRE' WHERE id = 1; -- CORRECTO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_1, ts_global_1)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)
