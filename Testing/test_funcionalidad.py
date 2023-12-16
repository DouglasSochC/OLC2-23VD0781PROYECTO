from Funcionalidad.ddl import DDL
from Funcionalidad.dml import DML
from dotenv import load_dotenv
import os
import shutil

# Se limpia todo para hacer el test de nuevo
path_bds = os.path.join(os.environ.get("CARPETA_PARA_BASES_DE_DATOS"))
if os.path.exists(path_bds):
    shutil.rmtree(path_bds)

ddl = DDL()
print()
# Crea la base de datos
respuesta = ddl.crear_base_de_datos("bd1")
print(respuesta.success, respuesta.valor)
# Crea la base de datos
respuesta = ddl.crear_base_de_datos("bd2")
print(respuesta.success, respuesta.valor)
# ERROR | Ya existe la base de datos
respuesta = ddl.crear_base_de_datos("bd1")
print(respuesta.success, respuesta.valor)
# ERROR | Debe indicar la base de datos
respuesta = ddl.crear_base_de_datos(None)
print(respuesta.success, respuesta.valor)

print()
# Elimina la 'bd2'
respuesta = ddl.eliminar_base_de_datos("bd2")
print(respuesta.success, respuesta.valor)
# ERROR | Debe indicar la base de datos
respuesta = ddl.eliminar_base_de_datos(None)
print(respuesta.success, respuesta.valor)
# ERROR | No existe la base de datos
respuesta = ddl.eliminar_base_de_datos("bd2")
print(respuesta.success, respuesta.valor)

print()
# ERROR | No se ha seleccionado la base de datos
respuesta = ddl.crear_tabla(None, "producto", None)
print(respuesta.success, respuesta.valor)
# ERROR | No existe la base de datos
respuesta = ddl.crear_tabla("error", "producto", None)
print(respuesta.success, respuesta.valor)
# Crea tabla
respuesta = ddl.crear_tabla("bd1", "producto", [
    {'name':'id', 'type':'int', 'pk':''},
    {'name':'esta_bueno', 'type':'bit', 'nullable':''},
    {'name':'total', 'type':'decimal', 'nullable':''},
    {'name':'fecha', 'type':'date', 'nullable':''},
    {'name':'fecha_hora', 'type':'datetime', 'nullable':''},
    {'name':'nombre', 'type':'nchar', 'length': 20, 'nullable':''},
    {'name':'descripcion', 'type':'nvarchar', 'length': 100, 'nullable':''},
    {'name':'id_tipo_producto', 'type':'int', 'nullable':'', 'fk_table':'tipo_producto', 'fk_attribute':'id'},
])
print(respuesta.success, respuesta.valor)
# ERROR | Ya existe la tabla
respuesta = ddl.crear_tabla("bd1", "producto", None)
print(respuesta.success, respuesta.valor)

print()
# ERROR | No existe la tabla para hacer referencia
respuesta = ddl.verificar_referencia_llave_foranea("bd1", {'type':'int'}, "tipo_producto", "id")
print(respuesta.success, respuesta.valor)
# Crea tabla
respuesta = ddl.crear_tabla("bd1", "tipo_producto", [
    {'name':'id', 'type':'int', 'nullable':'', 'pk':''},
    {'name':'nombre', 'type':'nchar', 'length': 20, 'nullable':''},
    {'name':'descripcion', 'type':'nvarchar', 'length': 100, 'nullable':''}
])
print(respuesta.success, respuesta.valor)
# ERROR | No existe el campo al que esta haciendo referencia
respuesta = ddl.verificar_referencia_llave_foranea("bd1", {'type':'int'}, "tipo_producto", "test")
print(respuesta.success, respuesta.valor)
# Referencia correcta
respuesta = ddl.verificar_referencia_llave_foranea("bd1", {'type':'int'}, "tipo_producto", "id")
print(respuesta.success, respuesta.valor)

print()
# ERROR | Error por referencia
respuesta = ddl.eliminar_tabla("bd1", "tipo_producto")
print(respuesta.success, respuesta.valor)
# Correcto
respuesta = ddl.eliminar_tabla("bd1", "producto")
print(respuesta.success, respuesta.valor)
# Correcto
respuesta = ddl.eliminar_tabla("bd1", "tipo_producto")
print(respuesta.success, respuesta.valor)

ddl.crear_tabla("bd1", "producto", [
    {'name':'id', 'type':'int', 'pk':''},
    {'name':'esta_bueno', 'type':'bit', 'nullable':''},
    {'name':'total', 'type':'decimal', 'nullable':''},
    {'name':'fecha', 'type':'date', 'nullable':''},
    {'name':'fecha_hora', 'type':'datetime', 'nullable':''},
    {'name':'nombre', 'type':'nchar', 'length': 20, 'nullable':''},
    {'name':'descripcion', 'type':'nvarchar', 'length': 100, 'nullable':''},
    {'name':'id_tipo_producto', 'type':'int', 'nullable':'', 'fk_table':'tipo_producto', 'fk_attribute':'id'},
])
ddl.crear_tabla("bd1", "tipo_producto", [
    {'name':'id', 'type':'int', 'nullable':'', 'pk':''},
    {'name':'nombre', 'type':'nchar', 'length': 20, 'nullable':''},
    {'name':'descripcion', 'type':'nvarchar', 'length': 100, 'nullable':''}
])

dml = DML()
print()
# ERROR | 'id' no es nuleable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {})
print(respuesta.success, respuesta.valor)
# ERROR INT | 'id' debe ser numerico
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 'a'})
print(respuesta.success, respuesta.valor)
# ERROR INT | 'id' debe de estar en un rango aceptable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': -2147483649})
print(respuesta.success, respuesta.valor)
# ERROR INT | 'id' debe de estar en un rango aceptable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 2147483648})
print(respuesta.success, respuesta.valor)
# ERROR BIT | 'esta_bueno' debe de estar en un rango aceptable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 2})
print(respuesta.success, respuesta.valor)
# ERROR DECIMAL | 'total' debe ser numerico
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 'a'})
print(respuesta.success, respuesta.valor)
# ERROR DECIMAL | 'total' debe de estar en un rango aceptable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': -2147483649})
print(respuesta.success, respuesta.valor)
# ERROR DECIMAL | 'total' debe de estar en un rango aceptable
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 2147483648})
print(respuesta.success, respuesta.valor)
# ERROR DATE | 'fecha' debe de ser un formato valido
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':''})
print(respuesta.success, respuesta.valor)
# ERROR DATE | 'fecha' es invalida
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'00-00-2000'})
print(respuesta.success, respuesta.valor)
# ERROR DATE | 'fecha' rango de fecha invalida
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'31-12-1752'})
print(respuesta.success, respuesta.valor)
# ERROR DATETIME | 'fecha_hora' debe de ser un formato valido
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024'})
print(respuesta.success, respuesta.valor)
# ERROR DATETIME | 'fecha_hora' es invalida
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'00-00-2024 00:00:00'})
print(respuesta.success, respuesta.valor)
# ERROR DATETIME | 'fecha_hora' rango de fecha invalida
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'31-12-1752 00:00:00'})
print(respuesta.success, respuesta.valor)
# ERROR NCHAR | 'nombre' debe contener por lo menos un caracter
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':''})
print(respuesta.success, respuesta.valor)
# ERROR NCHAR | 'nombre' no debe sobrepasarse la cantidad de caracteres definidos
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrstuvwxyz'})
print(respuesta.success, respuesta.valor)
# ERROR NVARCHAR | 'descripcion' debe contener por lo menos un caracter
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrs', 'descripcion':''})
print(respuesta.success, respuesta.valor)
# ERROR NVARCHAR | 'descripcion' no debe sobrepasarse la cantidad de caracteres definidos
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrs', 'descripcion':'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'})
print(respuesta.success, respuesta.valor)
# ERROR | No existe la llave foranea en la tabla de referencia
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha': '02-01-2024', 'fecha_hora': '02-01-2024 03:00:00', 'nombre': 'nombre0', 'descripcion': 'descripcion0', 'id_tipo_producto': '1'})
print(respuesta.success, respuesta.valor)
# Registro realizado correctamente
respuesta = dml.insertar_registro_tabla("bd1", "tipo_producto", {'id': 1, 'nombre': 'Tipo producto 1', 'descripcion': 'Descripcion tipo producto'})
print(respuesta.success, respuesta.valor)
# Registro realizado correctamente
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha': '02-01-2024', 'fecha_hora': '02-01-2024 03:00:00', 'nombre': 'nombre0', 'descripcion': 'descripcion0', 'id_tipo_producto': '1'})
print(respuesta.success, respuesta.valor)
# ERROR | La llave primaria no se puede repetir
respuesta = dml.insertar_registro_tabla("bd1", "producto", {'id': 100, 'esta_bueno': 1, 'total': 125.5, 'fecha': '02-01-2024', 'fecha_hora': '02-01-2024 03:00:00', 'nombre': 'nombre0', 'descripcion': 'descripcion0'})
print(respuesta.success, respuesta.valor)
dml.insertar_registro_tabla("bd1", "producto", {'id': 101, 'esta_bueno': 0, 'total': 75.2, 'fecha': '03-01-2024', 'fecha_hora': '02-01-2024 06:00:00', 'nombre': 'nombre1', 'descripcion': 'descripcion1'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 102, 'esta_bueno': 1, 'total': 42.0, 'fecha': '04-01-2024', 'fecha_hora': '02-01-2024 09:00:00', 'nombre': 'nombre2', 'descripcion': 'descripcion2'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 103, 'esta_bueno': 0, 'total': 150.3, 'fecha': '05-01-2024', 'fecha_hora': '02-01-2024 12:00:00', 'nombre': 'nombre3', 'descripcion': 'descripcion3'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 104, 'esta_bueno': 1, 'total': 80.1, 'fecha': '06-01-2024', 'fecha_hora': '02-01-2024 15:00:00', 'nombre': 'nombre4', 'descripcion': 'descripcion4'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 105, 'esta_bueno': 0, 'total': 170.5, 'fecha': '07-01-2024', 'fecha_hora': '02-01-2024 18:00:00', 'nombre': 'nombre5', 'descripcion': 'descripcion5'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 106, 'esta_bueno': 1, 'total': 95.2, 'fecha': '08-01-2024', 'fecha_hora': '02-01-2024 21:00:00', 'nombre': 'nombre6', 'descripcion': 'descripcion6'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 107, 'esta_bueno': 0, 'total': 120.8, 'fecha': '09-01-2024', 'fecha_hora': '03-01-2024 00:00:00', 'nombre': 'nombre7', 'descripcion': 'descripcion7'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 108, 'esta_bueno': 1, 'total': 60.3, 'fecha': '10-01-2024', 'fecha_hora': '03-01-2024 03:00:00', 'nombre': 'nombre8', 'descripcion': 'descripcion8'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 109, 'esta_bueno': 0, 'total': 110.0, 'fecha': '11-01-2024', 'fecha_hora': '03-01-2024 06:00:00', 'nombre': 'nombre9', 'descripcion': 'descripcion9'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 110, 'esta_bueno': 1, 'total': 85.7, 'fecha': '12-01-2024', 'fecha_hora': '03-01-2024 09:00:00', 'nombre': 'nombre10', 'descripcion': 'descripcion10'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 111, 'esta_bueno': 0, 'total': 130.4, 'fecha': '13-01-2024', 'fecha_hora': '03-01-2024 12:00:00', 'nombre': 'nombre11', 'descripcion': 'descripcion11'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 112, 'esta_bueno': 1, 'total': 75.0, 'fecha': '14-01-2024', 'fecha_hora': '03-01-2024 15:00:00', 'nombre': 'nombre12', 'descripcion': 'descripcion12'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 113, 'esta_bueno': 0, 'total': 100.2, 'fecha': '15-01-2024', 'fecha_hora': '03-01-2024 18:00:00', 'nombre': 'nombre13', 'descripcion': 'descripcion13'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 114, 'esta_bueno': 1, 'total': 55.9, 'fecha': '16-01-2024', 'fecha_hora': '03-01-2024 21:00:00', 'nombre': 'nombre14', 'descripcion': 'descripcion14'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 115, 'esta_bueno': 0, 'total': 105.6, 'fecha': '17-01-2024', 'fecha_hora': '04-01-2024 00:00:00', 'nombre': 'nombre15', 'descripcion': 'descripcion15'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 116, 'esta_bueno': 1, 'total': 80.3, 'fecha': '18-01-2024', 'fecha_hora': '04-01-2024 03:00:00', 'nombre': 'nombre16', 'descripcion': 'descripcion16'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 117, 'esta_bueno': 0, 'total': 120.0, 'fecha': '19-01-2024', 'fecha_hora': '04-01-2024 06:00:00', 'nombre': 'nombre17', 'descripcion': 'descripcion17'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 118, 'esta_bueno': 1, 'total': 95.7, 'fecha': '20-01-2024', 'fecha_hora': '04-01-2024 09:00:00', 'nombre': 'nombre18', 'descripcion': 'descripcion18'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 119, 'esta_bueno': 0, 'total': 140.4, 'fecha': '21-01-2024', 'fecha_hora': '04-01-2024 12:00:00', 'nombre': 'nombre19', 'descripcion': 'descripcion19'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 120, 'esta_bueno': 1, 'total': 65.2, 'fecha': '22-01-2024', 'fecha_hora': '04-01-2024 15:00:00', 'nombre': 'nombre20', 'descripcion': 'descripcion20'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 121, 'esta_bueno': 0, 'total': 110.9, 'fecha': '23-01-2024', 'fecha_hora': '04-01-2024 18:00:00', 'nombre': 'nombre21', 'descripcion': 'descripcion21'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 122, 'esta_bueno': 1, 'total': 75.6, 'fecha': '24-01-2024', 'fecha_hora': '04-01-2024 21:00:00', 'nombre': 'nombre22', 'descripcion': 'descripcion22'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 123, 'esta_bueno': 0, 'total': 105.3, 'fecha': '25-01-2024', 'fecha_hora': '05-01-2024 00:00:00', 'nombre': 'nombre23', 'descripcion': 'descripcion23'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 124, 'esta_bueno': 1, 'total': 85.1, 'fecha': '26-01-2024', 'fecha_hora': '05-01-2024 03:00:00', 'nombre': 'nombre24', 'descripcion': 'descripcion24'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 125, 'esta_bueno': 0, 'total': 125.8, 'fecha': '27-01-2024', 'fecha_hora': '05-01-2024 06:00:00', 'nombre': 'nombre25', 'descripcion': 'descripcion25'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 126, 'esta_bueno': 1, 'total': 100.5, 'fecha': '28-01-2024', 'fecha_hora': '05-01-2024 09:00:00', 'nombre': 'nombre26', 'descripcion': 'descripcion26'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 127, 'esta_bueno': 0, 'total': 145.2, 'fecha': '29-01-2024', 'fecha_hora': '05-01-2024 12:00:00', 'nombre': 'nombre27', 'descripcion': 'descripcion27'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 128, 'esta_bueno': 1, 'total': 70.0, 'fecha': '30-01-2024', 'fecha_hora': '05-01-2024 15:00:00', 'nombre': 'nombre28', 'descripcion': 'descripcion28'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 129, 'esta_bueno': 0, 'total': 115.7, 'fecha': '31-01-2024', 'fecha_hora': '05-01-2024 18:00:00', 'nombre': 'nombre29', 'descripcion': 'descripcion29'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 130, 'esta_bueno': 1, 'total': 90.4, 'fecha': '01-02-2024', 'fecha_hora': '05-01-2024 21:00:00', 'nombre': 'nombre30', 'descripcion': 'descripcion30'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 131, 'esta_bueno': 0, 'total': 135.1, 'fecha': '02-02-2024', 'fecha_hora': '06-01-2024 00:00:00', 'nombre': 'nombre31', 'descripcion': 'descripcion31'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 132, 'esta_bueno': 1, 'total': 60.8, 'fecha': '03-02-2024', 'fecha_hora': '06-01-2024 03:00:00', 'nombre': 'nombre32', 'descripcion': 'descripcion32'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 133, 'esta_bueno': 0, 'total': 110.5, 'fecha': '04-02-2024', 'fecha_hora': '06-01-2024 06:00:00', 'nombre': 'nombre33', 'descripcion': 'descripcion33'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 134, 'esta_bueno': 1, 'total': 85.2, 'fecha': '05-02-2024', 'fecha_hora': '06-01-2024 09:00:00', 'nombre': 'nombre34', 'descripcion': 'descripcion34'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 135, 'esta_bueno': 0, 'total': 130.9, 'fecha': '06-02-2024', 'fecha_hora': '06-01-2024 12:00:00', 'nombre': 'nombre35', 'descripcion': 'descripcion35'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 136, 'esta_bueno': 1, 'total': 75.6, 'fecha': '07-02-2024', 'fecha_hora': '06-01-2024 15:00:00', 'nombre': 'nombre36', 'descripcion': 'descripcion36'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 137, 'esta_bueno': 0, 'total': 105.3, 'fecha': '08-02-2024', 'fecha_hora': '06-01-2024 18:00:00', 'nombre': 'nombre37', 'descripcion': 'descripcion37'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 138, 'esta_bueno': 1, 'total': 80.0, 'fecha': '09-02-2024', 'fecha_hora': '06-01-2024 21:00:00', 'nombre': 'nombre38', 'descripcion': 'descripcion38'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 139, 'esta_bueno': 0, 'total': 120.7, 'fecha': '10-02-2024', 'fecha_hora': '07-01-2024 00:00:00', 'nombre': 'nombre39', 'descripcion': 'descripcion39'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 140, 'esta_bueno': 1, 'total': 95.4, 'fecha': '11-02-2024', 'fecha_hora': '07-01-2024 03:00:00', 'nombre': 'nombre40', 'descripcion': 'descripcion40'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 141, 'esta_bueno': 0, 'total': 135.1, 'fecha': '12-02-2024', 'fecha_hora': '07-01-2024 06:00:00', 'nombre': 'nombre41', 'descripcion': 'descripcion41'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 142, 'esta_bueno': 1, 'total': 110.8, 'fecha': '13-02-2024', 'fecha_hora': '07-01-2024 09:00:00', 'nombre': 'nombre42', 'descripcion': 'descripcion42'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 143, 'esta_bueno': 0, 'total': 155.5, 'fecha': '14-02-2024', 'fecha_hora': '07-01-2024 12:00:00', 'nombre': 'nombre43', 'descripcion': 'descripcion43'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 144, 'esta_bueno': 1, 'total': 80.2, 'fecha': '15-02-2024', 'fecha_hora': '07-01-2024 15:00:00', 'nombre': 'nombre44', 'descripcion': 'descripcion44'})
dml.insertar_registro_tabla("bd1", "producto", {'id': 145, 'esta_bueno': 0, 'total': 125.9, 'fecha': '16-02-2024', 'fecha_hora': '07-01-2024 18:00:00', 'nombre': 'nombre45', 'descripcion': 'descripcion45'})
