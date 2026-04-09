import ply.yacc as yacc
import calculator_lexer
from calculator_lexer import tokens
import sys

hubo_error = False

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'), 
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    pass

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    pass

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    pass

def p_expression_number(p):
    'expression : NUMBER'
    pass

def p_error(p):
    global hubo_error
    hubo_error = True  
    if p is not None:
        print(f"ERROR SINTÁCTICO: No se esperaba el token '{p.value}' en la línea {p.lineno}")
    else:
        print("ERROR SINTÁCTICO: Expresión incompleta al final del archivo")

parser = yacc.yacc()

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'evaluacion.txt'

    try:
        with open(fin, 'r') as f:
            data = f.read().strip()
        
        print(f"Analizando la estructura de:\n{data}\n")
        print("--- RESULTADO ---")
        
        hubo_error = False
        calculator_lexer.hubo_error_lexico = False 
        
        parser.parse(data, tracking=True)
        
        if not hubo_error and not calculator_lexer.hubo_error_lexico:
            print("Tu parser reconoció correctamente todo")
        else:
            print("Se encontraron errores léxicos o sintácticos. Corrige la expresión y vuelve a intentarlo.")
            
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{fin}'")