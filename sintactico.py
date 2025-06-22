import ply.yacc as yacc
from lexicon import tokens

def p_assignment(p):
    '''assignment : LET IDENTIFIER EQUALS value SEMICOLON 
                    | LET IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | LET IDENTIFIER COLON data_type SEMICOLON
                    | CONST IDENTIFIER EQUALS VALUE SEMICOLON
                    | CONST IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | VAR IDENTIFIER EQUALS value SEMICOLON
                    | VAR IDENTIFIER COLON data_type EQUALS value SEMICOLON
                    | VAR IDENTIFIER COLON data_type SEMICOLON'''
    
def p_statement(p): 
    '''statement : assignment
                    | expression SEMICOLON
                    | if_statement'''
    
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
    
def p_error(p):
    print("Syntax error in input!")