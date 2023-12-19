class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("")
print("BD utilizada antes del USE: {}".format(base_datos.valor))
instrucciones = parse(
'''
USE "bd_test"; -- ERROR: No existe la BD
USE "bd2"; -- EXITOSO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print(res)

print("BD utilizada despues del USE: {}".format(base_datos.valor))