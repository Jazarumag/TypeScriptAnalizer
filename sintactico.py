import ply.yacc as yacc
from lexicon import tokens
import time
import os

def p_assignment(p):
    '''assignment : LET IDENTIFIER EQUALS value SEMICOLON 
                    | LET IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | LET IDENTIFIER COLON data_type SEMICOLON
                    | CONST IDENTIFIER EQUALS value SEMICOLON
                    | CONST IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | VAR IDENTIFIER EQUALS value SEMICOLON
                    | VAR IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | VAR IDENTIFIER COLON data_type SEMICOLON'''
    
def p_statement(p): 
    '''statement : assignment
                    | expression SEMICOLON
                    | if_statement
                    | print
                    | input
                    | class_declaration'''
    
def p_statement_block(p):
    '''statement_block : LBRACE statement_list RBRACE
                            | statement'''
    
def p_statement_list(p):
    '''statement_list : statement
                        | statement statement_list'''
    
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement_block
                        | IF LPAREN expression RPAREN statement_block ELSE statement_block'''

def p_data_type(p):
    '''data_type : STRING_TYPE
                    | NUMBER_TYPE
                    | BOOLEAN_TYPE
                    | CHAR_TYPE
                    | array_type'''

def p_body(p):
    '''body : sentence
                | sentence body'''
    
def p_sentence(p):
    '''sentence : assignment
                    | expression '''
    
def p_expression_plus(p):
    'expression : expression PLUS term'

def p_expression_minus(p):
    'expression : expression MINUS term'

def p_term_times(p):
    'term : term TIMES factor'

def p_term_div(p):
    'term : term DIVIDE factor'

def p_term_factor(p):
    'term : factor'

def p_factor_number(p):
    'factor : NUMBER'

def p_value(p):
    '''value : NUMBER
                | STRING
                | CHARACTER
                | IDENTIFIER '''
    
def p_array(p):
    '''array : LBRACKET RBRACKET
                | LBRACKET element_list RBRACKET'''
    
def p_element_list(p):
    '''element_list : value
                        | value COMMA element_list'''
    
def p_array_type(p):
    '''array_type : NUMBER_TYPE LBRACKET RBRACKET
                    | STRING_TYPE LBRACKET RBRACKET
                    | BOOLEAN_TYPE LBRACKET RBRACKET
                    | ANY LBRACKET RBRACKET'''

def p_expression_value(p):
    'expression : value'
    
def p_error(p):
    print("Syntax error in input!")

def p_print(p):
    '''print : IDENTIFIER DOT IDENTIFIER LPAREN value RPAREN SEMICOLON'''

def p_input(p):
    '''input : IDENTIFIER EQUALS IDENTIFIER LPAREN value RPAREN SEMICOLON'''

def p_expression_logical(p):
    '''expression : expression AND expression
                  | expression OROR expression
                  | NOT expression
                  | expression EQEQ expression
                  | expression NOTEQ expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression'''

def p_empty(p):
    'empty :'
    pass

def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER LBRACE class_body RBRACE'''

def p_class_body(p):
    '''class_body : property
                  | empty'''

def p_property(p):
    '''property : IDENTIFIER COLON data_type SEMICOLON'''

def p_program(p):
    '''program : statement_list'''

def elegir_algoritmo():
    print("Selecciona el algoritmo a analizar:")
    print("1. algoritmo-1.ts")
    print("2. algoritmo-2.ts")
    print("3. algoritmo-3.ts")
    alg_choice = input("Ingresa el número: ")
    if alg_choice not in ["1", "2", "3"]:
        print("Seleccionando default: 'algoritmo-3.ts'")
        alg_choice = "3"
    return alg_choice

def elegir_autor():
    print("¿Quién está probando?")
    print("1. Joshua")
    print("2. Emily")
    print("3. Raul")
    author_choice = input("Ingresa el número: ")
    authors = {"1": "Joshua", "2": "Emily", "3": "Raul"}
    return authors.get(author_choice, "general")

alg_choice = elegir_algoritmo()
author = elegir_autor()

try:
    with open(f"algoritmo-{alg_choice}.ts", "r") as file_test:
        data = file_test.read()
except FileNotFoundError:
    print(f"El archivo algoritmo-{alg_choice}.ts no se encuentra en el directorio.")
    exit()

parser = yacc.yacc(start='program')

date = time.strftime("%Y-%m-%d")
hour = time.strftime("%Hh%Mm%Ss")
log_path = f"./logs/sintactico-{author}-{date}-{hour}.txt"

if not os.path.exists("./logs"):
    os.makedirs("./logs")

with open(log_path, 'w') as f:
    logfile = f
    result = parser.parse(data)