from ply.lex import lex

errores = []

reservadas = {
    # Sentencias DDL
    'create': 'CREATE',
    'alter': 'ALTER',
    'drop': 'DROP',
    'declare': 'DECLARE',
    'set': 'SET',
    'into': 'INTO',
    'between': 'BETWEEN',
    'truncate': 'TRUNCATE',
    'as': 'AS',
    'values': 'VALUES',
    'return': 'RETURN',
    'begin': 'BEGIN',
    'end': 'END',
    'add': 'ADD',
    'exec': 'EXEC',
    'and' : 'AND',
    'use' : 'USE',
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'then' : 'THEN',

    # Tipos de objeto
    'database': 'DATABASE',
    'table': 'TABLE',
    'column': 'COLUMN',
    'procedure': 'PROCEDURE',
    'function': 'FUNCTION',

    # Tipos de dato
    'int': 'INT',
    'bit': 'BIT',
    'decimal': 'DECIMAL',
    'datetime': 'DATETIME',
    'date': 'DATE',
    'nchar': 'NCHAR',
    'nvarchar': 'NVARCHAR',

    # Constraint
    'primary': 'PRIMARY',
    'null': 'NULL',
    'key': 'KEY',
    'references': 'REFERENCES',

    # Sentencia DML
    'select': 'SELECT',
    'insert': 'INSERT',
    'update': 'UPDATE',
    'delete': 'DELETE',
    'from': 'FROM',
    'where': 'WHERE',

    # Funciones nativas
    'concatena': 'CONCATENA',
    'substraer': 'SUBSTRAER',
    'hoy': 'HOY',
    'contar': 'CONTAR',
    'suma': 'SUMA',
    'cast': 'CAST',
}

tokens = [
    # Expresiones aritmeticas
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',

    # Expresiones relacionales
    'IGUALIGUAL',
    'DIFERENTE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'MAYOR',
    'MENOR',

    # Expresiones logicas
    'OR_OP',
    'AND_OP',
    'NOT',
    'IZQPAREN',
    'DERPAREN',

    # Literal
    'LNUMERO',
    'LDECIMAL',
    'LFECHA',
    'LFECHAHORA',
    'LVARCHAR',

    # Otros
    'ID',
    'COMA',
    'PUNTO',
    'ARROBA',
    'IGUAL',
    'PUNTOYCOMA'
] + list(reservadas.values())

# Caracteres ignorados
t_ignore = ' \t'

# Expresiones aritmeticas
t_MAS = r'\+'
t_MENOS = r'\-'
t_POR = r'\*'
t_DIVIDIDO = r'\/'

# Expresiones relacionales
t_IGUALIGUAL = r'\=\='
t_DIFERENTE = r'\!\='
t_MENORIGUAL = r'\<\='
t_MAYORIGUAL = r'\>\='
t_MAYOR = r'\>'
t_MENOR = r'\<'

# Expresiones logicas
t_OR_OP = r'\|\|'
t_AND_OP = r'\&\&'
t_NOT = r'\!'
t_IZQPAREN = r'\('
t_DERPAREN = r'\)'

# Literal
t_LDECIMAL = r'\d+\.\d+'
t_LFECHA = r'\d{2}-\d{2}-\d{4}'
t_LFECHAHORA = r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}'
t_LVARCHAR =  r'\"([^\\\n]|(\\.))*?\"'

# Otros
t_IGUAL = r'\='
t_COMA = r'\,'
t_PUNTO = r'\.'
t_ARROBA = r'\@'
t_PUNTOYCOMA = r'\;'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_LNUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    texto = t.value.split('\n')[0]
    caracter_error = list(texto)[0]
    errores.append("Caracter ilegal '{}' en '{}', linea {}".format(caracter_error, texto, t.lineno))
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()