import ply.lex as lex

tokens = (
    'PROGRAM', 'USES', 'VAR', 'PROCEDURE', 'FUNCTION', 'BEGIN', 'END',
    'IF', 'THEN', 'ELSE', 'WHILE', 'DO',
    'INTEGER', 'REAL', 'BOOLEAN', 'READ', 'WRITE', 'STRING', 'WRITELN',
    'ARRAY', 'OF', 'NEW', 'NOT', 'TRUE', 'FALSE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN', 'EQUAL', 'NOTEQ',
    'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL',
    'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'DOTDOT',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'ID', 'NUMBER', 'STRLIT',
)

reservadas = {
    'program'  : 'PROGRAM',
    'uses'     : 'USES',
    'var'      : 'VAR',
    'procedure': 'PROCEDURE',
    'function' : 'FUNCTION',
    'begin'    : 'BEGIN',
    'end'      : 'END',
    'if'       : 'IF',
    'then'     : 'THEN',
    'else'     : 'ELSE',
    'while'    : 'WHILE',
    'do'       : 'DO',
    'integer'  : 'INTEGER',
    'real'     : 'REAL',
    'boolean'  : 'BOOLEAN',
    'string'   : 'STRING',
    'read'     : 'READ',
    'write'    : 'WRITE',
    'writeln'  : 'WRITELN',
    'array'    : 'ARRAY',
    'of'       : 'OF',
    'new'      : 'NEW',
    'not'      : 'NOT',
    'true'     : 'TRUE',
    'false'    : 'FALSE',
}

t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_ASSIGN        = r':='
t_EQUAL         = r'='
t_NOTEQ         = r'<>'
t_LESS          = r'<'
t_LESSEQUAL     = r'<='
t_GREATER       = r'>'
t_GREATEREQUAL  = r'>='
t_SEMICOLON     = r';'
t_COLON         = r':'
t_COMMA         = r','
t_DOTDOT        = r'\.\.'
t_DOT           = r'\.'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'

def t_ID_INVALID_NUMBER(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    print(f"Error léxico: identificador inválido '{t.value}' (no puede empezar con número)")
    t.lexer.skip(len(t.value))

def t_ID_INVALID_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*[#@!$%&]+[a-zA-Z0-9_#@!$%&]*'
    print(f"Error léxico: identificador inválido '{t.value}' (carácter no permitido)")
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRLIT(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error Léxico: carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()