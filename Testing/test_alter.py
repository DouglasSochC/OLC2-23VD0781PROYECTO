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
ALTER TABLE jugador add column fecha DATE NOT NULL, test INT; -- ERROR: No se puede agregar la restriccion NOT NULL
ALTER TABLE tabla1 add column fecha DATE, test INT; -- ERROR: No existe la tabla
ALTER TABLE jugador add column fecha DATE, id BIT; -- ERROR: Ya existe la columna ID
ALTER TABLE jugador ADD column fecha DATE, fecha_exacta DATETIME; -- EXITO

Alter table tabla1 drop column columna1; -- ERROR: No existe la tabla
Alter table jugador drop column columna1; -- ERROR: No existe la columna
alter table tipo_producto drop column id; -- ERROR: El ID esta siendo referenciado a otra tabla
Alter table jugador drop column nombre; -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print(res)

