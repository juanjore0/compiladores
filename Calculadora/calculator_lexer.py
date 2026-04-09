import ply.lex as lex
import sys

hubo_error_lexico = False

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    global hubo_error_lexico
    hubo_error_lexico = True
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

def test(data, lexer):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fin = sys.argv[1]
    else:
        fin = 'Calculadora\\evaluacion.txt'

    with open(fin, 'r') as f:
        data = f.read()

    print("Contenido del archivo:")
    print(data)
    print("\nTokens encontrados:")
    
    test(data, lexer)