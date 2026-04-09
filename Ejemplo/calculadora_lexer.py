import ply.lex as lex
import sys

# lista de tokens para la calculadora
tokens = (   
    # Symbols
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    # Others   
    'ID', 
    'NUMERO',
)

# Regular expressions rules for a simple tokens 
t_MAS   = r'\+'
t_MENOS  = r'-'
t_POR  = r'\*'
t_DIVIDIDO = r'/'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER  = r'\)'

def t_NUMERO(t):
    r'\d+(\.\d+)?(([eE])?\d+(\.\d+)?)?'
    return t

def t_ID(t):
    r'\w+(_\d\w)*'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print ("Lexical error: " + str(t.value[0]))
    t.lexer.skip(1)
    
def test(data, lexer):
	lexer.input(data)
	while True:
		tok = lexer.token()
		if not tok:
			break
		print (tok)

lexer = lex.lex()

if __name__ == '__main__':
	if (len(sys.argv) > 1):
		fin = sys.argv[1]
	else:
		fin = 'calculadora_input.txt'
	f = open(fin, 'r')
	data = f.read()
	print (data)
	lexer.input(data)
	test(data, lexer)
	#input()

