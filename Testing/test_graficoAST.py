class BaseDatosWrapper:
    def _init_(self, valor):
        self.valor = valor

# Para realizar el analisis
from Parser.parser import parse

# Utilidades
from Funcionalidad.util import Respuesta
from Parser.tablas.tabla_simbolo import TablaDeSimbolos

ts_global = TablaDeSimbolos()
base_datos = BaseDatosWrapper()
instrucciones = parse(
'''
   CREATE TABLE accounts (
	user_id INT PRIMARY KEY,
	username NVARCHAR ( 50 ) NOT NULL,
	password NVARCHAR ( 50 ) NOT NULL
	
);

''')
'''
DECLARE tabla1.columna INT;
DECLARE var1 DATE;
DECLARE @var2 DATETIME;
DECLARE var3 AS var4 NVARCHAR(2);
USE bd1;
DECLARE var1 DATE;
DECLARE @var2 DATETIME;
DROP TABLE tabla1;
DROP DATABASE bd1;
drop column tipotarjeta
ADD COLUMN tipotarjeta NVARCHAR(20) PRIMARY KEY
ALTER TABLE tabla1 ADD COLUMN tipotarjeta NVARCHAR(20) PRIMARY KEY;
truncate table tbdetallefactura;
3 > 3 && 3 < 7
CAST(@NCHAR AS INT)
EXEC varaibles ( master );
concatena("hola", "mundo")
CREATE DATABASE bd1;


INSERT INTO tbvalores (id,nombre,bandera) VALUES(1,"JULIO LOPEZ",1);
'''

# Se revisa que se haya obtenido una instrucciones
if instrucciones is not None:
    
    if isinstance(instrucciones, str):
        print("SALIDA STRING: {}".format(instrucciones))
    else:
        for instr in instrucciones:
            res = instr.Ejecutar(base_datos, ts_global)
            graficar = instr.GraficarArbol(None)
            print(graficar)