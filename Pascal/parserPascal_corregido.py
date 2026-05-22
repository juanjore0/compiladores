import ply.yacc as yacc
import ply.lex as lex
import lexerPascal
from lexerPascal import tokens
import sys
import os

hubo_error = False
errores_encontrados = []  # Lista para acumular TODOS los errores

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# --- PROGRAMA ---
def p_program(p):
    '''program : PROGRAM ID SEMICOLON uses_section var_section BEGIN statements END DOT'''
    pass

# Recuperación: program sin punto final
def p_program_no_dot(p):
    '''program : PROGRAM ID SEMICOLON uses_section var_section BEGIN statements END'''
    registrar_error(f"Línea {p.lineno(8)}: Se esperaba '.' al final del programa después de 'end'")

# Recuperación: program sin punto y coma después del nombre
def p_program_no_semi(p):
    '''program : PROGRAM ID uses_section var_section BEGIN statements END DOT'''
    registrar_error(f"Línea {p.lineno(2)}: Se esperaba ';' después del nombre del programa '{p[2]}'")

# Recuperación: program sin punto y sin punto y coma
def p_program_no_semi_no_dot(p):
    '''program : PROGRAM ID uses_section var_section BEGIN statements END'''
    registrar_error(f"Línea {p.lineno(2)}: Faltan ';' después del nombre '{p[2]}' y '.' al final del programa")

# --- SECCIÓN USES ---
def p_uses_section(p):
    '''uses_section : USES uses_list SEMICOLON
                    | empty'''
    pass

# Recuperación: uses sin punto y coma al final
def p_uses_section_no_semi(p):
    '''uses_section : USES uses_list error'''
    registrar_error(f"Línea {p.lineno(1)}: Falta ';' al final de la cláusula 'uses'")

def p_uses_list(p):
    '''uses_list : uses_list COMMA ID
                 | ID'''
    pass

# --- SECCIÓN DE VARIABLES ---
def p_var_section(p):
    '''var_section : VAR var_declarations
                   | empty'''
    pass

def p_var_declarations(p):
    '''var_declarations : var_declarations var_decl
                        | var_decl'''
    pass

def p_var_decl(p):
    '''var_decl : id_list COLON type SEMICOLON'''
    pass

# Recuperación: declaración de variable sin dos puntos (ej: name string;)
def p_var_decl_no_colon(p):
    '''var_decl : id_list type SEMICOLON'''
    registrar_error(f"Línea {p.lineno(1)}: Falta ':' en declaración de variable (se esperaba 'identificador : tipo ;')")

# Recuperación: declaración de variable sin punto y coma
def p_var_decl_no_semi(p):
    '''var_decl : id_list COLON type error'''
    registrar_error(f"Línea {p.lineno(3)}: Falta ';' al final de la declaración de variable")

# Recuperación genérica de error en declaración de variable
def p_var_decl_error(p):
    '''var_decl : error SEMICOLON'''
    pass  # El error ya fue registrado en p_error

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    pass

def p_type(p):
    '''type : INTEGER
            | REAL
            | BOOLEAN
            | STRING
            | ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF type'''
    pass

# --- SENTENCIAS ---
def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statements SEMICOLON
                  | statement
                  | empty'''
    pass

# Recuperación: sentencias sin punto y coma entre ellas
def p_statements_no_semi(p):
    '''statements : statements statement'''
    registrar_error(f"Línea {p.lineno(2)}: Falta ';' entre sentencias")

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | read_statement
                 | write_statement
                 | writeln_statement'''
    pass

# Recuperación genérica de error en sentencia
def p_statement_error(p):
    '''statement : error'''
    pass  # El error ya fue registrado en p_error

# --- ASIGNACIÓN ---
def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    pass

# Recuperación: asignación sin expresión
def p_assignment_error(p):
    '''assignment : ID ASSIGN error'''
    registrar_error(f"Línea {p.lineno(1)}: Expresión inválida en asignación a '{p[1]}'")

# --- IF ---
def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    pass

# --- WHILE ---
def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    pass

# --- READ ---
def p_read_statement(p):
    '''read_statement : READ LPAREN id_list RPAREN'''
    pass

# --- WRITE ---
def p_write_statement(p):
    '''write_statement : WRITE LPAREN expr_list RPAREN'''
    pass

# --- WRITELN ---
def p_writeln_statement(p):
    '''writeln_statement : WRITELN LPAREN expr_list RPAREN
                         | WRITELN LPAREN RPAREN'''
    pass

# Recuperación: writeln sin paréntesis de cierre
def p_writeln_no_rparen(p):
    '''writeln_statement : WRITELN LPAREN expr_list error'''
    registrar_error(f"Línea {p.lineno(1)}: Falta ')' al cerrar writeln")

def p_expr_list(p):
    '''expr_list : expr_list COMMA expression
                 | expression'''
    pass

# --- EXPRESIONES ---
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    pass

def p_expression_comparison(p):
    '''expression : expression EQUAL expression
                  | expression NOTEQ expression
                  | expression LESS expression
                  | expression LESSEQUAL expression
                  | expression GREATER expression
                  | expression GREATEREQUAL expression'''
    pass

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    pass

def p_expression_not(p):
    '''expression : NOT expression'''
    pass

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    pass

def p_expression_id(p):
    '''expression : ID'''
    pass

def p_expression_number(p):
    '''expression : NUMBER'''
    pass

def p_expression_string(p):
    '''expression : STRLIT
                  | NEW LPAREN ID RPAREN'''
    pass

# --- REGLA VACÍA ---
def p_empty(p):
    '''empty :'''
    pass

# --- FUNCIÓN AUXILIAR PARA REGISTRAR ERRORES ---
def registrar_error(mensaje):
    global hubo_error
    hubo_error = True
    if mensaje not in errores_encontrados:
        errores_encontrados.append(mensaje)

# --- MANEJO DE ERRORES SINTÁCTICOS ---
def p_error(p):
    global hubo_error
    hubo_error = True

    if p is not None:
        token_type = p.type if hasattr(p, 'type') else 'DESCONOCIDO'
        token_value = p.value if hasattr(p, 'value') else ''

        # Mensajes descriptivos según el tipo de token erróneo
        if token_type == 'ID':
            msg = (f"Línea {p.lineno}: Identificador inesperado '{token_value}'. "
                   f"Puede faltar ';', ':' u otro separador antes de este token")
        elif token_type == 'SEMICOLON':
            msg = f"Línea {p.lineno}: ';' inesperado — verifique la estructura de la sentencia"
        elif token_type == 'COLON':
            msg = f"Línea {p.lineno}: ':' inesperado en declaración de variable"
        elif token_type == 'DOT':
            msg = f"Línea {p.lineno}: '.' inesperado — verifique el final del programa"
        elif token_type == 'BEGIN':
            msg = f"Línea {p.lineno}: 'begin' inesperado — puede faltar ';' antes de 'begin'"
        elif token_type == 'VAR':
            msg = (f"Línea {p.lineno}: 'var' inesperado — puede faltar ';' "
                   f"después del nombre del programa")
        else:
            msg = (f"Línea {p.lineno}: Token inesperado '{token_value}' "
                   f"(tipo: {token_type})")

        registrar_error(msg)

        # CLAVE: errok() le dice al parser que continúe buscando más errores
        parser.errok()
    else:
        registrar_error("Fin de archivo inesperado — programa incompleto")


if __name__ == '__main__':

    parser = yacc.yacc()

    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'Pascal\\Pascal\\pascal.txt'

    try:
        with open(fin, 'r') as f:
            data = f.read().strip()

        print("=" * 70)
        print("ANÁLISIS DE PROGRAMA PASCAL (Léxico y Sintáctico)")
        print("=" * 70)
        print()

        # Crear lexer limpio
        new_lexer = lex.lex(module=lexerPascal)

        hubo_error = False
        errores_encontrados.clear()

        parser.parse(data, tracking=True, lexer=new_lexer)

        print()
        print("=" * 70)
        if not hubo_error:
            print("✓ ANÁLISIS COMPLETADO: Programa válido (sin errores)")
        else:
            print(f"✗ ANÁLISIS COMPLETADO: Se encontraron {len(errores_encontrados)} error(es)\n")
            for i, err in enumerate(errores_encontrados, 1):
                print(f"  [{i}] {err}")
        print("=" * 70)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{fin}'")