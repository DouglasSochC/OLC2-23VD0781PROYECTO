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
/*EXEC test_procedure 1, 2, 3; -- ERROR: No se encuentra en la base de datos
EXEC procedimiento_test 1,2,3,4; -- ERROR: La cantidad de parametros no coincide con la cantidad de campos del procedimiento 'procedimiento_test'.
EXEC procedimiento_test 1; -- ERROR: La cantidad de parametros no coincide con la cantidad de campos del procedimiento 'procedimiento_test'.
EXEC procedimiento_test 1,2,3; -- ERROR: Tipos de datos incorrectos*/
EXEC procedimiento_test 1, '01-01-2020', 'hola mundo'; -- ERROR: En la semantica de la funcion
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_1, ts_global_1)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)
