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
    '''
    p[0] = p[1]

def p_sentencia_ddl(p):
    '''
        sentencia_ddl : drop
                      | alter
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
    p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'accion_alter': p[4]}

def p_accion(p):
    '''
    accion : ADD COLUMN identificador tipo
           | DROP identificador
    '''
    if len(p) == 5:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'tipo_dato': p[4]}
    else:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3]}


def p_drop(p):
    '''
    drop : DROP tipo_objeto identificador PUNTOYCOMA
    '''
    p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3]}


def p_declaracion_variable(p):
    '''
    declaracion_variable : DECLARE identificador tipo PUNTOYCOMA
    '''
    p[0] = {'accion':p[1], 'tipo': p[3], 'identificador': p[2]}

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
            | DECIMAL IZQPAREN LNUMERO COMA LNUMERO DERPAREN
            | BIT
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {'tipo_dato': p[1], 'precision': p[3], 'escala': p[5]}

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
    p[0] = {'tipo_cadena': p[1], 'longitud': p[3]}

def p_identificador(p):
    '''
    identificador : ID
                  | ID PUNTO ID
                  | ARROBA ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'{p[1]}.{p[3]}'
    else:
        p[0] = f'@{p[2]}'

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Construir el parser
parser = yacc()