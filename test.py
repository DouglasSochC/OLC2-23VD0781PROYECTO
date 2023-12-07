from Funcionalidad.ddl import crear_base_de_datos, crear_tabla, eliminar_base_de_datos
from Funcionalidad.dml import insertar_registro_tabla

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
    {'name':'nombre', 'type':'nchar', 'length': '5', 'nullable':'false'},
    {'name':'descripcion', 'type':'nvarchar', 'length': '10', 'nullable':'false'},
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
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abc123'})
print(respuesta)
# ERROR NVARCHAR | 'descripcion' debe contener por lo menos un caracter
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcde', 'descripcion':''})
print(respuesta)
# ERROR NVARCHAR | 'descripcion' no debe sobrepasarse la cantidad de caracteres definidos
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcde', 'descripcion':'123456789ab'})
print(respuesta)
# Registro realizado correctamente
respuesta = insertar_registro_tabla("bd1", "tbl1", {'id':'100', 'es_admin':'1', 'total':'125.5', 'fecha':'01-01-2024', 'fecha_hora':'01-01-2024 00:00:00', 'nombre':'abcde', 'descripcion':'douglas'})
print(respuesta)