import ply.lex as lex
# List of token names
tokens = [
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'EQEQ', 'NOTEQ',
    'LT', 'GT', 'LE', 'GE',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COLON', 'COMMA',
    'ARROW'
] + [
    'LET', 'CONST', 'VAR',
    'IF', 'ELSE',
    'FUNCTION', 'RETURN',
    'TYPE', 'INTERFACE',
    'NUMBER_TYPE', 'STRING_TYPE', 'BOOLEAN_TYPE', 'ANY_TYPE'
]

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
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
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_ARROW = r'=>'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    return t
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to integer
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
data = '''
3 + 4 * 10
  + -20 *2
'''
# ---------------------------------- Test the lexer with some input--------------------------------
import time as time
# Give the lexer some input

author = "joshua"
date = time.strftime("%Y-%m-%d")  # Get current
hour = time.strftime("%HH%Mm%Ss")  # Get current hour
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