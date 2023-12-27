class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError, RetornoCorrecto, RetornoMultiplesInstrucciones

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
DECLARE @texto NCHAR(2); -- EXITO
SET @texto = "ab";

IF (@texto == "ab")
BEGIN
    DECLARE @funciono AS INT;
    INSERT INTO producto (id, nombre) VALUES (1000, "THEN");
    SELECT * FROM producto;
END
ELSE
BEGIN
    DECLARE @no_funciono AS INT;
    INSERT INTO producto (id, nombre) VALUES (1001, "ELSE");
    SELECT * FROM producto;
END
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
            elif isinstance(res, RetornoCorrecto) and res.msg is None:
                pass
            elif isinstance(res, RetornoMultiplesInstrucciones):
                for mensaje in res.arreglo_mensajes:
                    print(mensaje)
                for arreglo in res.arreglo_arreglos:
                    print(arreglo)
            else:
                print(res)

