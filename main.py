from Parser.parser import parser

# Parseando expresion
ast = parser.parse('2 * 3 + 4 * (5 - x)')
print(ast)