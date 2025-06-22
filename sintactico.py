import ply.yacc as yacc
from lexicon import tokens, lexer

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
                    | print_statement
                    | function_def
                    | return_statement'''
    
def p_statement_block(p):
    '''statement_block : LBRACE statement_list RBRACE
                            | statement'''
    
def p_statement_list(p):
    '''statement_list : statement
                        | statement statement_list'''
    
def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement_block
                        | IF LPAREN expression RPAREN statement_block ELSE statement_block'''

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN SEMICOLON'''

def p_input_expression(p):
    '''factor : INPUT LPAREN RPAREN
              | INPUT LPAREN STRING RPAREN'''

def p_expression_logic(p):
    '''expression : expression AND expression
                  | expression OR expression
                  | NOT expression'''

def p_expression_comparison(p):
    '''expression : expression EQEQ expression
                  | expression NOTEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression'''

def p_function_def(p):
    '''function_def : FUNCTION IDENTIFIER LPAREN RPAREN statement_block
                    | FUNCTION IDENTIFIER LPAREN param_list RPAREN statement_block'''

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | IDENTIFIER COMMA param_list'''

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''

def p_class_def(p):
    'class_def : CLASS IDENTIFIER LBRACE class_body RBRACE'

def p_class_body(p):
    '''class_body : class_member
                  | class_member class_body'''

def p_class_member(p):
    '''class_member : assignment
                    | function_def'''

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

def p_expression_term(p):
    'expression : term'

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
                | IDENTIFIER
                | INPUT LPAREN STRING RPAREN'''

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

def p_program(p):
    'program : statement_list'

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")
