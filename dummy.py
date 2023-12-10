from ply.yacc import yacc
from .lexer import tokens, lexer, errors

# Operadores de precedencia
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'IGUALIGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENORIGUAL', 'MAYORIGUAL'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IZQPAREN', 'DERPAREN')
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
    if p[2] == "":
        p[1].append(p[2])
    p[0] = p[1]

def p_instrucciones_lista2(p):
    '''
    instrucciones : instruccion
    '''
    if p[1] == "":
        p[0] = []
    else:
        p[0] = [p[1]]

def p_instruccion(p):
    '''
    instruccion : sentencia_ddl 
                | declaracion
                | sentencia_dml
    '''
    p[0] = p[1]

#TODO: -LA PRODUCCION INICIALMENTE ESTABA ASI DECLARACION_VARIABLE -> 'DECLARE' TIPO ID ';'
#TODO: NO RECONOCE LA ARROBA COMO IDENTIFICADODR
def p_declaracion(p):
    '''
    declaracion : DECLARE identificador tipo PUNTOYCOMA
    '''
    p[0] = f"Declaración de variable '{p[2]}' como '{p[3]}' realizada."

def p_tipo(p):
    '''
    tipo : seg_num 
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
    p[0] = p[1]

def p_seg_date(p):
    '''
    seg_date : DATE
            | DATETIME
    '''
    p[0] = p[1]

def p_seg_string(p):
    '''
    seg_string : NCHAR IZQPAREN LNUMERO DERPAREN
                | NVARCHAR IZQPAREN LNUMERO DERPAREN
    '''
    p[0] = p[1]

def p_sentencia_ddl(p):
    '''
    sentencia_ddl : create
                  | drop
                  | alter
                  | truncate
    '''
    p[0] = p[1]


#TODO: PROBAR LA SEGUNDA PRODUCCION DE CREATE
def p_create(p):
    '''
    create : CREATE tipo_objeto ID PUNTOYCOMA
           | CREATE tipo_objeto ID IZQPAREN parametros DERPAREN PUNTOYCOMA
    '''
    p[0] = f"Creación de objeto '{p[2]}' con nombre '{p[3]}' realizada."


def p_parametros(p):
    '''
    parametros : parametros COMA identificador tipo constrain
                | identificador tipo constrain
                | parametros COMA identificador tipo
                | identificador tipo
    '''
    if len(p) == 6:
        p[0] = f"Parámetro '{p[3]}' de tipo '{p[4]}' con constraint '{p[5]}' agregado."
        p[0] = p[1]
    elif len(p) == 5:
        p[0] = f"Parámetro '{p[3]}' de tipo '{p[4]}' agregado."
    elif len(p) == 4:
        p[0] = f"Parámetro '{p[2]}' de tipo '{p[3]}' con constraint '{p[4]}' agregado."
        p[0] = p[1]
    else:
        p[0] = f"Parámetro '{p[2]}' de tipo '{p[3]}' agregado."

def p_constrain(p):
    '''
    constrain : NOT NULL PRIMARY KEY
              | NOT NULL
              | NULL
              | FOREIGN KEY identificador  REFERENCES identificador IZQPAREN identificador DERPAREN
    '''
    p[0] = p[1]


def p_tipo_objeto(p):
    '''
    tipo_objeto : DATABASE
                | TABLE
                | PROCEDURE
                | FUNCTION
    '''
    p[0] = p[1]

def p_alter(p):
    '''
    alter : ALTER tipo_objeto identificador accion PUNTOYCOMA
    '''
    p[0] = f"Alteración de objeto '{p[2]}' con nombre '{p[3]}' realizada '{p[4]}'."

def p_accion(p):
    '''
        accion : ADD identificador tipo
                | DROP identificador
    '''
    p[0] = p[1]

def p_drop(p):
    '''
    drop : DROP tipo_objeto identificador PUNTOYCOMA
    '''
    p[0] = f"Eliminación de objeto '{p[2]}' con nombre '{p[3]}' realizada."

def p_truncate(p):
    '''
    truncate : TRUNCATE identificador PUNTOYCOMA
    '''
    p[0] = f"Truncamiento de tabla '{p[3]}' realizada."


def p_sentencia_dml(p):
    '''
    sentencia_dml : delete
                 
    '''
    p[0] = p[1]


def p_delete(p):
    '''
    delete : DELETE FROM expresion WHERE expresion PUNTOYCOMA
    '''
    p[0] = f"Eliminación de tuplas de tabla '{p[3]}' realizada."


def p_lista_expresiones(p):
    '''
        lista_expresiones : lista_expresiones COMA expresion
                         | expresion
    '''
    if len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    elif len(p) == 2:
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
    '''
    p[0] = p[1]

def p_asignacion(p):
    '''
        asignacion : expresion IGUAL expresion
                   | SET expresion
    '''
    if p[1] == '=':
        p[0] = f"Asignación de '{p[1]}' a '{p[3]}' realizada."
    elif p[1] == 'SET':
        p[0] = f"Asignación de '{p[2]}' realizada."


def p_funcion_nativa(p):
    '''
        funcion_nativa : CONCATENA IZQPAREN expresion DERPAREN
                          | SUBSTRAER IZQPAREN expresion COMA expresion COMA expresion DERPAREN
                          | HOY IZQPAREN DERPAREN
                          | CONTAR IZQPAREN expresion DERPAREN
                          | SUMA IZQPAREN expresion DERPAREN
                          | CAST IZQPAREN expresion DERPAREN 
    '''
    if p[1] == 'CONCATENA':
        p[0] = f"Concatenación de '{p[3]}' realizada."
    elif p[1] == 'SUBSTRAER':
        p[0] = f"Substracción de '{p[3]}' realizada."
    elif p[1] == 'HOY':
        p[0] = f"Obtención de fecha actual realizada."
    elif p[1] == 'CONTAR':
        p[0] = f"Conteo de '{p[3]}' realizada."
    elif p[1] == 'SUMA':
        p[0] = f"Suma de '{p[3]}' realizada."
    elif p[1] == 'CAST':
        p[0] = f"Casting de '{p[3]}' realizada."

def p_aritmeticos(p):
    '''
        aritmeticos : expresion MAS expresion
                    | expresion MENOS expresion
                    | expresion POR expresion
                    | expresion DIVIDIDO expresion
    '''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_relacionales(p):
    '''
        relacionales : expresion IGUALIGUAL expresion
                    | expresion DIFERENTE expresion
                    | expresion MENOR expresion
                    | expresion MAYOR expresion
                    | expresion MENORIGUAL expresion
                    | expresion MAYORIGUAL expresion
    '''
    if p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]

def p_logicos(p):
    '''
        logicos : expresion AND expresion
                | expresion OR expresion
                | NOT expresion
    '''
    if p[1] == '&&': p[0] = p[1] and p[3]
    elif p[1] == '||': p[0] = p[1] or p[3]
    elif p[1] == '!': p[0] = not p[2]

def p_literal(p):
    '''
        literal : LNUMERO
                | LDECIMAL
                | LFECHA
                | LFECHAHORA
                | LVARCHAR
    '''
    p[0] = p[1]

def p_identificador(p):
    '''
    identificador : ID
                  | ID PUNTO ID
                  | ARROBA ID
    '''
    p[0] = p[1]

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Construir el parser
parser = yacc()

#ENTRADA DE PRUEBA
'''
DROP DATABASE compi2;
DECLARE @variable INT;
DECLARE @variable2 DECIMAL(10,2);
DECLARE @variable2 NVARCHAR(10);
Alter table products add column inventario decimal(10,2)

CREATE DATABASE julian;
INSERT INTO links (url, name, last_update)
VALUES("https://www.google.com","Google","2013-06-01");

DELETE FROM COMPANY WHERE ID = 2;
UPDATE COMPANY SET SALARY = 15000 WHERE ID = 3;

EXEC SP_CARGA_DATOS;
EXEC inicializacomisiones @Ciudad ="Guatemala" ,@Departamento = "Guatemala";


'''