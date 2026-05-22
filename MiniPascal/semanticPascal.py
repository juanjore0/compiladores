# -----------------------------------------------------------------------------
# DOCUMENTACIÓN DE USO DE IA
# -----------------------------------------------------------------------------
# 
# TablaDeSimbolos.imprimir_tabla | Lógica de renderizado visual 
# y formateo de cadenas en consola para el estado de las variables globales.
#
# TablaDeSimbolos.imprimir_historial | Algoritmo de filtrado y 
# mapeo dinámico del ciclo de vida interno de las variables en scopes locales.
#
# AnalizadorSemantico.registrar_error | Estructura de persistencia 
# en colecciones (listas) para evitar la detención abrupta del compilador.
#
# AnalizadorSemantico.trazar | Mecanismo condicional de depuración 
# en tiempo de desarrollo (modo_traza) para el rastreo de ejecuciones.
#
# AnalizadorSemantico.visitar_NodoAsignacion | Regla de inferencia 
# y casting implícito que permite la promoción automática de INTEGER a REAL.
#
# AnalizadorSemantico.visitar_NodoOperacionBinaria | Lógica de 
# verificación de tipos, control de excepciones por división y propagación estática.
#
# AnalizadorSemantico.visitar_NodoOperacionUnaria | Verificación 
# semántica rigurosa de operadores prefijos (NOT y menos unario) y tipos mutados.
#
# -----------------------------------------------------------------------------

class ErrorSemantico(Exception):
    pass

class NodoAST:
    def __init__(self, linea):
        self.linea = linea
        self.tipo_evaluado = None

class NodoPrograma(NodoAST):
    def __init__(self, nombre, declaraciones_variables, subprogramas, sentencias, linea):
        super().__init__(linea)
        self.nombre = nombre
        self.declaraciones_variables = declaraciones_variables
        self.subprogramas = subprogramas
        self.sentencias = sentencias

class NodoProcedimiento(NodoAST):
    def __init__(self, nombre, declaraciones_locales, sentencias, linea):
        super().__init__(linea)
        self.nombre = nombre
        self.declaraciones_locales = declaraciones_locales
        self.sentencias = sentencias

class NodoFuncion(NodoAST):
    def __init__(self, nombre, tipo_retorno, declaraciones_locales, sentencias, linea):
        super().__init__(linea)
        self.nombre = nombre
        self.tipo_retorno = tipo_retorno
        self.declaraciones_locales = declaraciones_locales
        self.sentencias = sentencias

class NodoLlamadaSubprograma(NodoAST):
    def __init__(self, nombre, linea):
        super().__init__(linea)
        self.nombre = nombre

class NodoDeclaracionVariable(NodoAST):
    def __init__(self, nombres_variables, tipo_variable, linea):
        super().__init__(linea)
        self.nombres_variables = nombres_variables
        self.tipo_variable = tipo_variable

class NodoAsignacion(NodoAST):
    def __init__(self, nombre_variable, expresion, linea):
        super().__init__(linea)
        self.nombre_variable = nombre_variable
        self.expresion = expresion

class NodoDeclaracionConstante(NodoAST):
    def __init__(self, nombre, expresion, linea):
        super().__init__(linea)
        self.nombre = nombre
        self.expresion = expresion

class NodoOperacionBinaria(NodoAST):
    def __init__(self, operando_izquierdo, operador, operando_derecho, linea):
        super().__init__(linea)
        self.operando_izquierdo = operando_izquierdo
        self.operador = operador
        self.operando_derecho = operando_derecho

class NodoOperacionUnaria(NodoAST):
    def __init__(self, operador, expresion, linea):
        super().__init__(linea)
        self.operador = operador
        self.expresion = expresion

class NodoVariable(NodoAST):
    def __init__(self, nombre, linea):
        super().__init__(linea)
        self.nombre = nombre

class NodoLiteral(NodoAST):
    def __init__(self, valor, tipo_literal, linea):
        super().__init__(linea)
        self.valor = valor
        self.tipo_literal = tipo_literal.upper()

class NodoCondicionalIf(NodoAST):
    def __init__(self, condicion, bloque_verdadero, bloque_falso, linea):
        super().__init__(linea)
        self.condicion = condicion
        self.bloque_verdadero = bloque_verdadero
        self.bloque_falso = bloque_falso

class NodoBucleWhile(NodoAST):
    def __init__(self, condicion, cuerpo_bucle, linea):
        super().__init__(linea)
        self.condicion = condicion
        self.cuerpo_bucle = cuerpo_bucle

class NodoLectura(NodoAST):
    def __init__(self, nombres_variables, linea):
        super().__init__(linea)
        self.nombres_variables = nombres_variables

class NodoEscritura(NodoAST):
    def __init__(self, lista_expresiones, es_salto_linea, linea):
        super().__init__(linea)
        self.lista_expresiones = lista_expresiones
        self.es_salto_linea = es_salto_linea

class TablaDeSimbolos:
    def __init__(self, ambito_padre=None, nombre_ambito="Global"):
        self.simbolos      = {}   # clave → {tipo, linea, valor}
        self.historial     = {}   # clave → [ {valor, linea}, … ]
        self.ambito_padre  = ambito_padre
        self.nombre_ambito = nombre_ambito

    def registrar_variable(self, nombre, tipo_simbolo, linea, es_constante=False):
        clave = nombre.lower()
        if clave in self.simbolos:
            raise ErrorSemantico(
                f"Línea {linea}: Identificador '{nombre}' ya declarado en ámbito '{self.nombre_ambito}'."
            )
        # Añadimos 'es_constante' al diccionario interno del símbolo
        self.simbolos[clave] = {
            'tipo': tipo_simbolo.upper(), 
            'linea': linea, 
            'valor': None, 
            'es_constante': es_constante
        }
        self.historial[clave] = [{'valor': None, 'linea': linea}]

    def actualizar_valor(self, nombre, valor, linea):
        clave = nombre.lower()
        if clave in self.simbolos:
            self.simbolos[clave]['valor'] = valor
            self.historial[clave].append({'valor': valor, 'linea': linea})
            return True
        if self.ambito_padre:
            return self.ambito_padre.actualizar_valor(nombre, valor, linea)
        return False

    def buscar_variable(self, nombre):
        clave = nombre.lower()
        if clave in self.simbolos:
            return self.simbolos[clave]
        if self.ambito_padre:
            return self.ambito_padre.buscar_variable(nombre)
        return None

    # ── Tabla global: historial completo por variable ─────────────────────
    def imprimir_tabla(self, causa=""):
        etiqueta = f" — {causa}" if causa else ""
        sep = "=" * 75
        vars_datos = {k: v for k, v in self.simbolos.items()
                      if v['tipo'] not in ('PROCEDURE', 'FUNCTION')}

        print(f"\n{sep}")
        print(f"  TABLA DE SÍMBOLOS GLOBALES  |  Ámbito: {self.nombre_ambito}{etiqueta}")
        print(sep)

        if not vars_datos:
            print("  (sin variables globales declaradas)")
            print(sep)
            return

        for nombre, info in vars_datos.items():
            print(f"\n  Variable: {nombre.upper()}  (tipo {info['tipo']})")
            print(f"  {'VARIABLE':<18} | {'TIPO':<12} | {'VALOR ACTUAL':<25} | LÍNEA")
            print("  " + "-" * 71)
            for entrada in self.historial.get(nombre, []):
                val = "NULL" if entrada['valor'] is None else str(entrada['valor'])
                print(f"  {nombre:<18} | {info['tipo']:<12} | {val:<25} | {entrada['linea']}")
            print("  " + "-" * 71)

    # ── Historial por variable: una tabla independiente por cada var ──────
    def imprimir_historial(self):
        vars_datos = {k: v for k, v in self.simbolos.items()
                      if v['tipo'] not in ('PROCEDURE', 'FUNCTION')}
        if not vars_datos:
            return

        sep = "=" * 75
        print(f"\n{sep}")
        print(f"  HISTORIAL DE VARIABLES LOCALES  |  Ámbito: {self.nombre_ambito}")
        print(sep)

        for nombre, info in vars_datos.items():
            print(f"\n  Variable: {nombre.upper()}  (tipo {info['tipo']})")
            print(f"  {'VARIABLE':<18} | {'TIPO':<12} | {'VALOR ACTUAL':<25} | LÍNEA")
            print("  " + "-" * 71)
            for entrada in self.historial.get(nombre, []):
                val = "NULL" if entrada['valor'] is None else str(entrada['valor'])
                print(f"  {nombre:<18} | {info['tipo']:<12} | {val:<25} | {entrada['linea']}")
            print("  " + "-" * 71)



class AnalizadorSemantico:
    def __init__(self, modo_traza=False):
        self.tabla_global     = TablaDeSimbolos(nombre_ambito="Global")
        self.tabla_actual     = self.tabla_global
        self.registro_errores = []
        self.modo_traza       = modo_traza
        self._tablas_locales  = []   # guardamos los ámbitos locales para impresión final

    def registrar_error(self, msg):
        self.registro_errores.append(msg)

    def trazar(self, msg):
        if self.modo_traza:
            print(f"   [TRAZA] {msg}")

    def analizar(self, nodo_raiz):
        if self.modo_traza:
            print("\n" + "-"*75)
            print("   ANÁLISIS SEMÁNTICO — RASTREO DINÁMICO DE VALORES")
            print("-"*75)
        self.visitar(nodo_raiz)
        return self.registro_errores

    def imprimir_resumen(self):
        """Imprime tabla global y luego el historial de cada ámbito local."""
        self.tabla_global.imprimir_tabla(causa="Estado Final")
        for tabla in self._tablas_locales:
            tabla.imprimir_historial()

    def visitar_NodoDeclaracionConstante(self, nodo):
        res = self.visitar(nodo.expresion)
        if res is None:
            return
        val_const, tipo_const = res
        
        try:
            # Registramos en la tabla marcando es_constante=True
            self.tabla_actual.registrar_variable(nodo.nombre, tipo_const, nodo.linea, es_constante=True)
            self.tabla_actual.actualizar_valor(nodo.nombre, val_const, nodo.linea)
            self.trazar(f"Constante Declarada '{nodo.nombre}' : {tipo_const} = {val_const} (Línea {nodo.linea})")
        except ErrorSemantico as e:
            self.registrar_error(str(e))

    def visitar(self, nodo):
        if nodo is None:
            return None
        if isinstance(nodo, list):
            for elem in nodo:
                self.visitar(elem)
            return None
        metodo = getattr(self, f'visitar_{type(nodo).__name__}', self.visita_generica)
        return metodo(nodo)

    def visita_generica(self, nodo):
        pass

    def _entrar_ambito(self, nombre):
        nueva = TablaDeSimbolos(ambito_padre=self.tabla_actual, nombre_ambito=nombre)
        self.tabla_actual = nueva
        return nueva

    def _salir_ambito(self):
        tabla_local = self.tabla_actual
        self.tabla_actual = self.tabla_actual.ambito_padre
        self._tablas_locales.append(tabla_local)

    # ── visitantes ────────────────────────────────────────────────────────

    def visitar_NodoPrograma(self, nodo):
        self.trazar(f"Programa: '{nodo.nombre}'")
        if hasattr(nodo, 'declaraciones_constantes'):
            self.visitar(nodo.declaraciones_constantes)
        self.visitar(nodo.declaraciones_variables)
        self.visitar(nodo.subprogramas)
        self.visitar(nodo.sentencias)

    def visitar_NodoProcedimiento(self, nodo):
        try:
            self.tabla_actual.registrar_variable(nodo.nombre, 'PROCEDURE', nodo.linea)
        except ErrorSemantico as e:
            self.registrar_error(str(e))
        self._entrar_ambito(f"procedure {nodo.nombre}")

        if hasattr(nodo, 'declaraciones_constantes'):
            self.visitar(nodo.declaraciones_constantes)

        self.visitar(nodo.declaraciones_locales)
        self.visitar(nodo.sentencias)
        self._salir_ambito()

    def visitar_NodoFuncion(self, nodo):
        try:
            self.tabla_actual.registrar_variable(nodo.nombre, 'FUNCTION', nodo.linea)
        except ErrorSemantico as e:
            self.registrar_error(str(e))
        self._entrar_ambito(f"function {nodo.nombre}")
        # variable de retorno: misma clave que el nombre de la función
        try:
            self.tabla_actual.registrar_variable(nodo.nombre, nodo.tipo_retorno.upper(), nodo.linea)
        except ErrorSemantico:
            pass
        
        if hasattr(nodo, 'declaraciones_constantes'):
            self.visitar(nodo.declaraciones_constantes)
            
        self.visitar(nodo.declaraciones_locales)
        self.visitar(nodo.sentencias)
        self._salir_ambito()

    def visitar_NodoDeclaracionVariable(self, nodo):
        tipo = (
            f"ARRAY OF {nodo.tipo_variable[-1].upper()}"
            if isinstance(nodo.tipo_variable, list)
            else nodo.tipo_variable.upper()
        )
        for nombre in nodo.nombres_variables:
            try:
                self.tabla_actual.registrar_variable(nombre, tipo, nodo.linea)
                self.trazar(f"Declarada '{nombre}' : {tipo}  (Línea {nodo.linea})")
            except ErrorSemantico as e:
                self.registrar_error(str(e))

    def visitar_NodoAsignacion(self, nodo):
        info = self.tabla_actual.buscar_variable(nodo.nombre_variable)
        if not info:
            self.registrar_error(
                f"Línea {nodo.linea}: Variable '{nodo.nombre_variable}' no declarada."
            )
            return
        
        if info.get('es_constante', False):
            self.registrar_error(
                f"Línea {nodo.linea}: Error semántico — No se puede modificar el valor de la constante '{nodo.nombre_variable}'."
            )
            return

        res = self.visitar(nodo.expresion)
        if res is None:
            return

        val_nuevo, tipo_exp = res
        tipo_var = info['tipo']
        valido = (tipo_var == tipo_exp) or (tipo_var == 'REAL' and tipo_exp == 'INTEGER')

        if valido:
            etiqueta = str(val_nuevo) if val_nuevo is not None else "NULL (operando sin inicializar)"
            self.trazar(f"Asignación: {nodo.nombre_variable} ← {etiqueta}  (Línea {nodo.linea})")
            self.tabla_actual.actualizar_valor(nodo.nombre_variable, val_nuevo, nodo.linea)
        else:
            self.registrar_error(
                f"Línea {nodo.linea}: Incompatibilidad — "
                f"no se puede asignar '{tipo_exp}' a '{nodo.nombre_variable}' (tipo '{tipo_var}')."
            )

    def visitar_NodoOperacionBinaria(self, nodo):
        r1 = self.visitar(nodo.operando_izquierdo)
        r2 = self.visitar(nodo.operando_derecho)
        # Verificamos que sean tuplas; el valor interno puede ser None (variable sin inicializar)
        if r1 is None or r2 is None:
            return None
        v1, t1 = r1
        v2, t2 = r2
        op = nodo.operador

        if op in ['+', '-', '*', '/']:
            if t1 not in ['INTEGER', 'REAL'] or t2 not in ['INTEGER', 'REAL']:
                self.registrar_error(
                    f"Línea {nodo.linea}: Operación aritmética inválida entre '{t1}' y '{t2}'."
                )
                return None
            t_res = 'REAL' if (op == '/' or t1 == 'REAL' or t2 == 'REAL') else 'INTEGER'
            # Si algún operando es NULL, no podemos calcular pero sí sabemos el tipo
            if v1 is None or v2 is None:
                return None, t_res
            try:
                v = v1 + v2 if op == '+' else v1 - v2 if op == '-' else v1 * v2 if op == '*' else v1 / v2
                return v, t_res
            except Exception:
                return None, t_res

        if op in ['=', '<>', '<', '<=', '>', '>=']:
            son_num = t1 in ['INTEGER', 'REAL'] and t2 in ['INTEGER', 'REAL']
            if t1 != t2 and not son_num:
                self.registrar_error(
                    f"Línea {nodo.linea}: Comparación inválida entre '{t1}' y '{t2}'."
                )
                return None
            return None, 'BOOLEAN'

        return None

    def visitar_NodoOperacionUnaria(self, nodo):
        res = self.visitar(nodo.expresion)
        if res is None:
            return None
        val, tipo = res
        if nodo.operador == 'NOT':
            if tipo != 'BOOLEAN':
                self.registrar_error(
                    f"Línea {nodo.linea}: NOT requiere BOOLEAN, se encontró '{tipo}'."
                )
            return val, 'BOOLEAN'
        if nodo.operador == '-':
            if tipo not in ['INTEGER', 'REAL']:
                self.registrar_error(
                    f"Línea {nodo.linea}: Negación unaria requiere numérico, se encontró '{tipo}'."
                )
            return ((-val) if val is not None else None), tipo
        return res

    def visitar_NodoVariable(self, nodo):
        info = self.tabla_actual.buscar_variable(nodo.nombre)
        if not info:
            self.registrar_error(f"Línea {nodo.linea}: Variable no declarada '{nodo.nombre}'.")
            return None
        return info['valor'], info['tipo']

    def visitar_NodoLiteral(self, nodo):
        return nodo.valor, nodo.tipo_literal

    def visitar_NodoCondicionalIf(self, nodo):
        res = self.visitar(nodo.condicion)
        if res and res[1] != 'BOOLEAN':
            self.registrar_error(
                f"Línea {nodo.linea}: Condición IF debe ser BOOLEAN, se encontró '{res[1]}'."
            )
        self.visitar(nodo.bloque_verdadero)
        if nodo.bloque_falso:
            self.visitar(nodo.bloque_falso)

    def visitar_NodoBucleWhile(self, nodo):
        res = self.visitar(nodo.condicion)
        if res and res[1] != 'BOOLEAN':
            self.registrar_error(
                f"Línea {nodo.linea}: Condición WHILE debe ser BOOLEAN, se encontró '{res[1]}'."
            )
        self.visitar(nodo.cuerpo_bucle)

    def visitar_NodoLectura(self, nodo):
        for nombre in nodo.nombres_variables:
            info = self.tabla_actual.buscar_variable(nombre)
            if not info:
                self.registrar_error(f"Línea {nodo.linea}: Variable '{nombre}' no declarada en READ.")
            elif info.get('es_constante', False):
                self.registrar_error(
                    f"Línea {nodo.linea}: Error semántico — No se puede pasar la constante '{nombre}' como argumento de lectura READ."
                )

    def visitar_NodoEscritura(self, nodo):
        self.visitar(nodo.lista_expresiones)

    def visitar_NodoLlamadaSubprograma(self, nodo):
        info = self.tabla_actual.buscar_variable(nodo.nombre)
        if not info or info['tipo'] not in ('PROCEDURE', 'FUNCTION'):
            self.registrar_error(
                f"Línea {nodo.linea}: '{nodo.nombre}' no es un procedimiento o función conocido."
            )