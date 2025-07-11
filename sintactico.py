import ply.yacc as yacc
from lexicon import tokens
import time
import os

# Tabla de símbolos global
tabla_simbolos = {
    "variables": {},
    "funciones": {},
    "clases": {},
    "tipos": {
        "primitivos": ["number", "string", "boolean", "char", "any"],
        "string_methods": ["length", "toUpperCase", "toLowerCase", "charAt", "substring"],
        "number_methods": ["toString", "toFixed", "valueOf"],
        "array_methods": ["push", "pop", "length", "join", "slice"]
    },
    "ambito_actual": "global",
    "pila_ambitos": ["global"],
    "errores": []
}

# Funciones auxiliares para el análisis semántico
def error_semantico(mensaje, lineno=None):
    """Reporta un error semántico"""
    error = f"Error semántico: {mensaje}"
    if lineno:
        error += f" (línea {lineno})"
    tabla_simbolos["errores"].append(error)
    print(error)

def obtener_tipo_valor(valor, tipo_token):
    """Determina el tipo de un valor según su token"""
    if tipo_token == "NUMBER":
        return "number"
    elif tipo_token == "STRING":
        return "string"
    elif tipo_token == "CHARACTER":
        return "char"
    elif tipo_token == "TRUE" or tipo_token == "FALSE":
        return "boolean"
    return None

def verificar_variable_declarada(nombre, lineno=None):
    """Verifica si una variable ha sido declarada"""
    if nombre not in tabla_simbolos["variables"]:
        error_semantico(f"La variable '{nombre}' no ha sido declarada", lineno)
        return False
    return True

def verificar_tipos_compatibles(tipo1, tipo2, operacion="asignación"):
    """Verifica si dos tipos son compatibles para una operación"""
    if tipo1 == tipo2:
        return True
    
    if operacion == "aritmetica":
        return tipo1 == "number" and tipo2 == "number"
    elif operacion == "concatenacion":
        return tipo1 == "string" or tipo2 == "string"
    elif operacion == "comparacion":
        return tipo1 == tipo2 or (tipo1 == "number" and tipo2 == "number")
    
    return False

def obtener_tipo_operacion(tipo1, tipo2, operador):
    """Obtiene el tipo resultado de una operación"""
    if operador in ["+", "-", "*", "/", "%", "**"]:
        if tipo1 == "number" and tipo2 == "number":
            return "number"
        elif operador == "+" and (tipo1 == "string" or tipo2 == "string"):
            return "string"
    elif operador in ["==", "!=", "<", ">", "<=", ">=", "&&", "||"]:
        return "boolean"
    return None

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                        | statement statement_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_statement(p): 
    '''statement : assignment SEMICOLON
                    | expression SEMICOLON
                    | if_statement
                    | function_def
                    | return_statement
                    | class_declaration
                    | while_statement
                    | for_statement
                    | break_statement
                    | continue_statement'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : LET IDENTIFIER EQUALS value
                    | LET IDENTIFIER COLON data_type EQUALS value
                    | LET IDENTIFIER COLON data_type
                    | CONST IDENTIFIER EQUALS value
                    | CONST IDENTIFIER COLON data_type EQUALS value
                    | VAR IDENTIFIER EQUALS value
                    | VAR IDENTIFIER COLON data_type EQUALS value
                    | VAR IDENTIFIER COLON data_type
                    | IDENTIFIER EQUALS value
                    | IDENTIFIER COLON value'''
    
    nombre = p[2]
    tipo_declaracion = p[1]
    
    if len(p) == 5:  # let/const/var id = value
        tipo_valor = p[4]
        if nombre in tabla_simbolos["variables"]:
            error_semantico(f"La variable '{nombre}' ya ha sido declarada", p.lineno(2))
        else:
            tabla_simbolos["variables"][nombre] = {
                "tipo": tipo_valor,
                "declaracion": tipo_declaracion,
                "inicializada": True,
                "linea": p.lineno(2)
            }
    elif len(p) == 7:  # let/const/var id : type = value
        tipo_declarado = p[4]
        tipo_valor = p[6]
        if nombre in tabla_simbolos["variables"]:
            error_semantico(f"La variable '{nombre}' ya ha sido declarada", p.lineno(2))
        elif not verificar_tipos_compatibles(tipo_declarado, tipo_valor):
            error_semantico(f"Tipo incompatible en asignación: se esperaba '{tipo_declarado}' pero se obtuvo '{tipo_valor}'", p.lineno(2))
        else:
            tabla_simbolos["variables"][nombre] = {
                "tipo": tipo_declarado,
                "declaracion": tipo_declaracion,
                "inicializada": True,
                "linea": p.lineno(2)
            }
    elif len(p) == 4:  # id = value (reasignación)
        if not verificar_variable_declarada(nombre, p.lineno(1)):
            return
        tipo_valor = p[3]
        var_info = tabla_simbolos["variables"][nombre]
        if var_info["declaracion"] == "const":
            error_semantico(f"No se puede reasignar la constante '{nombre}'", p.lineno(1))
        elif not verificar_tipos_compatibles(var_info["tipo"], tipo_valor):
            error_semantico(f"Tipo incompatible en reasignación: se esperaba '{var_info['tipo']}' pero se obtuvo '{tipo_valor}'", p.lineno(1))
        else:
            tabla_simbolos["variables"][nombre]["inicializada"] = True
    
    p[0] = ("assignment", nombre, p[1] if len(p) > 3 else None)

def p_data_type(p):
    '''data_type : STRING_TYPE
                    | NUMBER_TYPE
                    | BOOLEAN_TYPE
                    | CHAR_TYPE
                    | array_type
                    | object_type_literal'''
    if p[1] in ["string", "number", "boolean", "char"]:
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_value(p):
    '''value : STRING
                | CHARACTER
                | NUMBER
                | TRUE
                | FALSE
                | array
                | object_literal
                | expression'''
    
    if isinstance(p[1], str) and p.slice[1].type == "STRING":
        p[0] = "string"
    elif isinstance(p[1], str) and p.slice[1].type == "CHARACTER":
        p[0] = "char"
    elif isinstance(p[1], (int, float)):
        p[0] = "number"
    elif p[1] in ["true", "false"]:
        p[0] = "boolean"
    else:
        p[0] = p[1]

# Arreglos
def p_array_type(p):
    '''array_type : NUMBER_TYPE LBRACKET RBRACKET
                    | STRING_TYPE LBRACKET RBRACKET
                    | BOOLEAN_TYPE LBRACKET RBRACKET
                    | ANY LBRACKET RBRACKET'''
    p[0] = f"{p[1]}[]"

def p_array(p):
    '''array : LBRACKET RBRACKET
                | LBRACKET element_list RBRACKET'''
    if len(p) == 3:
        p[0] = "any[]"
    else:
        # Verificar que todos los elementos sean del mismo tipo
        tipos = p[2]
        if len(set(tipos)) == 1:
            p[0] = f"{tipos[0]}[]"
        else:
            p[0] = "any[]"

def p_element_list(p):
    '''element_list : value
                | value COMMA element_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Objetos literales
def p_object_type_literal(p):
    '''object_type_literal : LBRACE property_list RBRACE
                           | LBRACE RBRACE'''
    p[0] = "object"

def p_object_literal(p):
    '''object_literal : LBRACE property_assignment_list RBRACE'''
    p[0] = "object"

def p_property(p):
    '''property : IDENTIFIER COLON data_type'''
    p[0] = (p[1], p[3])

def p_property_assignment_list(p):
    '''property_assignment_list : property_assignment
                                | property_assignment COMMA property_assignment_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_property_assignment(p):
    '''property_assignment : IDENTIFIER COLON value
                           | STRING COLON value'''
    p[0] = (p[1], p[3])

def p_property_list(p):
    '''property_list : property
                     | property SEMICOLON property_list
                     | property COMMA property_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Operaciones matemáticas con verificación de tipos
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

def p_expression_plus(p):
    'arithmetic_expression : arithmetic_expression PLUS term'
    tipo_resultado = obtener_tipo_operacion(p[1], p[3], "+")
    if tipo_resultado is None:
        error_semantico(f"Operación '+' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = tipo_resultado

def p_expression_minus(p):
    'arithmetic_expression : arithmetic_expression MINUS term'
    if p[1] != "number" or p[3] != "number":
        error_semantico(f"Operación '-' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = "number"

def p_expression_term(p):
    'arithmetic_expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    if p[1] != "number" or p[3] != "number":
        error_semantico(f"Operación '*' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = "number"

def p_term_div(p):
    'term : term DIVIDE factor'
    if p[1] != "number" or p[3] != "number":
        error_semantico(f"Operación '/' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = "number"

def p_term_module(p):
    'term : term MODULE factor'
    if p[1] != "number" or p[3] != "number":
        error_semantico(f"Operación '%' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = "number"

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_power(p):
    'factor : atom POWER factor'
    if p[1] != "number" or p[3] != "number":
        error_semantico(f"Operación '^' no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = "number"

def p_factor_atom(p):
    'factor : atom'
    p[0] = p[1]

def p_atom(p):
    '''atom : NUMBER
                | IDENTIFIER
                | LPAREN arithmetic_expression RPAREN'''
    if len(p) == 2:
        if isinstance(p[1], (int, float)):
            p[0] = "number"
        else:
            nombre = p[1]
            if not verificar_variable_declarada(nombre, p.lineno(1)):
                p[0] = "any"
            else:
                var_info = tabla_simbolos["variables"][nombre]
                if not var_info["inicializada"]:
                    error_semantico(f"La variable '{nombre}' se usa sin haber sido inicializada", p.lineno(1))
                p[0] = var_info["tipo"]
    else:
        p[0] = p[2]

# Expresiones lógicas
def p_logical_expression(p):
    '''logical_expression : logical_expression AND logical_term
                          | logical_expression OR logical_term
                          | logical_term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "boolean"

def p_logical_term(p):
    '''logical_term : NOT logical_factor
                    | logical_factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "boolean"

def p_logical_factor(p):
    '''logical_factor : comparison_expression
                      | TRUE
                      | FALSE
                      | LPAREN logical_expression RPAREN'''
    if len(p) == 2:
        if p[1] in ["true", "false"]:
            p[0] = "boolean"
        else:
            p[0] = p[1]
    else:
        p[0] = p[2]

def p_comparison_expression(p):
    '''comparison_expression : arithmetic_expression EQEQ arithmetic_expression
                             | arithmetic_expression NOTEQ arithmetic_expression
                             | arithmetic_expression GT arithmetic_expression
                             | arithmetic_expression LT arithmetic_expression
                             | arithmetic_expression GE arithmetic_expression
                             | arithmetic_expression LE arithmetic_expression'''
    if not verificar_tipos_compatibles(p[1], p[3], "comparacion"):
        error_semantico(f"Comparación no válida entre tipos '{p[1]}' y '{p[3]}'", p.lineno(2))
    p[0] = "boolean"

def p_expression(p):
    '''expression : arithmetic_expression
                  | logical_expression
                  | member_access
                  | function_call
                  | class_instantiation
                  | this_access'''
    p[0] = p[1]

def p_member_access(p):
    '''member_access : member_access DOT IDENTIFIER
                    | IDENTIFIER DOT IDENTIFIER'''
    if len(p) == 4:
        objeto = p[1]
        propiedad = p[3]
        
        if isinstance(objeto, str) and objeto in tabla_simbolos["variables"]:
            tipo_objeto = tabla_simbolos["variables"][objeto]["tipo"]
            if tipo_objeto == "string" and propiedad in tabla_simbolos["tipos"]["string_methods"]:
                p[0] = "string" if propiedad != "length" else "number"
            elif tipo_objeto == "number" and propiedad in tabla_simbolos["tipos"]["number_methods"]:
                p[0] = "string" if propiedad == "toString" else "number"
            else:
                error_semantico(f"La propiedad '{propiedad}' no existe en el tipo '{tipo_objeto}'", p.lineno(2))
                p[0] = "any"
        else:
            p[0] = "any"
    else:
        p[0] = p[1]

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN RPAREN SEMICOLON
                  | IDENTIFIER LPAREN argument_list RPAREN SEMICOLON'''
    nombre_funcion = p[1]
    if nombre_funcion not in tabla_simbolos["funciones"]:
        error_semantico(f"La función '{nombre_funcion}' no ha sido declarada", p.lineno(1))
        p[0] = "any"
    else:
        func_info = tabla_simbolos["funciones"][nombre_funcion]
        num_args = len(p[3]) if len(p) == 5 else 0
        if num_args != len(func_info["parametros"]):
            error_semantico(f"La función '{nombre_funcion}' espera {len(func_info['parametros'])} argumentos, pero se proporcionaron {num_args}", p.lineno(1))
        p[0] = func_info["tipo_retorno"]

def p_argument_list(p):
    '''argument_list : expression
                     | expression COMMA argument_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_function_def(p):
    '''function_def : FUNCTION IDENTIFIER LPAREN RPAREN statement_block
                    | FUNCTION IDENTIFIER LPAREN param_list RPAREN statement_block'''
    nombre = p[2]
    if nombre in tabla_simbolos["funciones"]:
        error_semantico(f"La función '{nombre}' ya ha sido declarada", p.lineno(2))
    else:
        parametros = p[4] if len(p) == 7 else []
        tabla_simbolos["funciones"][nombre] = {
            "parametros": parametros,
            "tipo_retorno": "void",
            "linea": p.lineno(2)
        }
    p[0] = ("function", nombre)

def p_param_list(p):
    '''param_list : IDENTIFIER
                  | IDENTIFIER COMMA param_list
                  | IDENTIFIER COLON data_type
                  | IDENTIFIER COLON data_type COMMA param_list'''
    if len(p) == 2:
        p[0] = [(p[1], "any")]
    elif len(p) == 4 and p[2] == ",":
        p[0] = [(p[1], "any")] + p[3]
    elif len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3])] + p[5]

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ("return", p[2])

def p_statement_block(p):
    '''statement_block : LBRACE statement_list RBRACE
                            | statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[2]

def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER LBRACE class_body RBRACE'''
    nombre = p[2]
    if nombre in tabla_simbolos["clases"]:
        error_semantico(f"La clase '{nombre}' ya ha sido declarada", p.lineno(2))
    else:
        tabla_simbolos["clases"][nombre] = {
            "propiedades": {},
            "metodos": {},
            "linea": p.lineno(2)
        }
    p[0] = ("class", nombre)

def p_class_instantiation(p):
    '''class_instantiation : NEW IDENTIFIER LPAREN RPAREN
                  | NEW IDENTIFIER LPAREN argument_list RPAREN'''
    nombre_clase = p[2]
    if nombre_clase not in tabla_simbolos["clases"]:
        error_semantico(f"La clase '{nombre_clase}' no ha sido declarada", p.lineno(2))
        p[0] = "any"
    else:
        p[0] = nombre_clase

def p_class_body(p):
    '''class_body : class_member_list
                  | empty'''
    p[0] = p[1] if p[1] else []

def p_class_member_list(p):
    '''class_member_list : class_member
                         | class_member class_member_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_class_member(p):
    '''class_member : class_property
                    | function_def
                    | constructor'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

def p_class_property(p):
    '''class_property : IDENTIFIER COLON data_type SEMICOLON
                      | IDENTIFIER COLON data_type EQUALS value SEMICOLON'''
    p[0] = ("property", p[1], p[3])

def p_constructor(p):
    '''constructor : CONSTRUCTOR LPAREN RPAREN statement_block
                   | CONSTRUCTOR LPAREN param_list RPAREN statement_block'''
    p[0] = ("constructor",)

def p_this_assignment(p):
    '''assignment : THIS DOT IDENTIFIER EQUALS value'''
    p[0] = ("this_assignment", p[3], p[5])

def p_this_access(p):
    '''this_access : THIS DOT IDENTIFIER
                  | THIS'''
    if len(p) == 2:
        p[0] = "this"
    else:
        p[0] = ("this_access", p[3])

def p_while_statement(p):
    '''while_statement : WHILE LPAREN logical_expression RPAREN statement_block'''
    p[0] = ("while", p[3], p[5])

def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment SEMICOLON logical_expression SEMICOLON assignment RPAREN statement_block
                        | FOR LPAREN IDENTIFIER IN expression RPAREN statement_block'''
    p[0] = ("for", p[3], p[5], p[7] if len(p) == 10 else None)

def p_if_statement(p):
    '''if_statement : IF LPAREN logical_expression RPAREN statement_block
                        | IF LPAREN logical_expression RPAREN statement_block ELSE statement_block'''
    p[0] = ("if", p[3], p[5], p[7] if len(p) == 8 else None)

def p_break_statement(p):
    '''break_statement : BREAK SEMICOLON'''
    p[0] = ("break",)

def p_continue_statement(p):
    '''continue_statement : CONTINUE SEMICOLON'''
    p[0] = ("continue",)

# Manejo de errores
parser_errors = []

def p_error(p):
    global parser_errors
    if p:
        error_msg = f"Error sintáctico en el token '{p.value}' (tipo {p.type}) en línea {p.lineno}"
    else:
        error_msg = "Error sintáctico en EOF"
    print(error_msg)
    parser_errors.append(error_msg)

def elegir_algoritmo():
    print("Selecciona el algoritmo a analizar (Sintáctico-Semántico):")
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

if __name__ == "__main__":
    alg_choice = elegir_algoritmo()
    author = elegir_autor()

    try:
        with open(f"algoritmo-{alg_choice}.ts", "r", encoding='utf-8') as file_test:
            data = file_test.read()
    except FileNotFoundError:
        print(f"El archivo algoritmo-{alg_choice}.ts no se encuentra en el directorio.")
        exit()

    # Limpiar tabla de símbolos
    tabla_simbolos["variables"].clear()
    tabla_simbolos["funciones"].clear()
    tabla_simbolos["clases"].clear()
    tabla_simbolos["errores"].clear()
    parser_errors.clear()

    parser = yacc.yacc(start='program')

    date = time.strftime("%Y-%m-%d")
    hour = time.strftime("%Hh%Mm%Ss")
    log_path = f"./logs/sintactico-semantico-{author}-{date}-{hour}.txt"

    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    with open(log_path, 'w', encoding='utf-8') as logfile:
        logfile.write(f"=== ANÁLISIS SINTÁCTICO-SEMÁNTICO ===\n")
        logfile.write(f"Autor: {author}\n")
        logfile.write(f"Archivo: algoritmo-{alg_choice}.ts\n")
        logfile.write(f"Fecha: {date} {hour}\n")
        logfile.write("=" * 50 + "\n\n")
        
        result = parser.parse(data)
        
        # Escribir resultados del análisis sintáctico
        if parser_errors:
            logfile.write("ERRORES SINTÁCTICOS:\n")
            for error in parser_errors:
                logfile.write(f"  - {error}\n")
        else:
            logfile.write(" Análisis sintáctico exitoso\n")
        
        logfile.write(f"\n")
        
        # Escribir resultados del análisis semántico
        if tabla_simbolos["errores"]:
            logfile.write("ERRORES SEMÁNTICOS:\n")
            for error in tabla_simbolos["errores"]:
                logfile.write(f"  - {error}\n")
        else:
            logfile.write(" Análisis semántico exitoso\n")
        
        logfile.write(f"\n")
        
        # Escribir tabla de símbolos
        logfile.write("TABLA DE SÍMBOLOS:\n")
        logfile.write("Variables:\n")
        for nombre, info in tabla_simbolos["variables"].items():
            logfile.write(f"  - {nombre}: {info}\n")
        
        logfile.write("Funciones:\n")
        for nombre, info in tabla_simbolos["funciones"].items():
            logfile.write(f"  - {nombre}: {info}\n")
        
        logfile.write("Clases:\n")
        for nombre, info in tabla_simbolos["clases"].items():
            logfile.write(f"  - {nombre}: {info}\n")

    print(f"Análisis completado. Log generado: {log_path}")
    print(f"Errores sintácticos: {len(parser_errors)}")
    print(f"Errores semánticos: {len(tabla_simbolos['errores'])}")