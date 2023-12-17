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
CREATE DATABASE bd1; -- EXITO
CREATE DATABASE bd1; -- ERROR: Ya existe la base de datos
CREATE DATABASE bd2; -- EXITO
CREATE TABLE producto (
    id INT PRIMARY KEY,
    esta_bueno BIT,
    total DECIMAL,
    fecha DATE,
    fecha_hora DATETIME,
    nombre NCHAR(20) NOT NULL,
    descripcion NVARCHAR(100),
    id_tipo_producto INT REFERENCES tipo_producto (id)
); -- ERROR: No existe la referencia
CREATE TABLE tipo_producto (
    id INT PRIMARY KEY,
    nombre NCHAR(20) NOT NULL,
    descripcion NVARCHAR(100)
); -- EXITO
CREATE TABLE producto (
    id INT PRIMARY KEY,
    esta_bueno BIT,
    total DECIMAL,
    fecha DATE,
    fecha_hora DATETIME,
    nombre NCHAR(20) NOT NULL,
    descripcion NVARCHAR(100),
    id_tipo_producto INT REFERENCES tipo_producto (id)
); -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            print(res)

