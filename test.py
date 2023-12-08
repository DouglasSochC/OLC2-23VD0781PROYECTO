from Funcionalidad.ddl import crear_base_de_datos, crear_tabla, eliminar_base_de_datos
from Funcionalidad.dml import insertar_registro_tabla, seleccionar_registro_tabla

print()
# Crea la base de datos
respuesta = crear_base_de_datos("bd1")
print(respuesta)
# Crea la base de datos
respuesta = crear_base_de_datos("bd2")
print(respuesta)
# ERROR | Ya existe la base de datos
respuesta = crear_base_de_datos("bd1")
print(respuesta)
# ERROR | Debe indicar la base de datos
respuesta = crear_base_de_datos(None)
print(respuesta)

print()
# Elimina la 'bd2'
respuesta = eliminar_base_de_datos("bd2")
print(respuesta)
# ERROR | Debe indicar la base de datos
respuesta = eliminar_base_de_datos(None)
print(respuesta)
# ERROR | No existe la base de datos
respuesta = eliminar_base_de_datos("bd2")
print(respuesta)

print()
# ERROR | No se ha seleccionado la base de datos
respuesta = crear_tabla(None, "tbl1", None)
print(respuesta)
# ERROR | No existe la base de datos
respuesta = crear_tabla("error", "tbl1", None)
print(respuesta)
# Crea la tabla
respuesta = crear_tabla("bd1", "tbl1", [
    {'name':'id', 'type':'int', 'nullable':'false'},
    {'name':'es_admin', 'type':'bit', 'nullable':'false'},
    {'name':'total', 'type':'decimal', 'nullable':'false'},
    {'name':'fecha', 'type':'date', 'nullable':'false'},
    {'name':'fecha_hora', 'type':'datetime', 'nullable':'false'},
    {'name':'nombre', 'type':'nchar', 'length': '20', 'nullable':'false'},
    {'name':'descripcion', 'type':'nvarchar', 'length': '100', 'nullable':'false'},
])
print(respuesta)
# ERROR | Ya existe la tabla
respuesta = crear_tabla("bd1", "tbl1", None)
print(respuesta)

print()
# ERROR | 'id' no es nuleable
respuesta = insertar_registro_tabla("bd1", "tbl1", {})
print(respuesta)
# ERROR INT | 'id' debe ser numerico
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'a'})
print(respuesta)
# ERROR INT | 'id' debe de estar en un rango aceptable
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'-2147483649'})
print(respuesta)
# ERROR INT | 'id' debe de estar en un rango aceptable
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'2147483648'})
print(respuesta)
# ERROR BIT | 'es_admin' debe de estar en un rango aceptable
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'2'})
print(respuesta)
# ERROR DECIMAL | 'total' debe ser numerico
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'a'})
print(respuesta)
# ERROR DECIMAL | 'total' debe de estar en un rango aceptable
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'-2147483649'})
print(respuesta)
# ERROR DECIMAL | 'total' debe de estar en un rango aceptable
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'2147483648'})
print(respuesta)
# ERROR DATE | 'fecha' debe de ser un formato valido
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':''})
print(respuesta)
# ERROR DATE | 'fecha' es invalida
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'00-00-2000'})
print(respuesta)
# ERROR DATE | 'fecha' rango de fecha invalida
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'31-12-1752'})
print(respuesta)
# ERROR DATETIME | 'fecha_hora' debe de ser un formato valido
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024'})
print(respuesta)
# ERROR DATETIME | 'fecha_hora' es invalida
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'00-00-2024 00:00:00'})
print(respuesta)
# ERROR DATETIME | 'fecha_hora' rango de fecha invalida
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'31-12-1752 00:00:00'})
print(respuesta)
# ERROR NCHAR | 'nombre' debe contener por lo menos un caracter
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':''})
print(respuesta)
# ERROR NCHAR | 'nombre' no debe sobrepasarse la cantidad de caracteres definidos
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrstuvwxyz'})
print(respuesta)
# ERROR NVARCHAR | 'descripcion' debe contener por lo menos un caracter
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrs', 'descripcion':''})
print(respuesta)
# ERROR NVARCHAR | 'descripcion' no debe sobrepasarse la cantidad de caracteres definidos
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcdefghijklmnopqrs', 'descripcion':'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'})
print(respuesta)
# Registro realizado correctamente
insertar_registro_tabla("bd1", "tbl1", {'id': '100', 'es_admin': '1', 'total': '125.5', 'fecha': '02-01-2024', 'fecha_hora': '02-01-2024 03:00:00', 'nombre': 'nombre0', 'descripcion': 'descripcion0'})
insertar_registro_tabla("bd1", "tbl1", {'id': '101', 'es_admin': '0', 'total': '75.2', 'fecha': '03-01-2024', 'fecha_hora': '02-01-2024 06:00:00', 'nombre': 'nombre1', 'descripcion': 'descripcion1'})
insertar_registro_tabla("bd1", "tbl1", {'id': '102', 'es_admin': '1', 'total': '42.0', 'fecha': '04-01-2024', 'fecha_hora': '02-01-2024 09:00:00', 'nombre': 'nombre2', 'descripcion': 'descripcion2'})
insertar_registro_tabla("bd1", "tbl1", {'id': '103', 'es_admin': '0', 'total': '150.3', 'fecha': '05-01-2024', 'fecha_hora': '02-01-2024 12:00:00', 'nombre': 'nombre3', 'descripcion': 'descripcion3'})
insertar_registro_tabla("bd1", "tbl1", {'id': '104', 'es_admin': '1', 'total': '80.1', 'fecha': '06-01-2024', 'fecha_hora': '02-01-2024 15:00:00', 'nombre': 'nombre4', 'descripcion': 'descripcion4'})
insertar_registro_tabla("bd1", "tbl1", {'id': '105', 'es_admin': '0', 'total': '170.5', 'fecha': '07-01-2024', 'fecha_hora': '02-01-2024 18:00:00', 'nombre': 'nombre5', 'descripcion': 'descripcion5'})
insertar_registro_tabla("bd1", "tbl1", {'id': '106', 'es_admin': '1', 'total': '95.2', 'fecha': '08-01-2024', 'fecha_hora': '02-01-2024 21:00:00', 'nombre': 'nombre6', 'descripcion': 'descripcion6'})
insertar_registro_tabla("bd1", "tbl1", {'id': '107', 'es_admin': '0', 'total': '120.8', 'fecha': '09-01-2024', 'fecha_hora': '03-01-2024 00:00:00', 'nombre': 'nombre7', 'descripcion': 'descripcion7'})
insertar_registro_tabla("bd1", "tbl1", {'id': '108', 'es_admin': '1', 'total': '60.3', 'fecha': '10-01-2024', 'fecha_hora': '03-01-2024 03:00:00', 'nombre': 'nombre8', 'descripcion': 'descripcion8'})
insertar_registro_tabla("bd1", "tbl1", {'id': '109', 'es_admin': '0', 'total': '110.0', 'fecha': '11-01-2024', 'fecha_hora': '03-01-2024 06:00:00', 'nombre': 'nombre9', 'descripcion': 'descripcion9'})
insertar_registro_tabla("bd1", "tbl1", {'id': '110', 'es_admin': '1', 'total': '85.7', 'fecha': '12-01-2024', 'fecha_hora': '03-01-2024 09:00:00', 'nombre': 'nombre10', 'descripcion': 'descripcion10'})
insertar_registro_tabla("bd1", "tbl1", {'id': '111', 'es_admin': '0', 'total': '130.4', 'fecha': '13-01-2024', 'fecha_hora': '03-01-2024 12:00:00', 'nombre': 'nombre11', 'descripcion': 'descripcion11'})
insertar_registro_tabla("bd1", "tbl1", {'id': '112', 'es_admin': '1', 'total': '75.0', 'fecha': '14-01-2024', 'fecha_hora': '03-01-2024 15:00:00', 'nombre': 'nombre12', 'descripcion': 'descripcion12'})
insertar_registro_tabla("bd1", "tbl1", {'id': '113', 'es_admin': '0', 'total': '100.2', 'fecha': '15-01-2024', 'fecha_hora': '03-01-2024 18:00:00', 'nombre': 'nombre13', 'descripcion': 'descripcion13'})
insertar_registro_tabla("bd1", "tbl1", {'id': '114', 'es_admin': '1', 'total': '55.9', 'fecha': '16-01-2024', 'fecha_hora': '03-01-2024 21:00:00', 'nombre': 'nombre14', 'descripcion': 'descripcion14'})
insertar_registro_tabla("bd1", "tbl1", {'id': '115', 'es_admin': '0', 'total': '105.6', 'fecha': '17-01-2024', 'fecha_hora': '04-01-2024 00:00:00', 'nombre': 'nombre15', 'descripcion': 'descripcion15'})
insertar_registro_tabla("bd1", "tbl1", {'id': '116', 'es_admin': '1', 'total': '80.3', 'fecha': '18-01-2024', 'fecha_hora': '04-01-2024 03:00:00', 'nombre': 'nombre16', 'descripcion': 'descripcion16'})
insertar_registro_tabla("bd1", "tbl1", {'id': '117', 'es_admin': '0', 'total': '120.0', 'fecha': '19-01-2024', 'fecha_hora': '04-01-2024 06:00:00', 'nombre': 'nombre17', 'descripcion': 'descripcion17'})
insertar_registro_tabla("bd1", "tbl1", {'id': '118', 'es_admin': '1', 'total': '95.7', 'fecha': '20-01-2024', 'fecha_hora': '04-01-2024 09:00:00', 'nombre': 'nombre18', 'descripcion': 'descripcion18'})
insertar_registro_tabla("bd1", "tbl1", {'id': '119', 'es_admin': '0', 'total': '140.4', 'fecha': '21-01-2024', 'fecha_hora': '04-01-2024 12:00:00', 'nombre': 'nombre19', 'descripcion': 'descripcion19'})
insertar_registro_tabla("bd1", "tbl1", {'id': '120', 'es_admin': '1', 'total': '65.2', 'fecha': '22-01-2024', 'fecha_hora': '04-01-2024 15:00:00', 'nombre': 'nombre20', 'descripcion': 'descripcion20'})
insertar_registro_tabla("bd1", "tbl1", {'id': '121', 'es_admin': '0', 'total': '110.9', 'fecha': '23-01-2024', 'fecha_hora': '04-01-2024 18:00:00', 'nombre': 'nombre21', 'descripcion': 'descripcion21'})
insertar_registro_tabla("bd1", "tbl1", {'id': '122', 'es_admin': '1', 'total': '75.6', 'fecha': '24-01-2024', 'fecha_hora': '04-01-2024 21:00:00', 'nombre': 'nombre22', 'descripcion': 'descripcion22'})
insertar_registro_tabla("bd1", "tbl1", {'id': '123', 'es_admin': '0', 'total': '105.3', 'fecha': '25-01-2024', 'fecha_hora': '05-01-2024 00:00:00', 'nombre': 'nombre23', 'descripcion': 'descripcion23'})
insertar_registro_tabla("bd1", "tbl1", {'id': '124', 'es_admin': '1', 'total': '85.1', 'fecha': '26-01-2024', 'fecha_hora': '05-01-2024 03:00:00', 'nombre': 'nombre24', 'descripcion': 'descripcion24'})
insertar_registro_tabla("bd1", "tbl1", {'id': '125', 'es_admin': '0', 'total': '125.8', 'fecha': '27-01-2024', 'fecha_hora': '05-01-2024 06:00:00', 'nombre': 'nombre25', 'descripcion': 'descripcion25'})
insertar_registro_tabla("bd1", "tbl1", {'id': '126', 'es_admin': '1', 'total': '100.5', 'fecha': '28-01-2024', 'fecha_hora': '05-01-2024 09:00:00', 'nombre': 'nombre26', 'descripcion': 'descripcion26'})
insertar_registro_tabla("bd1", "tbl1", {'id': '127', 'es_admin': '0', 'total': '145.2', 'fecha': '29-01-2024', 'fecha_hora': '05-01-2024 12:00:00', 'nombre': 'nombre27', 'descripcion': 'descripcion27'})
insertar_registro_tabla("bd1", "tbl1", {'id': '128', 'es_admin': '1', 'total': '70.0', 'fecha': '30-01-2024', 'fecha_hora': '05-01-2024 15:00:00', 'nombre': 'nombre28', 'descripcion': 'descripcion28'})
insertar_registro_tabla("bd1", "tbl1", {'id': '129', 'es_admin': '0', 'total': '115.7', 'fecha': '31-01-2024', 'fecha_hora': '05-01-2024 18:00:00', 'nombre': 'nombre29', 'descripcion': 'descripcion29'})
insertar_registro_tabla("bd1", "tbl1", {'id': '130', 'es_admin': '1', 'total': '90.4', 'fecha': '01-02-2024', 'fecha_hora': '05-01-2024 21:00:00', 'nombre': 'nombre30', 'descripcion': 'descripcion30'})
insertar_registro_tabla("bd1", "tbl1", {'id': '131', 'es_admin': '0', 'total': '135.1', 'fecha': '02-02-2024', 'fecha_hora': '06-01-2024 00:00:00', 'nombre': 'nombre31', 'descripcion': 'descripcion31'})
insertar_registro_tabla("bd1", "tbl1", {'id': '132', 'es_admin': '1', 'total': '60.8', 'fecha': '03-02-2024', 'fecha_hora': '06-01-2024 03:00:00', 'nombre': 'nombre32', 'descripcion': 'descripcion32'})
insertar_registro_tabla("bd1", "tbl1", {'id': '133', 'es_admin': '0', 'total': '110.5', 'fecha': '04-02-2024', 'fecha_hora': '06-01-2024 06:00:00', 'nombre': 'nombre33', 'descripcion': 'descripcion33'})
insertar_registro_tabla("bd1", "tbl1", {'id': '134', 'es_admin': '1', 'total': '85.2', 'fecha': '05-02-2024', 'fecha_hora': '06-01-2024 09:00:00', 'nombre': 'nombre34', 'descripcion': 'descripcion34'})
insertar_registro_tabla("bd1", "tbl1", {'id': '135', 'es_admin': '0', 'total': '130.9', 'fecha': '06-02-2024', 'fecha_hora': '06-01-2024 12:00:00', 'nombre': 'nombre35', 'descripcion': 'descripcion35'})
insertar_registro_tabla("bd1", "tbl1", {'id': '136', 'es_admin': '1', 'total': '75.6', 'fecha': '07-02-2024', 'fecha_hora': '06-01-2024 15:00:00', 'nombre': 'nombre36', 'descripcion': 'descripcion36'})
insertar_registro_tabla("bd1", "tbl1", {'id': '137', 'es_admin': '0', 'total': '105.3', 'fecha': '08-02-2024', 'fecha_hora': '06-01-2024 18:00:00', 'nombre': 'nombre37', 'descripcion': 'descripcion37'})
insertar_registro_tabla("bd1", "tbl1", {'id': '138', 'es_admin': '1', 'total': '80.0', 'fecha': '09-02-2024', 'fecha_hora': '06-01-2024 21:00:00', 'nombre': 'nombre38', 'descripcion': 'descripcion38'})
insertar_registro_tabla("bd1", "tbl1", {'id': '139', 'es_admin': '0', 'total': '120.7', 'fecha': '10-02-2024', 'fecha_hora': '07-01-2024 00:00:00', 'nombre': 'nombre39', 'descripcion': 'descripcion39'})
insertar_registro_tabla("bd1", "tbl1", {'id': '140', 'es_admin': '1', 'total': '95.4', 'fecha': '11-02-2024', 'fecha_hora': '07-01-2024 03:00:00', 'nombre': 'nombre40', 'descripcion': 'descripcion40'})
insertar_registro_tabla("bd1", "tbl1", {'id': '141', 'es_admin': '0', 'total': '135.1', 'fecha': '12-02-2024', 'fecha_hora': '07-01-2024 06:00:00', 'nombre': 'nombre41', 'descripcion': 'descripcion41'})
insertar_registro_tabla("bd1", "tbl1", {'id': '142', 'es_admin': '1', 'total': '110.8', 'fecha': '13-02-2024', 'fecha_hora': '07-01-2024 09:00:00', 'nombre': 'nombre42', 'descripcion': 'descripcion42'})
insertar_registro_tabla("bd1", "tbl1", {'id': '143', 'es_admin': '0', 'total': '155.5', 'fecha': '14-02-2024', 'fecha_hora': '07-01-2024 12:00:00', 'nombre': 'nombre43', 'descripcion': 'descripcion43'})
insertar_registro_tabla("bd1", "tbl1", {'id': '144', 'es_admin': '1', 'total': '80.2', 'fecha': '15-02-2024', 'fecha_hora': '07-01-2024 15:00:00', 'nombre': 'nombre44', 'descripcion': 'descripcion44'})
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id': '145', 'es_admin': '0', 'total': '125.9', 'fecha': '16-02-2024', 'fecha_hora': '07-01-2024 18:00:00', 'nombre': 'nombre45', 'descripcion': 'descripcion45'})
print(respuesta)