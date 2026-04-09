import sys
import ply.lex as lex

# Lista de tokens
tokens = [

    # Palabras reservadas
    'PROGRAM',
    'VAR',
    'BEGIN',
    'END',
    'INTEGER',
    'REAL',
    'STRINGTYPE',
    'CHAR',
    'ARRAY',
    'OF',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'DO',
    'NOT',

    # Otros
    'ID',
    'STRING',
    'NUMBER',

    # Operadores
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'ASSIGN',

    # Comparadores
    'EQUAL',
    'LT',
    'GT',

    # Símbolos
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',

    'SEMI',
    'COLON',
    'COMMA',
    'DOT',
    'RANGE'
]

# Operadores
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_ASSIGN = r':='

t_EQUAL = r'='
t_LT = r'<'
t_GT = r'>'

# Símbolos
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_SEMI = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'

t_RANGE = r'\.\.'

# Ignorar espacios
t_ignore = ' \t'


# Palabras reservadas
def t_PROGRAM(t):
    r'program'
    return t

def t_VAR(t):
    r'var'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_INTEGER(t):
    r'integer'
    return t

def t_REAL(t):
    r'real'
    return t

def t_STRINGTYPE(t):
    r'string'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
    return t

def t_NOT(t):
    r'not'
    return t


# Números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Strings
def t_STRING(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t


# Identificadores
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t


# Saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
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
		fin = 'pascal.txt'
	f = open(fin, 'r')
	data = f.read()
	print (data)
	lexer.input(data)
	test(data, lexer)
	#input()
