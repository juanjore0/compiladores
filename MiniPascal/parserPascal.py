import ply.yacc as yacc
from lexerPascal import tokens
from semanticPascal import (
    NodoPrograma, NodoDeclaracionVariable, NodoAsignacion,
    NodoOperacionBinaria, NodoOperacionUnaria, NodoVariable, NodoLiteral,
    NodoCondicionalIf, NodoBucleWhile, NodoLectura, NodoEscritura,
    NodoProcedimiento, NodoFuncion, NodoLlamadaSubprograma,
)

estado_analisis = {'hubo_error': False, 'registro_errores': []}

precedence = (
    ('left',  'PLUS', 'MINUS'),
    ('left',  'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

# ── Programa principal ────────────────────────────────────────────────────────

def p_program(p):
    '''program : PROGRAM ID SEMICOLON uses_section var_section subprogram_section BEGIN statements END DOT'''
    p[0] = NodoPrograma(p[2], p[5], p[6], p[8], p.lineno(1))

# ── Sección uses ──────────────────────────────────────────────────────────────

def p_uses_section(p):
    '''uses_section : USES uses_list SEMICOLON
                    | empty'''
    pass

def p_uses_list(p):
    '''uses_list : uses_list COMMA ID
                 | ID'''
    pass

# ── Variables globales ────────────────────────────────────────────────────────

def p_var_section(p):
    '''var_section : VAR var_declarations
                   | empty'''
    p[0] = p[2] if len(p) == 3 else []

def p_var_declarations(p):
    '''var_declarations : var_declarations var_decl
                        | var_decl'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_var_decl(p):
    '''var_decl : id_list COLON type SEMICOLON'''
    p[0] = NodoDeclaracionVariable(p[1], p[3], p.lineno(2))

def p_id_list(p):
    '''id_list : id_list COMMA ID
               | ID'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_type(p):
    '''type : INTEGER
            | REAL
            | BOOLEAN
            | STRING
            | ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF type'''
    p[0] = p[1] if len(p) == 2 else ['ARRAY', p[3], p[5], p[8]]

# ── Sección de subprogramas (procedures + functions) ─────────────────────────

def p_subprogram_section(p):
    '''subprogram_section : subprogram_list
                          | empty'''
    p[0] = p[1] if p[1] else []

def p_subprogram_list(p):
    '''subprogram_list : subprogram_list subprogram_decl
                       | subprogram_decl'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_subprogram_decl(p):
    '''subprogram_decl : procedure_decl
                       | function_decl'''
    p[0] = p[1]

# procedure NombreProc ; [var …] begin … end ;
def p_procedure_decl(p):
    '''procedure_decl : PROCEDURE ID SEMICOLON var_section BEGIN statements END SEMICOLON'''
    p[0] = NodoProcedimiento(p[2], p[4], p[6], p.lineno(1))

# function NombreFunc : TipoRetorno ; [var …] begin … end ;
def p_function_decl(p):
    '''function_decl : FUNCTION ID COLON type SEMICOLON var_section BEGIN statements END SEMICOLON'''
    p[0] = NodoFuncion(p[2], p[4], p[6], p[8], p.lineno(1))

# ── Sentencias ────────────────────────────────────────────────────────────────

def p_statements(p):
    '''statements : statements SEMICOLON statement
                  | statement'''
    if len(p) == 4:
        lista = p[1] if p[1] is not None else []
        if p[3] is not None:
            lista.append(p[3])
        p[0] = lista
    else:
        p[0] = [p[1]] if p[1] is not None else []

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | read_statement
                 | write_statement
                 | writeln_statement
                 | call_statement
                 | compound_statement
                 | empty'''
    p[0] = p[1]

def p_compound_statement(p):
    '''compound_statement : BEGIN statements END'''
    p[0] = p[2]
    
def p_call_statement(p):
    '''call_statement : ID'''
    p[0] = NodoLlamadaSubprograma(p[1], p.lineno(1))

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    p[0] = NodoAsignacion(p[1], p[3], p.lineno(1))

def p_if_statement(p):
    '''if_statement : IF expression THEN statement
                    | IF expression THEN statement ELSE statement'''
    if len(p) == 5:
        p[0] = NodoCondicionalIf(p[2], p[4], None, p.lineno(1))
    else:
        p[0] = NodoCondicionalIf(p[2], p[4], p[6], p.lineno(1))

def p_while_statement(p):
    '''while_statement : WHILE expression DO statement'''
    p[0] = NodoBucleWhile(p[2], p[4], p.lineno(1))

def p_read_statement(p):
    '''read_statement : READ LPAREN id_list RPAREN'''
    p[0] = NodoLectura(p[3], p.lineno(1))

def p_write_statement(p):
    '''write_statement : WRITE LPAREN expr_list RPAREN'''
    p[0] = NodoEscritura(p[3], False, p.lineno(1))

def p_writeln_statement(p):
    '''writeln_statement : WRITELN LPAREN expr_list RPAREN
                         | WRITELN LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = NodoEscritura(p[3], True, p.lineno(1))
    else:
        p[0] = NodoEscritura([], True, p.lineno(1))

def p_expr_list(p):
    '''expr_list : expr_list COMMA expression
                 | expression'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

# ── Expresiones ───────────────────────────────────────────────────────────────

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = NodoOperacionBinaria(p[1], p[2], p[3], p.lineno(2))

def p_expression_comparison(p):
    '''expression : expression EQUAL expression
                  | expression NOTEQ expression
                  | expression LESS expression
                  | expression LESSEQUAL expression
                  | expression GREATER expression
                  | expression GREATEREQUAL expression'''
    p[0] = NodoOperacionBinaria(p[1], p[2], p[3], p.lineno(2))

def p_expression_uminus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = NodoOperacionUnaria(p[1], p[2], p.lineno(1))

def p_expression_not(p):
    '''expression : NOT expression'''
    p[0] = NodoOperacionUnaria(p[1], p[2], p.lineno(1))

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_id(p):
    '''expression : ID'''
    p[0] = NodoVariable(p[1], p.lineno(1))

def p_expression_number(p):
    '''expression : NUMBER'''
    tipo = 'REAL' if '.' in str(p[1]) else 'INTEGER'
    p[0] = NodoLiteral(p[1], tipo, p.lineno(1))

def p_expression_string(p):
    '''expression : STRLIT
                  | NEW LPAREN ID RPAREN'''
    if len(p) == 2:
        p[0] = NodoLiteral(p[1], 'STRING', p.lineno(1))
    else:
        p[0] = NodoLiteral('NEW', 'OBJECT', p.lineno(1))

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    valor = True if str(p[1]).lower() == 'true' else False
    p[0] = NodoLiteral(valor, 'BOOLEAN', p.lineno(1))

def p_empty(p):
    '''empty :'''
    pass

# ── Manejo de errores ─────────────────────────────────────────────────────────

def registrar_error_sintactico(msg):
    estado_analisis['hubo_error'] = True
    if msg not in estado_analisis['registro_errores']:
        estado_analisis['registro_errores'].append(msg)

def p_error(p):
    if p:
        mensaje = f"Error sintáctico en la línea {p.lineno}: Token inesperado '{p.value}'"
        estado_analisis['hubo_error'] = True
        estado_analisis['registro_errores'].append(mensaje)
        
        while True:
            tok = parser.token() 
            if not tok or tok.type == 'SEMICOLON' or tok.type == 'END':
                break
        if tok:
            parser.errok() 
            return tok
    else:
        estado_analisis['hubo_error'] = True
        estado_analisis['registro_errores'].append("Error sintáctico: Fin de archivo inesperado.")

parser = yacc.yacc()