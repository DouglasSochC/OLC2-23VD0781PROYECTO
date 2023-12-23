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
        instruccion : declare
                    | set
                    | if
                    | while
                    | comando_sql
                    | RETURN expresion PUNTOYCOMA
    '''
    p[0] = p[1]

def p_comando_sql(p):
    '''
        comando_sql : sentencia_ddl
                    | sentencia_dml
                    | exec
                    | use
    '''
    p[0] = p[1]

def p_set(p):
    '''
    set  : SET identificador IGUAL expresion PUNTOYCOMA
    '''
    p[0] = Set(None, p[2], p[4])





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
               | CREATE PROCEDURE identificador IZQPAREN parametros DERPAREN AS BEGIN instrucciones END PUNTOYCOMA
               | CREATE FUNCTION identificador IZQPAREN parametros DERPAREN RETURN tipo_dato AS BEGIN instrucciones END PUNTOYCOMA
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p) == 5:
        p[0] = Create(id_nodo, p[2].lower(), p[3], None, None, None, None)
    elif len(p) == 8:
        p[0] = Create(id_nodo, p[2].lower(), p[3], p[5], None, None, None)
    elif len(p) == 12:
        p[0] = Create(id_nodo, p[2].lower(), p[3], None, p[5], p[9], None)
    elif len(p) == 14:
        p[0] = Create(id_nodo, p[2].lower(), p[3], None, p[5], p[11], p[8])


def p_parametros(p):
    '''
        parametros : parametros COMA identificador AS tipo_dato
                   | identificador AS tipo_dato
                   | parametros COMA identificador tipo_dato
                   | identificador tipo_dato
    '''
    if len(p) == 6:
        p[1].append(Parametro(p[3], p[5]))
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = [Parametro(p[1], p[3])]
    elif len(p) == 5:
        p[1].append(Parametro(p[3], p[4]))
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = [Parametro(p[1], p[2])]







def p_sentencia_dml(p):
    '''
        sentencia_dml : select
                      | insert
                      | update
                      | delete
    '''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_select(p):
    '''
        select : SELECT POR FROM lista_expresiones PUNTOYCOMA
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM lista_expresiones PUNTOYCOMA
               | SELECT lista_expresiones FROM lista_expresiones PUNTOYCOMA
               | SELECT POR FROM lista_expresiones WHERE condicion PUNTOYCOMA
               | SELECT IZQPAREN lista_expresiones DERPAREN FROM lista_expresiones WHERE condicion PUNTOYCOMA
               | SELECT lista_expresiones FROM lista_expresiones WHERE condicion PUNTOYCOMA
               | SELECT lista_expresiones PUNTOYCOMA
    '''
    if len(p) == 4:
        p[0] = Select(None, p[2], None)
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





def p_if(p):
    '''
        if : IF expresion THEN instrucciones ELSE instrucciones END IF PUNTOYCOMA
           | IF expresion THEN instrucciones END IF PUNTOYCOMA
           | IF expresion BEGIN instrucciones END ELSE BEGIN instrucciones END
           | IF expresion BEGIN instrucciones END
    '''
    global contador
    id_nodo = str(abs(hash(p[1])) + contador)
    contador += 1
    if len(p) == 10 and p[3].lower() == 'then':
        p[0] = If_I(id_nodo, p[2], p[4], p[6])
    elif len(p) == 8:
        p[0] = If_I(id_nodo, p[2], p[4], None)
    elif len(p) == 10 and p[3].lower() == 'begin':
        p[0] = If_I(id_nodo, p[2], p[4], p[8])
    elif len(p) == 6:
        p[0] = If_I(id_nodo, p[2], p[4], None)


