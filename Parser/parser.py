from ply.yacc import yacc
from .lexer import tokens, lexer, errores

# Clases
from .instrucciones.create import Create

# Operadores de precedencia
precedence = (
    ('left', 'OR'),
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
    '''
    p[0] = p[1]

def p_sentencia_ddl(p):
    '''
        sentencia_ddl : drop
                      | alter
                      | truncate
                      | create
    '''
    p[0] = p[1]

def p_create(p):
    '''
        create : CREATE tipo_objeto identificador PUNTOYCOMA
               | CREATE tipo_objeto identificador IZQPAREN parametros DERPAREN PUNTOYCOMA
               | CREATE tipo_objeto ID IZQPAREN parametros DERPAREN AS lista_sentencias_dml
               | CREATE tipo_objeto ID AS lista_sentencias_dml
               | CREATE tipo_objeto ID IZQPAREN parametros DERPAREN RETURN tipo AS BEGIN lista_sentencias_dml END PUNTOYCOMA
               | CREATE tipo_objeto ID  RETURN tipo AS BEGIN lista_sentencias_dml END PUNTOYCOMA
               | CREATE tipo_objeto ID  AS BEGIN lista_sentencias_dml END PUNTOYCOMA
    '''
    if len(p) == 5:
        p[0] = Create(p.lineno(1), p.lexpos(1), p[2], p[3])
    elif len(p) == 8:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'parametros': p[5]}
    elif len(p) == 10:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'parametros': p[5], 'sentencias': p[8]}
    elif len(p) == 7:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'sentencias': p[5]}
    elif len(p) == 13:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'parametros': p[5], 'tipo_retorno': p[7], 'sentencias': p[10]}
    else:
        p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3], 'tipo_retorno': p[5], 'sentencias': p[8]}

def p_parametros(p):
    '''
    parametros : parametros COMA identificador tipo constrain
                | parametros COMA identificador tipo
                | identificador tipo constrain
                | identificador tipo
    '''
    if len(p) == 6:
        p[0] = {'identificador': p[3], 'tipo': p[4], 'constrain': p[5]}
    elif len(p) == 5:
        p[0] = {'identificador': p[3], 'tipo': p[4]}
    elif len(p) == 4:
        p[0] = {'identificador': p[2], 'tipo': p[3], 'constrain': p[4]}
    else:
        p[0] = {'identificador': p[2], 'tipo': p[3]}

def p_constrain(p):
    '''
    constrain : PRIMARY KEY
              | NOT NULL
              | REFERENCES ID IZQPAREN ID DERPAREN
    '''
    if len(p) == 3:
        p[0] = {'constrain': p[1], 'tipo': p[2]}
    else:
        p[0] = {'constrain': p[1], 'tipo': p[2], 'tabla': p[3], 'columna': p[5]}

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

def p_truncate(p):
    '''
    truncate : TRUNCATE tipo_objeto identificador PUNTOYCOMA
    '''
    p[0] = {'accion': p[1], 'tipo': p[2], 'nombre': p[3]}


def p_llamar_procedure(p):
    '''
    llamar_procedure : EXEC lista_expresiones PUNTOYCOMA
    '''
    p[0] = {'accion': p[1], 'parametros': p[3]}

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

def p_sentencia_dml(p):
    '''
    sentencia_dml : insert
                | delete
                | update
                | select
                | RETURN expresion PUNTOYCOMA
                | expresion
    '''
    p[0] = p[1]

def p_select(p):
    '''
        select : SELECT lista_expresiones FROM ID PUNTOYCOMA
                | SELECT IZQPAREN lista_expresiones DERPAREN FROM ID PUNTOYCOMA
                | SELECT lista_expresiones FROM ID WHERE lista_expresiones PUNTOYCOMA
                | SELECT IZQPAREN lista_expresiones DERPAREN FROM ID WHERE lista_expresiones PUNTOYCOMA
                | SELECT lista_expresiones PUNTOYCOMA
                | SELECT identificador IZQPAREN DERPAREN PUNTOYCOMA
                | SELECT identificador IZQPAREN lista_expresiones  DERPAREN PUNTOYCOMA
                | SELECT identificador IZQPAREN DERPAREN FROM ID PUNTOYCOMA
                | SELECT identificador IZQPAREN lista_expresiones  DERPAREN FROM ID PUNTOYCOMA
                | SELECT identificador IZQPAREN DERPAREN FROM ID WHERE lista_expresiones PUNTOYCOMA
                | SELECT identificador IZQPAREN lista_expresiones  DERPAREN FROM ID WHERE lista_expresiones PUNTOYCOMA
    '''
    if len(p) == 6:
        p[0] = {'accion': p[1], 'columnas': p[2], 'tabla': p[4]}
    elif len(p) == 7:
        p[0] = {'accion': p[1], 'columnas': p[3], 'tabla': p[5]}
    elif len(p) == 8:
        p[0] = {'accion': p[1], 'columnas': p[2], 'tabla': p[5], 'condicion': p[7]}

def p_insert(p):
    '''
    insert : INSERT INTO lista_expresiones VALUES IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
            | INSERT INTO lista_expresiones IZQPAREN lista_expresiones DERPAREN VALUES IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
    '''
    if len(p) == 9:
        p[0] = {'accion': p[1], 'tipo': p[2], 'columnas': p[3], 'valores': p[6]}
    else:
        p[0] = {'accion': p[1], 'tipo': p[2], 'columnas': p[3], 'valores': p[9]}

def p_delete(p):
    '''
    delete : DELETE FROM lista_expresiones WHERE lista_expresiones PUNTOYCOMA
    '''
    p[0] = {'accion': p[1], 'tipo': p[2], 'tabla': p[3], 'condicion': p[5]}

def p_update(p):
    '''
    update : UPDATE lista_expresiones SET lista_expresiones WHERE lista_expresiones PUNTOYCOMA
            | UPDATE IZQPAREN lista_expresiones DERPAREN SET IZQPAREN lista_expresiones DERPAREN WHERE lista_expresiones PUNTOYCOMA
    '''
    if len(p) == 8:
        p[0] = {'accion': p[1], 'expresion': p[2], 'accion': p[3], 'valores': p[4], 'condicion': p[6]}
    else:
        p[0] = {'accion': p[1], 'expresiones': p[3], 'accion': p[5], 'valores': p[7], 'condicion': p[10]}

def p_lista_expresiones(p):
    '''
        lista_expresiones : lista_expresiones COMA expresion
                         | lista_expresiones AND expresion
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
    '''
    if(len(p) == 4):
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_asignacion(p):
    '''
        asignacion : expresion IGUAL expresion
                   | SET expresion
    '''
    if len(p) == 4:
        p[0] = {'accion': p[1], 'tipo': p[2], 'valor': p[3]}
    else:
        p[0] = {'accion': p[1], 'valor': p[2]}

def p_funcion_nativa(p):
    '''
        funcion_nativa : CONCATENA IZQPAREN expresion COMA expresion DERPAREN
                          | SUBSTRAER IZQPAREN expresion COMA expresion COMA expresion DERPAREN
                          | HOY IZQPAREN DERPAREN
                          | CONTAR IZQPAREN expresion DERPAREN
                          | SUMA IZQPAREN expresion DERPAREN
                          | CAST IZQPAREN expresion AS tipo DERPAREN
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
        p[0] = {'accion': p[1], 'valor': p[3], 'tipo': p[5]}
    else:
        p[0] = {'accion': p[1], 'valor': p[2]}

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
                    | BETWEEN expresion AND expresion
    '''
    if p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]
    elif p[1] == 'BETWEEN': p[0] = p[1] >= p[3]

def p_logicos(p):
    '''
        logicos : expresion AND_OP expresion
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
                | NULL
    '''
    p[0] = p[1]



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
    seg_string : NVARCHAR IZQPAREN LNUMERO DERPAREN
                | NCHAR IZQPAREN LNUMERO DERPAREN
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