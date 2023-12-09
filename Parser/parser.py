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
    '''
    p[0] = p[1]

def p_sentencia_ddl(p):
    '''
    sentencia_ddl : create
    '''
    p[0] = p[1]

def p_create(p):
    '''
    create : CREATE DATABASE ID PUNTOYCOMA
    '''
    p[0] = "Base de datos creada correctamente"

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Construir el parser
parser = yacc()