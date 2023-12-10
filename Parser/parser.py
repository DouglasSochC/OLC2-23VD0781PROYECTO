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
    seg_string : NCHAR
                | NVARCHAR
    '''
    p[0] = p[1]

def p_sentencia_ddl(p):
    '''
    sentencia_ddl : create
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