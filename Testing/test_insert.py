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
INSERT INTO test (id, nombre) VALUES (1000, "Dummy"); -- ERROR: No existe la tabla
INSERT INTO producto (id, nombre, nombre) VALUES (1000, "Dummy", "Dummy"); -- ERROR: Doble parametro
INSERT INTO producto (nombre) VALUES ("Dummy"); -- ERROR: Llave primaria obligatoria
INSERT INTO tipo_producto (id, descripcion) VALUES (1, "Productos electronicos"); -- ERROR: Parametro nombre es obligatorio
INSERT INTO tipo_producto (id / 2, nombre, descripcion) VALUES (1, "Electronico", "Productos electronicos"); -- ERROR: Al definir los campos
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (1 + @var, "Test", "Hola mundo!"); -- ERROR: Al definir los valores

INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (1, "Electronico", "Productos electronicos"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (2, "Ropa", "Ropa de moda"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (3, "Libro", "Libros de diversos generos"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (4, "Alimenticio", "Productos alimenticios"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (5, "Hogar", "Articulos para el hogar"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (6, "Muebles", "Mobiliario para el hogar"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (7, "Juguetes", "Juguetes para todas las edades"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (8, "Electrodomesticos", "Aparatos electricos para el hogar"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (9, "Instrumentos Musicales", "Instrumentos para musicos aficionados y profesionales"); -- EXITO
INSERT INTO tipo_producto (id, nombre, descripcion) VALUES (10, "Articulos de Oficina", "Suministros para el lugar de trabajo"); -- EXITO

INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (1, 1, 299.99, "15-01-2023", "15-01-2023 08:30:00", "Smartphone", "Telefono inteligente de ultima generacion", 1); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (2, 1, 49.99, "20-01-2023", "20-01-2023 12:45:00", "Camiseta", "Camiseta de algodon con estampado", 2); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (3, 0, 15.00, "25-01-2023", "25-01-2023 18:20:00", "Ciencia Ficcion", "Libro de ciencia ficcion popular", 3); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (4, 1, 5.99, "05-02-2023", "05-02-2023 14:10:00", "Chocolate", "Barra de chocolate suizo", 4); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (5, 1, 199.99, "10-02-2023", "10-02-2023 09:00:00", "Sarten", "Sarten antiadherente de alta calidad", 5); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (6, 1, 129.99, "15-02-2023", "15-02-2023 16:30:00", "Auriculares Inalambricos", "Auriculares Bluetooth con cancelacion de ruido", 1); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (7, 1, 29.99, "20-02-2023", "20-02-2023 11:15:00", "Jeans", "Jeans clasicos de mezclilla", 2); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (8, 0, 8.50, "25-02-2023", "25-02-2023 19:45:00", "Historia Antigua", "Libro de historia antigua", 3); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (9, 1, 2.49, "05-03-2023", "05-03-2023 15:00:00", "Cereal", "Cereal integral para el desayuno", 4); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (10, 1, 39.99, "10-03-2023", "10-03-2023 10:30:00", "Lampara de Mesa", "Lampara de mesa con luz LED", 5); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (11, 1, 799.00, "15-03-2023", "15-03-2023 08:30:00", "Sofa", "Sofa comodo para la sala de estar", 6); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (12, 1, 19.99, "20-03-2023", "20-03-2023 12:45:00", "Rompecabezas", "Rompecabezas desafiante de 1000 piezas", 7); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (13, 1, 249.99, "25-03-2023", "25-03-2023 18:20:00", "Licuadora", "Licuadora potente para smoothies", 8); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (14, 1, 499.99, "05-04-2023", "05-04-2023 14:10:00", "Guitarra Acustica", "Guitarra para principiantes con cuerdas de nylon", 9); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (15, 1, 5.49, "10-04-2023", "10-04-2023 09:00:00", "Boligrafos", "Paquete de boligrafos de tinta negra", 10); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (16, 1, 129.99, "15-04-2023", "15-04-2023 16:30:00", "Aspiradora Robot", "Aspiradora inteligente con tecnologia de mapeo", 8); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (17, 1, 39.99, "20-04-2023", "20-04-2023 11:15:00", "Muñeca de Peluche", "Muñeca suave y adorable para niños", 7); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (18, 1, 24.99, "25-04-2023", "25-04-2023 19:45:00", "Cuaderno de Notas", "Cuaderno con tapa dura y paginas rayadas", 10); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (19, 1, 3.99, "05-05-2023", "05-05-2023 15:00:00", "Salsa Picante", "Botella de salsa picante de edicion limitada", 4); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (20, 1, 79.99, "10-05-2023", "10-05-2023 10:30:00", "Escritorio", "Escritorio moderno para la oficina en casa", 6); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (21, 1, 14.99, "15-05-2023", "15-05-2023 08:30:00", "Pelota de Futbol", "Pelota oficial para partidos de futbol", 7); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (22, 1, 129.99, "20-05-2023", "20-05-2023 12:45:00", "Cafetera", "Cafetera programable para cafe fresco", 8); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (23, 1, 29.99, "25-05-2023", "25-05-2023 18:20:00", "Juego de Te", "Juego elegante de te para cuatro personas", 6); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (24, 1, 8.50, "05-06-2023", "05-06-2023 14:10:00", "Crema Hidratante", "Crema hidratante para piel seca", 4); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (25, 1, 149.99, "10-06-2023", "10-06-2023 09:00:00", "Teclado Musical", "Teclado electronico para aprender a tocar", 9); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (26, 1, 49.99, "15-06-2023", "15-06-2023 16:30:00", "Lampara de Pie", "Lampara de pie con regulador de intensidad", 5); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (27, 1, 12.99, "20-06-2023", "20-06-2023 11:15:00", "Romance Historico", "Libro de romance ambientado en el pasado", 3); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (28, 1, 6.99, "25-06-2023", "25-06-2023 19:45:00", "Calculadora Cientifica", "Calculadora avanzada para estudiantes", 10); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (29, 1, 2.99, "05-07-2023", "05-07-2023 15:00:00", "Yogurt", "Envase de yogur con sabores variados", 4); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (30, 1, 299.99, "10-07-2023", "10-07-2023 10:30:00", "Mesa de Centro", "Mesa de centro elegante para la sala de estar", 6); -- EXITO
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (30, 1, 299.99, "10-07-2023", "10-07-2023 10:30:00", "Mesa de Centro", "Mesa de centro elegante para la sala de estar", 6); -- ERROR: No se puede duplicar una llave primaria
INSERT INTO producto (id, esta_bueno, total, fecha, fecha_hora, nombre, descripcion, id_tipo_producto)
VALUES (300, 1, 299.99, "10-07-2023", "10-07-2023 10:30:00", "Mesa de Centro", "Mesa de centro elegante para la sala de estar", 1000); -- ERROR: No existe la llave foranea

INSERT INTO jugador (id, nombre, puntaje) VALUES (1, "Juan Pérez", 85);
INSERT INTO jugador (id, nombre, puntaje) VALUES (2, "María Gómez", 92);
INSERT INTO jugador (id, nombre, puntaje) VALUES (3, "Carlos Rodríguez", 78);
INSERT INTO jugador (id, nombre, puntaje) VALUES (4, "Ana López", 95);
INSERT INTO jugador (id, nombre, puntaje) VALUES (5, "Pedro Ramirez", 88);
INSERT INTO jugador (id, nombre, puntaje) VALUES (6, "Luisa Fernández", 90);
INSERT INTO jugador (id, nombre, puntaje) VALUES (7, "Miguel Torres", 75);
INSERT INTO jugador (id, nombre, puntaje) VALUES (8, "Isabel Garcia", 82);
INSERT INTO jugador (id, nombre, puntaje) VALUES (9, "David Martinez", 89);
INSERT INTO jugador (id, nombre, puntaje) VALUES (10, "Laura Perez", 94);
INSERT INTO jugador (id, nombre, puntaje) VALUES (11, "Carlos Herrera", 80);
INSERT INTO jugador (id, nombre, puntaje) VALUES (12, "Elena Ruiz", 91);
INSERT INTO jugador (id, nombre, puntaje) VALUES (13, "Juan Carlos Morales", 87);
INSERT INTO jugador (id, nombre, puntaje) VALUES (14, "Beatriz Soto", 93);
INSERT INTO jugador (id, nombre, puntaje) VALUES (15, "Francisco Jiménez", 79);
INSERT INTO jugador (id, nombre, puntaje) VALUES (16, "Sofía Navarro", 96);
INSERT INTO jugador (id, nombre, puntaje) VALUES (17, "Javier Castro", 84);
INSERT INTO jugador (id, nombre, puntaje) VALUES (18, "Marina Ortega", 88);
INSERT INTO jugador (id, nombre, puntaje) VALUES (19, "Ricardo Herrera", 97);
INSERT INTO jugador (id, nombre, puntaje) VALUES (20, "Eva Gutierrez", 83);
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
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (1, "Cien años de soledad", "Gabriel Garcia Marquez", 1967, "Realismo magico");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (2, "1984", "George Orwell", 1949, "Distopia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (3, "To Kill a Mockingbird", "Harper Lee", 1960, "Ficcion");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (4, "The Great Gatsby", "F. Scott Fitzgerald", 1925, "Ficcion");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (5, "The Catcher in the Rye", "J.D. Salinger", 1951, "Ficcion");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (6, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 1997, "Fantasia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (7, "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (8, "The Da Vinci Code", "Dan Brown", 2003, "Misterio");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (9, "Brave New World", "Aldous Huxley", 1932, "Distopia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (10, "The Lord of the Rings", "J.R.R. Tolkien", 1954, "Fantasia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (11, "Pride and Prejudice", "Jane Austen", 1813, "Romance");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (12, "The Alchemist", "Paulo Coelho", 1988, "Ficcion");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (13, "The Girl with the Dragon Tattoo", "Stieg Larsson", 2005, "Misterio");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (14, "The Hunger Games", "Suzanne Collins", 2008, "Distopia");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (15, "The Shining", "Stephen King", 1977, "Terror");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (16, "The Fault in Our Stars", "John Green", 2012, "Romance");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (17, "Gone with the Wind", "Margaret Mitchell", 1936, "Historico");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (18, "One Hundred Years of Solitude", "Gabriel Garcia Marquez", 1967, "Realismo magico");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (19, "The Odyssey", "Homer", 800, "epico");
INSERT INTO Libros (id, Titulo, Autor, anio_publicacion, Genero) VALUES (20, "Sapiens: A Brief History of Humankind", "Yuval Noah Harari", 2011, "Historia");

INSERT INTO Usuarios (id, Nombre, Email) VALUES (1, "Juan Perez", "juan.perez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (2, "Maria Gomez", "maria.gomez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (3, "Carlos Rodriguez", "carlos.rodriguez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (4, "Ana Lopez", "ana.lopez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (5, "Pedro Ramirez", "pedro.ramirez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (6, "Luisa Fernandez", "luisa.fernandez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (7, "Miguel Torres", "miguel.torres@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (8, "Isabel Garcia", "isabel.garcia@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (9, "David Martinez", "david.martinez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (10, "Laura Perez", "laura.perez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (11, "Carlos Herrera", "carlos.herrera@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (12, "Elena Ruiz", "elena.ruiz@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (13, "Juan Carlos Morales", "juan.carlos.morales@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (14, "Beatriz Soto", "beatriz.soto@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (15, "Francisco Jimenez", "francisco.jimenez@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (16, "Sofia Navarro", "sofia.navarro@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (17, "Javier Castro", "javier.castro@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (18, "Marina Ortega", "marina.ortega@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (19, "Ricardo Herrera", "ricardo.herrera@example.com");
INSERT INTO Usuarios (id, Nombre, Email) VALUES (20, "Eva Gutierrez", "eva.gutierrez@example.com");

INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (1, 1, 1, "01-01-2023", "15-01-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (2, 2, 2, "01-02-2023", "15-02-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (3, 3, 3, "01-03-2023", "15-03-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (4, 4, 4, "01-04-2023", "15-04-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (5, 5, 5, "01-05-2023", "15-05-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (6, 6, 6, "01-06-2023", "15-06-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (7, 7, 7, "01-07-2023", "15-07-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (8, 8, 8, "01-08-2023", "15-08-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (9, 9, 9, "01-09-2023", "15-09-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (10, 10, 10, "01-10-2023", "15-10-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (11, 11, 11, "01-11-2023", "15-11-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (12, 12, 12, "01-12-2023", "15-12-2023");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (13, 13, 13, "01-01-2024", "15-01-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (14, 14, 14, "01-02-2024", "15-02-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (15, 15, 15, "01-03-2024", "15-03-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (16, 16, 16, "01-04-2024", "15-04-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (17, 17, 17, "01-05-2024", "15-05-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (18, 18, 18, "01-06-2024", "15-06-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (19, 19, 19, "01-07-2024", "15-07-2024");
INSERT INTO Prestamos (id, id_libro, id_usuario, fecha_prestamo, fecha_devolucion) VALUES (20, 20, 20, "01-08-2024", "15-08-2024");
''')

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:

    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos_2, ts_global_2)
            print("ERROR: {}".format(res.msg) if isinstance(res, RetornoError) else res.msg)