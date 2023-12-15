from ply.yacc import yacc
from .lexer import tokens, lexer, errores
from .expresiones.literal import *
from .abstract.retorno import *

# Clases
from .abstract.retorno import TIPO_DATO
from .expresiones.accion import Accion
from .expresiones.tipo_dato import Tipo_Dato
from .expresiones.identificador import Identificador
from .expresiones.aritmetica import Aritmetica
from .expresiones.relacional import Relacional
from .expresiones.logico import Logico
from .expresiones.campo_table import Campo_Table
from .expresiones.constrain import Constrain
from .instrucciones.use import Use
from .instrucciones.select import Select
from .instrucciones.declare import Declare
from .instrucciones.alter import Alter
from .instrucciones.truncate import Truncate
from .instrucciones.drop import Drop


contador = 0

# Operadores de precedencia
precedence = (
    ('left', 'OR_OP'),
    ('left', 'AND_OP'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('right', 'NOT'),
    ('left', 'IZQPAREN', 'DERPAREN'),
)

# Gramatica
def p_inicio(p):
    '''
    inicio : instrucciones
    '''
    p[0] = p[1]

def p_instrucciones_lista(p):
    '''
    instrucciones : instrucciones instruccion
    '''
    p[1].append(p[2])
    p[0] = p[1]

def p_instrucciones_lista2(p):
    '''
    instrucciones : instruccion
    '''
    p[0] = [p[1]]

def p_instruccion(p):
    '''
    instruccion : expresion
    '''
    p[0] = p[1]

def p_usar_db(p):
    '''
    usar_db : USE identificador PUNTOYCOMA
    '''
    global contador
    id_nodo_use = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Use(id_nodo_use, p[2])

def p_declaracion_variable(p):
    '''
    declaracion_variable : DECLARE identificador tipo_dato PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Declare(id_nodo, p[2], p[3])

def p_tipo_dato(p):
    '''
    tipo_dato : seg_num
        | seg_date
        | seg_string
    '''
    p[0] = p[1]

def p_seg_num(p):
    '''
    seg_num : INT
            | DECIMAL IZQPAREN LNUMERO COMA LNUMERO DERPAREN
            | BIT
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if p[1] == 'INT':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.INT, -1)
    elif p[1] == 'DECIMAL':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.DECIMAL, -1)
    elif p[1] == 'BIT':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.BIT, -1)
    else:
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NULL, -1)

def p_seg_date(p):
    '''
    seg_date : DATE
            | DATETIME
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if p[1] == 'DATE':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.DATE, -1)
    elif p[1] == 'DATETIME':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.DATETIME, -1)
    else:
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NULL, -1)

def p_seg_string(p):
    '''
    seg_string : NVARCHAR IZQPAREN LNUMERO DERPAREN
                | NCHAR IZQPAREN LNUMERO DERPAREN
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if p[1] == 'NVARCHAR':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NVARCHAR, p[3])
    elif p[1] == 'NCHAR':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NCHAR, p[3])
    else:
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NULL, -1)

def p_sentencia_ddl(p):
    '''
        sentencia_ddl : create
                      | alter
                      | truncate
                      | drop
    '''
    p[0] = p[1]

def p_create(p):
    '''
        create : CREATE DATABASE identificador PUNTOYCOMA
               | CREATE TABLE identificador IZQPAREN campos_table DERPAREN PUNTOYCOMA
               | CREATE PROCEDURE identificador IZQPAREN parametros DERPAREN AS BEGIN lista_sentencias_dml END PUNTOYCOMA
               | CREATE FUNCTION identificador IZQPAREN parametros DERPAREN RETURN tipo_dato AS BEGIN lista_sentencias_dml END PUNTOYCOMA
    '''
    p[0] = p[1]

def p_campos_table(p):
    '''
    campos_table : campos_table COMA identificador tipo_dato constrain
                 | campos_table COMA identificador tipo_dato
                 | identificador tipo_dato constrain
                 | identificador tipo_dato
    '''
    global contador
    elemento_hashable = p[3] if len(p) > 3 else p[1]
    id_nodo = str(abs(hash(elemento_hashable)) + contador)
    contador += 1
    if len(p) == 6:
        p[0] = Campo_Table(id_nodo, p[1], p[3], p[4], p[5])
    elif len(p) == 5:
        p[0] = Campo_Table(id_nodo, p[1], p[3], p[4])
    elif len(p) == 4:
        print("tiene constrain")
        #p[0] = [p[1], p[2], p[3]]
        p[0] = Campo_Table(id_nodo, p[1], p[2], p[3])
    else:
        p[0] = Campo_Table(id_nodo, p[1], p[2])

def p_parametros(p):
    '''
    parametros : parametros COMA identificador tipo_dato
                | identificador tipo_dato
    '''
    p[0] = p[1]

def p_constrain(p):
    '''
    constrain : PRIMARY KEY
              | NOT NULL
              | REFERENCES identificador IZQPAREN identificador DERPAREN
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1

    if len(p) == 3:
        if p[1] == 'PRIMARY':
            print("ENTRO A ESTA PRODUCCION")
            p[0] = Constrain(id_nodo,[p[1],p[2]])
        else:
            p[0] = Constrain(id_nodo,0,[p[1],p[2]]) # NOT NULL
    else:
        print("ENTRO A ESTA PRODUCCION")
        p[0] = Constrain(id_nodo, p[1], p[4], p[2])

def p_alter(p):
    '''
    alter : ALTER TABLE identificador accion PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Alter(id_nodo,p[1], p[2], p[3], p[4])

def p_accion(p):
    '''
    accion : ADD COLUMN campos_table
           | DROP COLUMN identificador
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if p[0] == 'ADD':
        p[0] = Accion(id_nodo,p[1], p[2], p[3])
    else:
        p[0] = Accion(id_nodo,p[1], p[2], p[3])

def p_drop(p):
    '''
    drop : DROP DATABASE identificador PUNTOYCOMA
         | DROP TABLE identificador PUNTOYCOMA
         | DROP PROCEDURE identificador PUNTOYCOMA
         | DROP FUNCTION identificador PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Drop(id_nodo,p[1], p[2], p[3])

def p_truncate(p):
    '''
    truncate : TRUNCATE TABLE identificador PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Truncate(id_nodo,p[1], p[2], p[3])

def p_lista_sentencias_dml(p):
    '''
    lista_sentencias_dml : lista_sentencias_dml sentencia_dml
                         | sentencia_dml
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_llamar_procedure(p):
    '''
    llamar_procedure : EXEC identificador lista_expresiones PUNTOYCOMA
    '''
    p[0] = p[1]

def p_sentencia_dml(p):
    '''
    sentencia_dml : select
                | insert
                | update
                | delete
                | if
                | while
                | RETURN expresion PUNTOYCOMA
                | expresion
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_select(p):
    '''
        select : SELECT POR FROM identificador PUNTOYCOMA
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM identificador PUNTOYCOMA
               | SELECT lista_expresiones FROM identificador PUNTOYCOMA
               | SELECT POR FROM identificador WHERE condicion PUNTOYCOMA
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM identificador WHERE condicion PUNTOYCOMA
               | SELECT lista_expresiones FROM identificador WHERE condicion PUNTOYCOMA
               | SELECT lista_expresiones PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN FROM identificador PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN FROM identificador PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN FROM identificador WHERE condicion PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN FROM identificador WHERE condicion PUNTOYCOMA
    '''
    if len(p) == 4:
        p[0] = p[1]
    elif len(p) == 6 and p[2] == '*':
        p[0] = p[1]
    elif len(p) == 6 and p[3] == 'from':
        p[0] = Select(p[4], p[2], [])
    elif len(p) == 6 and p[3] == '(':
        p[0] = p[1]
    elif len(p) == 7:
        p[0] = p[1]
    elif len(p) == 8 and p[2] == '(':
        p[0] = p[1]
    elif len(p) == 8 and p[2] == '*':
        p[0] = p[1]
    elif len(p) == 8 and p[3] == 'from':
        p[0] = Select(p[4], p[2], p[6])
    elif len(p) == 8 and p[3] == '(':
        p[0] = p[1]
    elif len(p) == 9:
        p[0] = p[1]
    elif len(p) == 10 and p[2] == '(':
        p[0] = p[1]
    elif len(p) == 10 and p[3] == '(':
        p[0] = p[1]
    elif len(p) == 11:
        p[0] = p[1]

def p_insert(p):
    '''
    insert : INSERT INTO identificador IZQPAREN lista_expresiones DERPAREN VALUES IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
    '''
    p[0] = p[1]

def p_update(p):
    '''
    update : UPDATE identificador SET lista_expresiones WHERE condicion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_delete(p):
    '''
    delete : DELETE FROM identificador WHERE condicion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_if(p):
    '''
    if : IF expresion THEN sentencia_dml ELSE sentencia_dml END IF PUNTOYCOMA
       | IF expresion THEN sentencia_dml END IF PUNTOYCOMA
    '''
    p[0] = p[1]

def p_while(p):
    '''
    while : WHILE expresion BEGIN lista_sentencias_dml END
    '''
    p[0] = p[1]

def p_condicion(p):
    '''
    condicion : condicion AND expresion
              | expresion
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_lista_expresiones(p):
    '''
        lista_expresiones : lista_expresiones COMA expresion
                         | expresion
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_expresion(p):
    '''
        expresion : aritmeticos
                | relacionales
                | logicos
                | literal
                | funcion_nativa
                | IZQPAREN expresion DERPAREN
                | asignacion
                | identificador
                | alias
    '''
    p[0] = p[1]

def p_alias(p):
    '''
        alias : expresion AS ID
            | expresion ID
    '''
    p[0] = p[1]

def p_asignacion(p):
    '''
        asignacion : expresion IGUAL expresion
                   | SET expresion
    '''
    if len(p) == 4:
        p[0] = {'accion': p[1], 'tipo_dato': p[2], 'valor': p[3]}
    else:
        p[0] = {'accion': p[1], 'valor': p[2]}

def p_funcion_nativa(p):
    '''
        funcion_nativa : CONCATENA IZQPAREN expresion COMA expresion DERPAREN
                          | SUBSTRAER IZQPAREN expresion COMA expresion COMA expresion DERPAREN
                          | HOY IZQPAREN DERPAREN
                          | CONTAR IZQPAREN expresion DERPAREN
                          | SUMA IZQPAREN expresion DERPAREN
                          | CAST IZQPAREN expresion AS tipo_dato DERPAREN
    '''
    if p[1] == 'CONCATENA':
        p[0] = {'accion': p[1], 'valor': p[3], 'valor2': p[5]}
    elif p[1] == 'SUBSTRAER':
        p[0] = {'accion': p[1], 'valor': p[3], 'valor2': p[5], 'valor3': p[7]}
    elif p[1] == 'HOY':
        p[0] = {'accion': p[1]}
    elif p[1] == 'CONTAR':
        p[0] = {'accion': p[1], 'valor': p[3]}
    elif p[1] == 'SUMA':
        p[0] = {'accion': p[1], 'valor': p[3]}
    elif p[1] == 'CAST':
        p[0] = {'accion': p[1], 'valor': p[3], 'tipo_dato': p[5]}
    else:
        p[0] = {'accion': p[1], 'valor': p[2]}

def p_aritmeticos(p):
    '''
        aritmeticos : expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Aritmetica(id_nodo,p[1], p[2], p[3])

def p_relacionales(p):
    '''
        relacionales : expresion IGUALIGUAL expresion
                    | expresion DIFERENTE expresion
                    | expresion MENOR expresion
                    | expresion MAYOR expresion
                    | expresion MENORIGUAL expresion
                    | expresion MAYORIGUAL expresion
                    | BETWEEN expresion AND expresion
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p) == 4:
        p[0] = Relacional(id_nodo,p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = Relacional(id_nodo,p[2], p[1], p[4])

def p_logicos(p):
    '''
        logicos : expresion AND_OP expresion
                | expresion OR_OP expresion
                | NOT expresion
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p)==4:
        p[0] = Logico(id_nodo,p[1], p[2], p[3])
    else:
        p[0] = Logico(id_nodo,p[1], p[2])  

def p_literal1(p):
    '''
        literal : LNUMERO
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
  
    if((len(str(p[1])) == 1) and(str(p[1]) == "0" or str(p[1]) == "1")):
        p[0] = Literal(id_nodo, p[1], TIPO_DATO.BIT or TIPO_DATO.INT)
    else:
        p[0] = Literal(id_nodo,p[1], TIPO_DATO.INT)

def p_literal2(p):
    '''
        literal : LDECIMAL
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Literal(id_nodo,p[1], TIPO_DATO.DECIMAL)

def p_literal3(p):
    '''
        literal : LFECHA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Literal(id_nodo,p[1], TIPO_DATO.DATE)

def p_literal4(p):
    '''
        literal : LFECHAHORA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Literal(id_nodo,p[1], TIPO_DATO.DATETIME)

def p_literal5(p):
    '''
        literal : LVARCHAR
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Literal(id_nodo,p[1], TIPO_DATO.NCHAR or TIPO_DATO.NVARCHAR)

def p_identificador(p):
    '''
    identificador : ID
                  | ID PUNTO ID
                  | ARROBA ID
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p) == 2:
        p[0] = Identificador(id_nodo, p[1])
    elif len(p) == 3:
        p[0] = Identificador(id_nodo, p[2])
    elif len(p) == 4 and p[2] == '.':
        p[0] = Identificador(id_nodo, p[3], p[1])

def p_error(p):
    errores.append("Sintaxis incorrecta cerca '{}', en linea {}.".format(p.value, p.lineno))

def parse(input):

    # Construir el parser
    parser = yacc()
    lexer.lineno = 1
    ast = parser.parse(input)
    resultado = None
    if len(errores) > 0:
        resultado = '\n'.join(errores)
    else:
        resultado = ast
    errores.clear()

    return resultado