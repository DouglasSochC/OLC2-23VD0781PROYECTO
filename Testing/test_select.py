class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError, RetornoCorrecto

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper("bd1")
instrucciones = parse(
'''
-- SELECT A UNA O VARIAS TABLAS
SELECT id, nombre, total FROM producto, tipo_producto WHERE id = id; -- ERROR: Es ambiguo
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto > "2"; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = "2"; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.nombre; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM tipo_producto, producto, jugador WHERE jugador.id >= tipo_producto.id; -- ERROR: No se puede realizar una operacion relacional entre dos columnas.
SELECT producto.id FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.id AND producto.id = jugador.id; -- ERROR: La tabla jugador no se incluye en la clausula FROM
SELECT producto.id FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.id AND producto.hola > 10; -- ERROR: La columna hola no se encuentra en la tabla producto
SELECT producto.id FROM producto, tipo_producto, jugador WHERE producto.id_tipo_producto = tipo_producto.id AND jugador.id = producto.id; -- EXITO: No retorna nada debido a que la primera condicion no tiene jugador
SELECT producto.id FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.id AND producto.id > 10; -- EXITO
SELECT producto.id, producto.id * 2 /2 as calculo FROM producto; -- EXITO
SELECT (producto.id + producto.total) + 2 as total FROM producto; -- EXITO
SELECT producto.id * 2 + producto.id as testing FROM producto, tipo_producto, jugador WHERE producto.id_tipo_producto = tipo_producto.id AND producto.id = jugador.id; -- EXITO

-- SELECT A FUNCIONES NATIVAS
SELECT CONCATENA("HOLA","MUNDO","COMO","ESTAN", "1"); -- EXITO
SELECT SUBSTRAER("HOLA COMO ESTAN",1,1000); -- EXITO
SELECT (1+2) < 1; -- EXITO = 0
SELECT (1+2) > 1; -- EXITO = 1

-- SELECT A UNA O VARIAS TABLAS CON FUNCIONES NATIVAS
SELECT CONCATENA(producto.abc, "abc", " nombre: ", producto.nombre ) FROM producto; -- ERROR: No existe la columna abc
SELECT CONCATENA(test.id, "abc", " nombre: ", producto.nombre ) FROM producto; -- ERROR: No existe la tabla test
SELECT CONCATENA("id_producto: ", producto.id, " costo: ", producto.total) FROM producto; -- EXITO
SELECT CONCATENA("id_producto: ", producto.id, " nombre_producto: ", producto.nombre, " nombre_tipo_producto: ", tipo_producto.nombre) FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.id; -- EXITO
SELECT CONCATENA("id_producto: ", id, " nombre_producto: ", nombre) FROM producto; -- EXITO
SELECT SUBSTRAER(nombre, 1, 3) FROM producto;
SELECT SUBSTRAER(CONCATENA(producto.id, "ABCDEF"), 0, 3) FROM producto;
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
            elif isinstance(res, RetornoCorrecto):
                print(res.msg)
            else:
                print(res)
