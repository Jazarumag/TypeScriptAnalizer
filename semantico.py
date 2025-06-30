import re
import os
import time

def verificar_variables_declaradas(data, log):
    declaradas = set()
    errores = []

    for i, linea in enumerate(data.splitlines(), 1):
        match_decl = re.match(r'\s*(let|const|var)\s+(\w+)', linea)
        if match_decl:
            declaradas.add(match_decl.group(2))
            continue

        palabras = re.findall(r'\b[a-zA-Z_]\w*\b', linea)
        for palabra in palabras:
            if palabra not in declaradas and palabra not in ['let', 'const', 'var', 'function', 'return', 'console',
                                                             'log', 'string', 'number', 'boolean', 'void', 'input',
                                                             'print']:
                if '=' in linea and palabra in linea.split('=')[0]:
                    errores.append(f"Línea {i}: La variable '{palabra}' se usa sin haber sido declarada")

    for e in errores:
        log.write("ERROR: " + e + "\n")
        print("ERROR: " + e)

def verificar_tipo_retorno_funcion(data, log):
    funciones = re.finditer(r'function\s+(\w+)\s*\([^)]*\)\s*:\s*(\w+)\s*\{([\s\S]*?)\}', data)

    for match in funciones:
        nombre = match.group(1)
        tipo = match.group(2)
        cuerpo = match.group(3)

        if tipo != "void" and "return" not in cuerpo:
            mensaje = f"Función '{nombre}' declara tipo '{tipo}' pero no tiene return"
            log.write("ERROR: " + mensaje + "\n")
            print("ERROR: " + mensaje)

def verificar_redeclaracion_variables(data, log):
    declaradas = set()
    for i, linea in enumerate(data.splitlines(), 1):
        match_decl = re.match(r'\s*(let|const|var)\s+(\w+)', linea)
        if match_decl:
            nombre = match_decl.group(2)
            if nombre in declaradas:
                log.write(f"ERROR: Línea {i}: La variable '{nombre}' está redeclarada en el mismo ámbito\n")
                print(f"ERROR: Línea {i}: La variable '{nombre}' está redeclarada en el mismo ámbito")
            else:
                declaradas.add(nombre)


def verificar_parametros_funcion_tipados(data, log):
    funciones = re.finditer(r'function\s+(\w+)\s*\(([^)]*)\)', data)
    for match in funciones:
        nombre = match.group(1)
        params = match.group(2)
        for param in params.split(','):
            param = param.strip()
            if param and ':' not in param:
                log.write(f"ERROR: Función '{nombre}' tiene parámetro sin tipo declarado: '{param}'\n")
                print(f"ERROR: Función '{nombre}' tiene parámetro sin tipo declarado: '{param}'")


def verificar_variables_inicializadas(data, log):
    declaradas = set()
    inicializadas = set()
    for i, linea in enumerate(data.splitlines(), 1):
        match_decl = re.match(r'\s*(let|const|var)\s+(\w+)', linea)
        if match_decl:
            declaradas.add(match_decl.group(2))
            if '=' in linea:
                inicializadas.add(match_decl.group(2))
            continue
        palabras = re.findall(r'\b[a-zA-Z_]\w*\b', linea)
        for palabra in palabras:
            if palabra in declaradas and palabra not in inicializadas:
                if '=' not in linea or palabra not in linea.split('=')[0]:
                    log.write(f"ERROR: Línea {i}: La variable '{palabra}' se usa sin haber sido inicializada\n")
                    print(f"ERROR: Línea {i}: La variable '{palabra}' se usa sin haber sido inicializada")

def verificar_numero_argumentos_funcion(data, log):
    firmas_funciones = {}
    declaraciones = re.finditer(r'function\s+(\w+)\s*\(([^)]*)\)', data)
    for match in declaraciones:
        nombre_funcion = match.group(1)
        parametros_str = match.group(2).strip()
        num_parametros = len(parametros_str.split(',')) if parametros_str else 0
        firmas_funciones[nombre_funcion] = num_parametros

    lineas = data.splitlines()
    for i, linea in enumerate(lineas, 1):
        llamadas = re.finditer(r'(\w+)\s*\(([^)]*)\)', linea)
        for match_llamada in llamadas:
            nombre_llamada = match_llamada.group(1)
            if nombre_llamada in firmas_funciones:
                argumentos_str = match_llamada.group(2).strip()
                num_argumentos = len(argumentos_str.split(',')) if argumentos_str else 0
                num_parametros_esperados = firmas_funciones[nombre_llamada]
                if num_argumentos != num_parametros_esperados:
                    log.write(f"ERROR: Línea {i}: Llamada a la función '{nombre_llamada}' con {num_argumentos} argumento(s), pero se esperaban {num_parametros_esperados}\n")
                    print(f"ERROR: Línea {i}: Llamada a la función '{nombre_llamada}' con {num_argumentos} argumento(s), pero se esperaban {num_parametros_esperados}")

def verificar_division_por_cero(data, log):
    lineas = data.splitlines()
    for i, linea in enumerate(lineas, 1):
        if re.search(r'/\s*0(\.0+)?\b', linea):
            log.write(f"ERROR: Línea {i}: Se encontró una división por cero.\n")
            print(f"ERROR: Línea {i}: Se encontró una división por cero.")

def elegir_algoritmo():
    print("Selecciona el algoritmo a analizar:")
    print("1. algoritmo-1.ts")
    print("2. algoritmo-2.ts")
    print("3. algoritmo-3.ts")
    alg_choice = input("Ingresa el número: ")
    return alg_choice if alg_choice in ["1", "2", "3"] else "3"


def elegir_autor():
    print("¿Quién está probando?")
    print("1. Joshua")
    print("2. Emily")
    print("3. Raul")
    autores = {"1": "Joshua", "2": "Emily", "3": "Raul"}
    return autores.get(input("Ingresa el número: "), "general")

alg = elegir_algoritmo()
autor = elegir_autor()

try:
    with open(f"algoritmo-{alg}.ts", "r") as archivo:
        codigo = archivo.read()
except FileNotFoundError:
    print(f"No se encontró 'algoritmo-{alg}.ts'")
    exit()

fecha = time.strftime("%Y-%m-%d")
hora = time.strftime("%Hh%Mm%Ss")
ruta_log = f"./logs/semantico-{autor}-{fecha}-{hora}.txt"

if not os.path.exists("./logs"):
    os.makedirs("./logs")

with open(ruta_log, 'w') as log:
    log.write(f"Log semántico - Autor: {autor} - {fecha} {hora}\n")
    log.write("=" * 50 + "\n")
    verificar_variables_declaradas(codigo, log)
    verificar_tipo_retorno_funcion(codigo, log)
    verificar_redeclaracion_variables(codigo, log)
    verificar_parametros_funcion_tipados(codigo, log)
    verificar_variables_inicializadas(codigo, log)
    verificar_numero_argumentos_funcion(codigo, log)
    verificar_division_por_cero(codigo, log)

print(f"\nLog generado: {ruta_log}")
