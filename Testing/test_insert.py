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
INSERT INTO producto (id, nombre, nombre) VALUES (1000, "Dummy", "Dummy");
INSERT INTO producto (nombre) VALUES ("Dummy");
INSERT INTO producto (id, nombre) VALUES (250, "Dummy");
INSERT INTO producto (id, nombre) VALUES (250, "Dummy");
INSERT INTO producto (id, nombre, id_tipo_producto) VALUES (251, "Dummy", 2);
INSERT INTO producto (id, nombre, id_tipo_producto) VALUES (251, "Dummy", 1);
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print(res)

