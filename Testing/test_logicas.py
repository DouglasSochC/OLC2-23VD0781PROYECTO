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
SELECT (1<2 && 2>1);
SELECT (1>4 && 2>4);
SELECT (1<4 || 2>4);
SELECT (1>3 || 2>4);
SELECT !(1<2);
SELECT !(1>2);
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)

