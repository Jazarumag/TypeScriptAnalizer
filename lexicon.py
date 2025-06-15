import ply.lex as lex
# Dictionary of reserved words
reserved = {'let': 'LET',
            'const': 'CONST',
            'var': 'VAR',
            'if': 'IF',
            'else':'ELSE',
            'while': 'WHILE',
            'for': 'FOR',
            'switch': 'SWITCH',
            'case': 'CASE',
            'break': 'BREAK',
            'function': 'FUNCTION',
            'return': 'RETURN',
            'void': 'VOID',
            'type': 'TYPE',
            'typeof': 'TYPEOF',
            'class': 'CLASS',
            'this': 'THIS',
            'constructor': 'CONSTRUCTOR',
            'public': 'PUBLIC',
            'private': 'PRIVATE',
            'protected': 'PROTECTED',
            'interface': 'INTERFACE',
            'boolean': 'BOOLEAN',
            'any': 'ANY',
            'default': 'DEFAULT'
            }
# List of token names
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULE',
    'EQUALS', 'EQEQ', 'NOTEQ',
    'LT', 'GT', 'LE', 'GE',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET',
    'SEMICOLON', 'COLON', 'COMMA',
    'ARROW', 'DOT', 'BACKTICK', 'DOLLAR', 'QUESTION',
    'OROR', 'AND', 'NOT', 'PIPE'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
t_EQUALS = r'='
t_EQEQ = r'=='
t_NOTEQ = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_ARROW = r'=>'
t_DOT = r'\.'
t_BACKTICK = r'`'
t_DOLLAR = r'\$'
t_QUESTION = r'\?'
t_OROR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'
t_PIPE = r'\|'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t
def t_NUMBER(t):
    r'(\d+\.\d*|\.\d+|\d+)'
    if '.' in t.value:
        t.value = float(t.value)
    else:    
        t.value = int(t.value)
    return t
def t_STRING(t):
    r'"([^"\\]*(\\.[^"\\]*)*)"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

t_ignore  = ' \t'
def t_COMMENT(t):
    r'//.*'
    pass
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)
lexer = lex.lex()

# Test it out

print("Selecciona el algoritmo a analizar:")
print("1. algoritmo-1.ts")
print("2. algoritmo-2.ts")
print("3. algoritmo-3.ts")
alg_choice = input("Ingresa el número: ")
if alg_choice not in ["1", "2", "3"]:
    print("Seleccionando default: 'algoritmo-3.ts'")
    alg_choice = "3"

file_test = open(f"algoritmo-{alg_choice}.ts", "r")
data = file_test.read()
file_test.close()

import time as time

print("Quién está probando:")
print("1. joshua")
print("2. emily")
print("3. raul")
author_choice = input("Ingresa el número: ")
if author_choice == "1":
    author = "joshua"
elif author_choice == "2":
    author = "emily"
elif author_choice == "3":
    author = "raul"
else:
    print("Seleccionando default: 'general'")
    author = "general"

date = time.strftime("%Y-%m-%d")
hour = time.strftime("%HH%Mm%Ss")
file = open(f'./logs/lexico-{author}-{date}-{hour}.txt', 'a')

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
    file.write(str(tok) + '\n')
file.close()