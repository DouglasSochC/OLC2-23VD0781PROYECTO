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
DECLARE @texto NCHAR(1); -- EXITO
SET @texto = "ab"; -- ERROR: Se excede la dimension

DECLARE @hola DATETIME; -- EXITO
DECLARE @hola DATETIME; -- ERROR: Ya esta instanciada el nombre
SET @hola = "123"; -- ERROR: Tipo de dato
SET @hola = HOY(); -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)
