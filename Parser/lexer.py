from ply.lex import lex

errors = ()

reserved = {
    # Sentences
    'select': 'SELECT',
    
    # User functions
    'create': 'CREATE',
    'function': 'FUNCTION',
    'returns': 'RETURNS',
    'as': 'AS',
    'begin': 'BEGIN',
    'return': 'RETURN',
    'end': 'END',
    
    # Native functions
    'concatena': 'CONCATENA',
    'substraer': 'SUBSTRAER',
    'hoy': 'HOY',
    'contar': 'CONTAR',
    'suma': 'SUMA',
    'cast': 'CAST',

    # Data types
    'int': 'INT',
    'bit': 'BIT',
    'decimal': 'DECIMAL',
    'datetime': 'DATETIME',
    'date': 'DATE',
    'nchar': 'NCHAR',
    'nvarchar': 'NVARCHAR',
}

tokens = (
    # Arithmetic Expressions
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    # Comparison Operators
    'IGUAL',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MENORIGUAL',
    'MAYORIGUAL',

    # Logical Expressions
    'OR',
    'AND',
    'IZQPAREN',
    'DERPAREN',
)

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_IGUAL = r'\='
t_IZQPAREN = r'\('
t_DERPAREN = r'\)'
# t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()