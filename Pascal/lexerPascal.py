import ply.lex as lex

tokens = (

    # --- Palabras Reservadas ---
    'PROGRAM', 'VAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE', 
    'WHILE', 'DO', 'INTEGER', 'REAL', 'BOOLEAN', 'READ', 'WRITE', 
    'STRING', 'WRITELN', 'ARRAY', 'OF', 'NEW', 'NOT',

    # --- Operadores Matemáticos y Lógicos ---
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',        
    'ASSIGN', 'EQUAL', 'NOTEQ',                
    'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 
    
    # --- Símbolos de Puntuación y Agrupación ---
    'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'DOTDOT',      
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',                        
    
    'ID',       
    'NUMBER',
    'STRLIT',
)

reservadas = {
    'program': 'PROGRAM', 'var': 'VAR', 'begin': 'BEGIN', 'end': 'END',
    'if': 'IF', 'then': 'THEN', 'else': 'ELSE', 'while': 'WHILE', 'do': 'DO',
    'integer': 'INTEGER', 'real': 'REAL', 'boolean': 'BOOLEAN', 'string': 'STRING',
    'read': 'READ', 'write': 'WRITE', 'writeln': 'WRITELN',
    'array': 'ARRAY', 'of': 'OF', 'new': 'NEW', 'not': 'NOT'
}

# Tokens Estaticos

t_PLUS         = r'\+'
t_MINUS        = r'-'
t_TIMES        = r'\*'
t_DIVIDE       = r'/'
t_ASSIGN       = r':='
t_EQUAL        = r'='
t_NOTEQ        = r'<>'
t_LESS         = r'<'
t_LESSEQUAL    = r'<='
t_GREATER      = r'>'
t_GREATEREQUAL = r'>='
t_SEMICOLON    = r';'
t_COLON        = r':'
t_COMMA        = r','
t_DOTDOT       = r'\.\.'
t_DOT          = r'\.'
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'

# Tokens Dinámicos

def t_ID_INVALID_NUMBER(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    print(f"Error léxico: identificador inválido '{t.value}' (no puede empezar con número)")
    t.lexer.skip(len(t.value))

def t_ID_INVALID_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*[#@!$%&]+[a-zA-Z0-9_#@!$%&]*'
    print(f"Error léxico: identificador inválido '{t.value}' (carácter no permitido)")
    t.lexer.skip(1)

def t_ID_INVALID_CONSECUTIVE(t):
    r'(?!(program|var|begin|end|if|then|else|while|do|integer|real|boolean|read|write)\b)[a-zA-Z_][a-zA-Z0-9_]*[ \t]+(?!(program|var|begin|end|if|then|else|while|do|integer|real|boolean|read|write)\b)(?![#@!$%&])[a-zA-Z_][a-zA-Z0-9_]*(?=[ \t]*:(?!=))'
    print(f"Error léxico: declaración inválida en línea {t.lexer.lineno}: '{t.value.strip()}' "
          f"(múltiples identificadores sin coma separadora)")
    t.lexer.lineno += t.value.count('\n')

def t_COMMENT_UNCLOSED(t):
    r'\{[^}]*$'
    print(f"Error léxico: comentario no cerrado en línea {t.lexer.lineno}: '{t.value[:20]}...' (falta '}}')")
    t.lexer.skip(len(t.value))

def t_COMMENT(t):
    r'\{[^}]*\}'
    t.lexer.lineno += t.value.count('\n')

def t_STRING_UNCLOSED(t):
    r'\'[^\'\n]*$'
    print(f"Error léxico: string no cerrado en línea {t.lexer.lineno}: '{t.value[:20]}' (falta comilla de cierre)")
    t.lexer.skip(len(t.value))

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t

def t_NUMBER_MALFORMED(t):
    r'\d+\.(?![\d.])'
    print(f"Error léxico: número mal formado '{t.value}' en línea {t.lexer.lineno} (falta parte decimal)")
    t.lexer.skip(len(t.value))

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_STRLIT(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]
    t.type = 'STRLIT'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error Léxico: Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

with open('Pascal\\pascal.txt', 'r') as file:
        data = file.read()
        
print("----- Código Fuente Leído -----")
print(data)

print("\n----- Tokens Generados -----")

lexer.input(data)

while True:
    token = lexer.token()
    if not token:
        break     
    print(token)
