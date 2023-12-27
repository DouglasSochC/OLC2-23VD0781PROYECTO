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
DECLARE @cantidad INT; -- EXITO
SET @cantidad = 0;

WHILE (@cantidad < 10)
BEGIN
    SELECT CONCATENA('Ciclo: ', @cantidad);
    SET @cantidad = @cantidad + 1;
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

