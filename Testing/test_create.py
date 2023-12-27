class BaseDatosWrapper:
    def __init__(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Parser.tablas.tabla_simbolo import TablaDeSimbolos
from Parser.abstract.retorno import RetornoError

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
CREATE PROCEDURE procedimiento_test(@aumento int, @fecha date, @texto nvarchar(10))
AS
BEGIN
    DECLARE @var nvarchar(100); -- EXITO
    SET @var = 1; -- EXITO
    INSERT INTO tipo_producto (id / 2 + "hola mundo", nombre, descripcion) VALUES (1, @hola, "Productos electronicos"); -- EXITO
    INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (1, "Electronico", "Productos electronicos"); -- EXITO
    DELETE FROM tipo_producto WHERE id = "1" and hola >= 1 and test <= 1; -- EXITO
    DELETE FROM tipo_producto; -- EXITO
    UPDATE producto SET nombre = 'TESTING', campo_x = 'Hola :D' WHERE id_tipo_producto = 1; -- ERROR: No existe el campo 'campo_x'
    UPDATE producto SET nombre = 'NUEVO NOMBRE' WHERE id = @aumento; -- CORRECTO
    SELECT * FROM producto;
    SELECT producto.id FROM producto;
    SELECT id, nombre, total FROM producto, tipo_producto WHERE producto.id_tipo_producto > "2"; -- ERROR: Diferentes tipos de dato
    SELECT producto.id * 2 + producto.id as testing, tipo_producto.id FROM producto, tipo_producto, jugador WHERE producto.id_tipo_producto = tipo_producto.id AND producto.id = jugador.id; -- EXITO
    -- SELECT (1+2) * 3 + ("1") + "ab";
    SELECT HOY();

    DECLARE @cantidad INT; -- EXITO
    SET @cantidad = 0;

    WHILE (@cantidad < 10)
    BEGIN
        SELECT CONCATENA('Ciclo: ', @cantidad);
        SET @cantidad = @cantidad + 1;
    END
END;
CREATE FUNCTION funcion_test(@aumento int, @fecha date, @texto nvarchar(10))
RETURN INT
AS
BEGIN
    DECLARE @var nvarchar(100); -- EXITO
    SET @var = 1; -- EXITO
END;
CREATE FUNCTION impuesto(@total AS DECIMAL, @mensaje AS NVARCHAR(100))
RETURN INT
AS
BEGIN
    SET @total = @total * 0.12;
    SET @mensaje = SUBSTRAER(@mensaje, 1, 3);
    IF (@total > 100) THEN
        RETURN concatena(@total);
    ELSE
        RETURN concatena(@mensaje, @total);
    END IF;
END;
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_1, ts_global_1)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)

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
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)