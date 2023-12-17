from ply.yacc import yacc
from .lexer import tokens, lexer, errores
from .expresiones.literal import *
from .abstract.retorno import *

# Clases
from .abstract.retorno import TIPO_DATO
from .expresiones.tipo_dato import Tipo_Dato
from .expresiones.identificador import Identificador
from .expresiones.alias import Alias
from .expresiones.aritmetica import Aritmetica
from .expresiones.asignacion import Asignacion
from .expresiones.relacional import Relacional
from .expresiones.campo_table import Campo_Table
from .expresiones.constraint import Constraint
from .expresiones.logico import Logico
from .expresiones.expresion import Expresion
from .expresiones.funcion_nativa import Funcion_Nativa
from .instrucciones.use import Use
from .instrucciones.select import Select
from .instrucciones.insert import Insert
from .instrucciones.create import Create
from .instrucciones.drop import Drop
from .instrucciones.truncate import Truncate
from .instrucciones.delete import Delete
from .instrucciones.declare import Declare
from .instrucciones.select_print import Select_Print
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
    instruccion : declaracion_variable
                | sentencia_ddl
                | sentencia_dml
                | llamar_procedure
                | usar_db
                | asignacion
    '''
    p[0] = p[1]

def p_asignacion(p):
    '''
    asignacion  : SET expresion PUNTOYCOMA
    '''
    #p[0] =

def p_usar_db(p):
    '''
    usar_db : USE LVARCHAR PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Use(id_nodo,p[2])

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
            | DECIMAL
            | BIT
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[1] = p[1].lower()
    if p[1] == 'int':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.INT, -1)
    elif p[1] == 'decimal':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.DECIMAL, -1)
    elif p[1] == 'bit':
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
    p[1] = p[1].lower()
    if p[1] == 'date':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.DATE, -1)
    elif p[1] == 'datetime':
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
    p[1] = p[1].lower()
    if p[1] == 'nvarchar':
        p[0] = Tipo_Dato(id_nodo, TIPO_DATO.NVARCHAR, p[3])
    elif p[1] == 'nchar':
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
    if len(p) == 5:
        p[0] = Create(p[2].lower(), p[3], None)
    elif len(p) == 8:
        p[0] = Create(p[2].lower(), p[3], p[5])
    else:
        p[0] = p[1]

def p_campos_table(p):
    '''
    campos_table : campos_table COMA identificador tipo_dato constraint
                 | campos_table COMA identificador tipo_dato
                 | identificador tipo_dato constraint
                 | identificador tipo_dato
    '''
    if len(p) == 6:
        p[1].append(Campo_Table(p[3], p[4], p[5]))
        p[0] = p[1]
    elif len(p) == 5:
        p[1].append(Campo_Table(p[3], p[4], None))
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = [Campo_Table(p[1], p[2], p[3])]
    elif len(p) == 3:
        p[0] = [Campo_Table(p[1], p[2], None)]

def p_parametros(p):
    '''
    parametros : parametros COMA identificador tipo_dato
                | identificador tipo_dato
    '''
    p[0] = p[1]

def p_constraint(p):
    '''
    constraint : PRIMARY KEY
              | NOT NULL
              | REFERENCES identificador IZQPAREN identificador DERPAREN
    '''
    p[1] = p[1].lower()
    if p[1] == 'primary':
        p[0] = Constraint('primary key', None, None)
    elif p[1] == 'not':
        p[0] = Constraint('not null', None, None)
    elif p[1] == 'references':
        p[0] = Constraint('references', p[2], p[4])

def p_alter(p):
    '''
    alter : ALTER TABLE identificador accion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_accion(p):
    '''
    accion : ADD COLUMN campos_table
           | DROP COLUMN identificador
    '''
    p[0] = p[1]

def p_drop(p):
    '''
    drop : DROP DATABASE identificador PUNTOYCOMA
         | DROP TABLE identificador PUNTOYCOMA
         | DROP PROCEDURE identificador PUNTOYCOMA
         | DROP FUNCTION identificador PUNTOYCOMA
    '''
    p[0] = Drop(p[2].lower(), p[3])

def p_truncate(p):
    '''
    truncate : TRUNCATE TABLE identificador PUNTOYCOMA
    '''
    p[0] = Truncate(p[3])

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
    '''
    if len(p) == 4:
        p[0] = Select_Print(p[2])
    elif len(p) == 6 and p[2] == '*':
        p[0] = Select(p[4], [p[2]], None)
    elif len(p) == 6 and p[3].lower() == 'from':
        p[0] = Select(p[4], p[2], None)
    elif len(p) == 8 and p[2] == '(':
        p[0] = Select(p[6], p[3], None)
    elif len(p) == 8 and p[2] == '*':
        p[0] = Select(p[4], [p[2]], p[6])
    elif len(p) == 8 and p[3].lower() == 'from':
        p[0] = Select(p[4], p[2], p[6])
    elif len(p) == 10 and p[2] == '(':
        p[0] = Select(p[6], p[3], p[8])

def p_insert(p):
    '''
    insert : INSERT INTO identificador IZQPAREN lista_expresiones DERPAREN VALUES IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
    '''
    p[0] = Insert(p[3], p[5], p[9])

def p_update(p):
    '''
    update : UPDATE identificador SET lista_expresiones WHERE condicion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_delete(p):
    '''
    delete : DELETE FROM identificador WHERE condicion PUNTOYCOMA
           | DELETE FROM identificador PUNTOYCOMA
    '''
    if len(p) == 7:
        p[0] = Delete(p[3], p[5])
    elif len(p) == 5:
        p[0] = Delete(p[3], None)

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
                | asignacion_exp
                | identificador
                | alias
                | IF IZQPAREN lista_expresiones DERPAREN
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p) == 2:
        p[0] = Expresion(id_nodo, p[1])
    elif len(p) == 4:
        p[0] = Expresion(id_nodo, p[2])
    elif len(p) == 5:
        #TODO: por probar 
        p[0] = Expresion(id_nodo, p[4])

def p_alias(p):
    '''
        alias : expresion AS ID
            | expresion ID
    '''
    global contador
    id_nodo = str(abs(hash("AS")) + contador)
    contador += 1
    if len(p) == 3:
        p[0] = Alias(id_nodo, p[1], p[2])
    elif len(p) == 4:
        p[0] = Alias(id_nodo, p[1], p[3])

def p_asignacion_exp(p):
    '''
        asignacion_exp : ID IGUAL expresion
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[0] = Asignacion(id_nodo,p[1], p[2], p[3])

def p_funcion_nativa(p):
    '''
        funcion_nativa : CONCATENA IZQPAREN lista_expresiones DERPAREN
                          | SUBSTRAER IZQPAREN lista_expresiones DERPAREN
                          | HOY IZQPAREN DERPAREN
                          | CONTAR IZQPAREN POR DERPAREN
                          | SUMA IZQPAREN expresion DERPAREN
                          | CAST IZQPAREN expresion AS tipo_dato DERPAREN
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    p[1] = p[1].lower()
    if p[1] == 'concatena':
        p[0] = Funcion_Nativa(id_nodo,p[1], p[3])
    elif p[1] == 'substraer':
        p[0] = Funcion_Nativa(id_nodo,p[1], p[3])
    elif p[1] == 'hoy':
        p[0] = Funcion_Nativa(id_nodo,p[1], None)
    elif p[1] == 'contar':
        p[0] = Funcion_Nativa(id_nodo,p[1], None)
    elif p[1] == 'suma':
        p[0] = Funcion_Nativa(id_nodo,p[1], p[3])
    elif p[1] == 'cast':
        p[0] = {'accion': p[1], 'valor': p[3], 'tipo_dato': p[5]}

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
    id_nodo = str(abs(hash("relacionalesOLC2")) + contador)
    contador += 1
    if len(p) == 4:
        p[0] = Relacional(id_nodo,p[1], p[2], p[3])
    elif len(p) == 5:
        p[0] = Relacional(id_nodo,p[2], p[1], p[4])

def p_logicos(p):
    '''
        logicos : expresion AND_OP expresion
                | expresion OR_OP expresion
                | NOT_OP expresion
    '''
    global contador
    id_nodo = str(abs(hash("logicosOLC2")) + contador)
    contador += 1
    if len(p) == 4:
        p[0] = Logico(id_nodo,p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = Logico(id_nodo,None, p[1],p[2])

def p_literal1(p):
    '''
        literal : LNUMERO
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if((len(str(p[1])) == 1) and(str(p[1]) == "0" or str(p[1]) == "1")):
        p[0] = Literal(id_nodo,p[1], TIPO_DATO.BIT or TIPO_DATO.INT)
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