class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError, RetornoCorrecto, RetornoLiteral

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
DECLARE @var1 INT;
SET @var1 = 50;
SET @var1 = @var1 + 12;
return @var1;
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            if isinstance(res, RetornoError):
                print("ERROR: {}".format(res.msg))
            elif isinstance(res, RetornoCorrecto) and res.msg is not None:
                print(res.msg)
            elif isinstance(res, RetornoLiteral):
                print(res.valor)
