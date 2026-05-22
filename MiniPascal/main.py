import lexerPascal
import parserPascal
from semanticPascal import AnalizadorSemantico

def inicializar_compilador(ruta_codigo_fuente):
    print("\n" + "=" * 75)
    print("  SISTEMA DE COMPILACIÓN MINI PASCAL — REGISTRO DE EJECUCIÓN")
    print("=" * 75)

    try:
        with open(ruta_codigo_fuente, 'r', encoding='utf-8') as f:
            codigo_fuente = f.read().strip()
    except FileNotFoundError:
        print(f"[ERROR] El archivo '{ruta_codigo_fuente}' no existe.")
        return

    # ── FASE 1/2: Léxico + Sintáctico ────────────────────────────────────
    print("\n[FASE 1/2] Evaluación léxico-sintáctica...")
    parserPascal.estado_analisis['hubo_error'] = False
    parserPascal.estado_analisis['registro_errores'].clear()

    analizador_lexico    = lexerPascal.lexer
    analizador_lexico.lineno = 1          # reiniciar contador de líneas
    analizador_sintactico = parserPascal.parser

    arbol = analizador_sintactico.parse(
        codigo_fuente, tracking=True, lexer=analizador_lexico
    )

    if parserPascal.estado_analisis['hubo_error'] or arbol is None:
        print("\n[FALLO SINTÁCTICO] Anomalías detectadas:")
        for i, err in enumerate(parserPascal.estado_analisis['registro_errores'], 1):
            print(f"  {i}. {err}")
        return

    print("[ÉXITO SINTÁCTICO] AST generado correctamente.")

    # ── FASE 2/2: Semántico ───────────────────────────────────────────────
    print("\n[FASE 2/2] Validación semántica...")
    motor = AnalizadorSemantico(modo_traza=True)
    errores = motor.analizar(arbol)

    # Imprimir tabla global + historiales locales
    motor.imprimir_resumen()

    if errores:
        print(f"\n[FALLO SEMÁNTICO] Conflictos detectados:")
        for i, err in enumerate(errores, 1):
            print(f"  {i}. {err}")
    else:
        print("\n[ÉXITO SEMÁNTICO] Tipos y alcances verificados correctamente.")

    print("=" * 75 + "\n")


inicializar_compilador('MiniPascal\\pascal.txt')