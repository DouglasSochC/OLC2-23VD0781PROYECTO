from ply.yacc import yacc
from .lexer import tokens, lexer, errores

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

def p_declaracion_variable(p):
    '''
    declaracion_variable : DECLARE identificador tipo_dato PUNTOYCOMA
    '''
    p[0] = {'accion':p[1]}

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
    p[0] = p[1]

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
    p[0] = p[1]

def p_alter(p):
    '''
    alter : ALTER TABLE identificador accion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_accion(p):
    '''
    accion : ADD COLUMN identificador tipo_dato
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
    p[0] = p[1]

def p_truncate(p):
    '''
    truncate : TRUNCATE TABLE identificador PUNTOYCOMA
    '''
    p[0] = p[1]

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
                | RETURN expresion PUNTOYCOMA
                | expresion
    '''
    p[0] = p[1]

def p_select(p):
    '''
        select : SELECT POR FROM identificador
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM identificador
               | SELECT lista_expresiones FROM identificador
               | SELECT POR FROM identificador WHERE expresion PUNTOYCOMA
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM identificador WHERE expresion PUNTOYCOMA
               | SELECT lista_expresiones FROM identificador WHERE expresion PUNTOYCOMA
               | SELECT lista_expresiones PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN FROM identificador PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN FROM identificador PUNTOYCOMA
               | SELECT identificador IZQPAREN DERPAREN FROM identificador WHERE expresion PUNTOYCOMA
               | SELECT identificador IZQPAREN lista_expresiones DERPAREN FROM identificador WHERE expresion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_insert(p):
    '''
    insert : INSERT INTO identificador IZQPAREN lista_expresiones DERPAREN VALUES IZQPAREN lista_expresiones DERPAREN PUNTOYCOMA
    '''
    p[0] = p[1]

def p_update(p):
    '''
    update : UPDATE identificador SET lista_expresiones WHERE expresion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_delete(p):
    '''
    delete : DELETE FROM identificador WHERE expresion PUNTOYCOMA
    '''
    p[0] = p[1]

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