import ply.yacc as yacc
import ply.lex as lex
import lexerPascal
from lexerPascal import tokens
import sys
import os

hubo_error = False

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# --- PROGRAMA ---
def p_program(p):
    '''program : PROGRAM ID SEMICOLON var_section BEGIN statements END DOT'''
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

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | read_statement
                 | write_statement
                 | writeln_statement'''
    pass

# --- ASIGNACIÓN ---
def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    pass

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

# --- MANEJO DE ERRORES ---
def p_error(p):
    global hubo_error
    hubo_error = True
    if p is not None:
        token_type = p.type if hasattr(p, 'type') else 'DESCONOCIDO'
        token_value = repr(p.value) if hasattr(p, 'value') else ''
        
        # Determinar el error específico según el contexto
        if token_type == 'SEMICOLON':
            print(f"ERROR SINTÁCTICO en línea {p.lineno}: Se esperaba ';' pero se encontró '{p.value}'")
        elif token_type == 'COLON':
            print(f"ERROR SINTÁCTICO en línea {p.lineno}: Se esperaba ':' en declaración de variable")
        elif token_type == 'DOT':
            print(f"ERROR SINTÁCTICO en línea {p.lineno}: Se esperaba '.' al final del programa")
        elif token_type == 'ID':
            print(f"ERROR SINTÁCTICO en línea {p.lineno}: Identificador inesperado '{p.value}'. Se esperaba ';', ':' u otro token")
        else:
            print(f"ERROR SINTÁCTICO en línea {p.lineno}: Token inesperado '{p.value}' ({token_type})")
    else:
        print("ERROR SINTÁCTICO: Programa incompleto al final del archivo")

if __name__ == '__main__':
    
    parser = yacc.yacc()
    
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'Pascal\\pascal.txt'

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
        parser.parse(data, tracking=True, lexer=new_lexer)
        
        print()
        print("=" * 70)
        if not hubo_error:
            print("✓ ANÁLISIS COMPLETADO: Programa válido (sin errores)")
        else:
            print("✗ ANÁLISIS COMPLETADO: Se encontraron errores (ver detalles arriba)")
        print("=" * 70)
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{fin}'")

