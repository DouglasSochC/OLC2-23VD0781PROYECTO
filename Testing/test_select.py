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
SELECT id, nombre, total FROM producto, tipo_producto WHERE id = id; -- ERROR: Es ambiguo
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto > "2"; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = "2"; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.nombre; -- ERROR: Diferentes tipos de dato
SELECT id, nombre, total FROM tipo_producto, producto, jugador WHERE jugador.id >= tipo_producto.id; -- ERROR: No se puede realizar una operacion relacional entre dos columnas.
SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = tipo_producto.id; -- EXITO

-- SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto = 2; -- EXITOSO
-- SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto > 2; -- EXITO
-- SELECT id, nombre, total FROM tipo_producto, producto, jugador WHERE jugador.id >= 1 AND tipo_producto.id >= 1; -- EXITO
/* SELECT id, nombre, total FROM producto;
SELECT (id, total) FROM producto;
SELECT * FROM producto WHERE total > 130;
SELECT id, nombre FROM producto WHERE total > 130;
SELECT (id * 2 + 1, nombre) FROM producto WHERE total > 130;
SELECT CONCATENA("HOLA","MUNDO","COMO","ESTAN", "1");
SELECT CONCATENA(nombre, descripcion) FROM producto;
SELECT CONCATENA("A", "B"), nombre FROM tipo_producto;
SELECT CONCATENA("A", nombre) FROM tipo_producto;
SELECT CONCATENA(nombre, "B") FROM tipo_producto;
SELECT SUBSTRAER("HOLA COMO ESTAN",1,1000);
SELECT SUBSTRAER(nombre, 1, 3) FROM producto;
SELECT id, nombre, descripcion FROM producto WHERE SUBSTRAER(nombre, 1, 3) == "om";*/
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res)

