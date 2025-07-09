import ply.yacc as yacc
from lexicon import tokens
import time
import os


# Definición de la gramática
def p_program(p):
    '''program : statement_list'''
def p_statement_list(p):
    '''statement_list : statement
                        | statement statement_list'''
def p_statement(p): 
    '''statement : assignment SEMICOLON
                    | expression SEMICOLON
                    | if_statement
                    | function_def
                    | return_statement
                    | class_declaration'''

# Asignacion de variables
def p_assignment(p):
    '''assignment : LET IDENTIFIER EQUALS value
                    | LET IDENTIFIER COLON data_type EQUALS value
                    | LET IDENTIFIER COLON data_type
                    | CONST IDENTIFIER EQUALS value
                    | CONST IDENTIFIER COLON data_type EQUALS value
                    | VAR IDENTIFIER EQUALS value
                    | VAR IDENTIFIER COLON data_type EQUALS value
                    | VAR IDENTIFIER COLON data_type
                    | IDENTIFIER EQUALS value'''
def p_data_type(p):
    '''data_type : STRING_TYPE
                    | NUMBER_TYPE
                    | BOOLEAN_TYPE
                    | CHAR_TYPE
                    | array_type
                    | object_type_literal'''
def p_value(p):
    '''value : STRING
                | CHARACTER
                | array
                | object_literal
                | arithmetic_expression
                | logical_expression
                | expression'''

# Arreglos
def p_array_type(p):
    '''array_type : NUMBER_TYPE LBRACKET RBRACKET
                    | STRING_TYPE LBRACKET RBRACKET
                    | BOOLEAN_TYPE LBRACKET RBRACKET
                    | ANY LBRACKET RBRACKET'''
def p_array(p):
    '''array : LBRACKET RBRACKET
                | LBRACKET element_list RBRACKET'''
def p_element_list(p):
    '''element_list : value
                | value COMMA element_list'''

# Propiedades de objetos literales
def p_object_type_literal(p):
    '''object_type_literal : LBRACE property_list RBRACE
                           | LBRACE RBRACE'''
def p_object_literal(p):
    '''object_literal : LBRACE property_assignment_list RBRACE
                      | LBRACE RBRACE'''
# Atributos de objetos
def p_property(p):
    '''property : IDENTIFIER COLON data_type'''
def p_property_assignment_list(p):
    '''property_assignment_list : property_assignment
                                | property_assignment COMMA property_assignment_list'''
def p_property_assignment(p):
    '''property_assignment : IDENTIFIER COLON value
                           | STRING COLON value'''
def p_property_list(p):
    '''property_list : property
                     | property SEMICOLON property_list'''

# Operaciones matemáticas
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQEQ', 'NOTEQ'),
    ('left', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    ('right', 'POWER'),
    ('right', 'NOT'),
    ('left', 'DOT'),
    ('left', 'LPAREN'),
)
# nivel 1 para suma y resta  
def p_expression_plus(p):
    'arithmetic_expression : arithmetic_expression PLUS term'
def p_expression_minus(p):
    'arithmetic_expression : arithmetic_expression MINUS term'
def p_expression_term(p):
    'arithmetic_expression : term'
# nivel 2 para multiplicación, división, modulo
def p_term_times(p):
    'term : term TIMES factor'
def p_term_div(p):
    'term : term DIVIDE factor'
def p_term_module(p):
    'term : term MODULE factor'
def p_term_factor(p):
    'term : factor'
# nivel 3 para potencias
def p_factor_power(p):
    'factor : atom POWER factor'
def p_factor_atom(p):
    'factor : atom'
def p_atom(p):
    '''atom : NUMBER
                | IDENTIFIER
                | LPAREN arithmetic_expression RPAREN'''

# Lógica y comparaciones
def p_logical_expression(p):
    '''logical_expression : logical_expression AND logical_term
                          | logical_expression OR logical_term
                          | logical_term'''
def p_logical_term(p):
    '''logical_term : NOT logical_factor
                    | logical_factor'''
def p_logical_factor(p):
    '''logical_factor : comparison_expression
                      | IDENTIFIER
                      | TRUE
                      | FALSE
                      | LPAREN logical_expression RPAREN'''
def p_comparison_expression(p):
    '''comparison_expression : arithmetic_expression EQEQ arithmetic_expression
                             | arithmetic_expression NOTEQ arithmetic_expression
                             | arithmetic_expression GT arithmetic_expression
                             | arithmetic_expression LT arithmetic_expression
                             | arithmetic_expression GE arithmetic_expression
                             | arithmetic_expression LE arithmetic_expression'''
# Acceso a propiedades y llamadas a funciones
def p_member_access(p):
    '''expression : expression DOT IDENTIFIER
                    | IDENTIFIER DOT IDENTIFIER'''
def p_function_call(p):
    '''expression : IDENTIFIER LPAREN RPAREN
                  | IDENTIFIER LPAREN argument_list RPAREN'''
def p_argument_list(p):
    '''argument_list : expression
                     | expression COMMA argument_list'''

# FIN CORRECCION PARTE 1 -------------------------

# Definición de clases
def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER LBRACE class_body RBRACE'''
    pass

def p_class_body(p):
    '''class_body : class_member_list
                  | empty'''
    pass

def p_class_member_list(p):
    '''class_member_list : class_member
                         | class_member class_member_list'''
    pass

def p_class_member(p):
    '''class_member : assignment
                    | function_def
                    | property'''
    pass
    
def p_empty(p):
    'empty :'
    pass

def p_function_def(p):
    '''function_def : FUNCTION IDENTIFIER LPAREN RPAREN statement_block
                    | FUNCTION IDENTIFIER LPAREN param_list RPAREN statement_block'''

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | IDENTIFIER COMMA param_list'''

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    
def p_statement_block(p):
    '''statement_block : LBRACE statement_list RBRACE
                            | statement'''

    
def p_if_statement(p):
    '''if_statement : IF LPAREN logical_expression RPAREN statement_block
                        | IF LPAREN logical_expression RPAREN statement_block ELSE statement_block'''


# -------------------------------------- LOGS --------------------------------------

parser_errors = []
def p_error(p):
    global parser_errors
    if p:
        error_msg = f"Syntax error at token '{p.value}' (type {p.type}) on line {p.lineno}"
    else:
        error_msg ="Syntax error at EOF"
    print(error_msg)
    parser_errors.append(error_msg)

def elegir_algoritmo():
    print("Selecciona el algoritmo a analizar (Sintáctico):")
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

with open(log_path, 'w') as logfile:
    parser_errors.clear()
    result = parser.parse(data)
    if result is not None:
        logfile.write("--- Parsing Successful ---\n")
        logfile.write(str(result))
    else:
        if parser_errors:  
            for error in parser_errors:
                logfile.write(f"{error}\n")
        else:
            logfile.write("No se encontraron errores de sintaxis.\n")
print("FIN")