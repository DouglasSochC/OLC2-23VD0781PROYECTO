class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos

ts_global_1 = TablaDeSimbolos()
base_datos_1 = BaseDatosWrapper("bd1")
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
    nombre NCHAR(200) NOT NULL,
    descripcion NVARCHAR(1000),
    id_tipo_producto INT REFERENCES tipo_producto (id)
); -- ERROR: No existe la referencia
CREATE TABLE tipo_producto (
    id INT PRIMARY KEY,
    nombre NCHAR(200) NOT NULL,
    descripcion NVARCHAR(1000)
); -- EXITO
CREATE TABLE producto (
    id INT PRIMARY KEY,
    esta_bueno BIT,
    total DECIMAL,
    fecha DATE,
    fecha_hora DATETIME,
    nombre NCHAR(200) NOT NULL,
    descripcion NVARCHAR(1000),
    id_tipo_producto INT REFERENCES tipo_producto (id)
); -- EXITO
CREATE TABLE jugador (
    id INT PRIMARY KEY,
    nombre NCHAR(200) NOT NULL,
    puntaje INT
); -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_1, ts_global_1)
            print(res)

ts_global_2 = TablaDeSimbolos()
base_datos_2 = BaseDatosWrapper("bd2")
instrucciones = parse(

'''
CREATE TABLE Libros (
    id INT PRIMARY KEY,
    titulo NVARCHAR(100),
    autor NVARCHAR(50),
    anio_publicacion INT,
    genero NVARCHAR(30)
); -- EXITO
CREATE TABLE Usuarios (
    id INT PRIMARY KEY,
    nombre NVARCHAR(50),
    email NVARCHAR(100)
); -- EXITO
CREATE TABLE Prestamos (
    id INT PRIMARY KEY,
    id_libro INT REFERENCES Libros(id),
    id_usuario INT REFERENCES Usuarios(id),
    fecha_prestamo DATE,
    fecha_devolucion DATE
); -- EXITO
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_2, ts_global_2)
            print(res)