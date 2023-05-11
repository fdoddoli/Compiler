from ply import lex
from ply import yacc

# Definir tokens que se utilizarán
tokens = (
'bracket_isq',
'bracket_der',
'id',
'string',
'int',
'float',
'var',
'print',
'si',
'sino',
'mientras',
'prog',
'end',
'menor',
'mayor',
'menor_mayor',
'por',
'mas',
'menos',
'div',
'igual',
'par_isq',
'par_der',
'dos_puntos',
'comma',
'punto_comma',
'cte_i',
'cte_f'
)

# Token matching rules are written as regexs
t_id = r'id[A-Za-z0-9]*'
t_cte_i = r'[0-9]+'
t_cte_f = r'[0-9]+\.[0-9]+'
t_string = r'\"[a-zA-Z\s]+\"'
t_int = r'int'
t_float = r'float'
t_var = r'var'
t_print = r'print'
t_si = r'si'
t_sino = r'sino'
t_mientras = r'mientras'
t_prog = r'prog'
t_end = r'end'
t_menor = r'\<'
t_mayor = r'\>'
t_menor_mayor = r'\<\>'
t_por = r'\*'
t_mas = r'\+'
t_menos = r'\-'
t_div = r'/'
t_igual = r'\='
t_par_isq = r'\('
t_par_der = r'\)'
t_dos_puntos = r'\:'
t_comma = r'\,'
t_punto_comma = r'\;'
t_bracket_isq = r'\['
t_bracket_der = r'\]'

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– 

# ESTRUCTURAS DE DATOS


# Tabla De Variables
# (nombre, direccion))

# Las direcciones se manejan como un contador donde
# Las direcciones de enteras son de 1000 a 1999
# Las direcciones flotantes son de 2000 a 2999
# Las direcciones booleanas son de 3000 a 3999
# Las direcciones constantes enteras son de 4000 a 4999
# Las direcciones constantes flotantes son de 5000 a 5999

tabla_de_variables = {}

# Tabla de Constantes para cambiar los números por direcciones y así no confundir
# las constantes por las direcciones
# (constante, dirección)
tabla_de_constantes = {}

# = -> 9
# * -> 5
# / -> 6
# + -> 4
# print -> 26
# > 7
# < 8
# <> 10
tabla_de_operadores = {"=":20,"*":7,"/":6,"+":4,"-":5, "print":100,">":10,"<":11,"<>":12, "GotoF":101, "Goto":102, "GotoT":103}

# Contadores de Direcciones
# Current type sólo es int o float, no te dice si es cte_i o cte_f
tabla_de_direcciones = {"int":1000,"float":2000,"bool":3000,"cte_i":4000, "cte_f":5000}

#Codigo numerico para fondeo falso (parentesis): 99

# Definimos nuestras pilas de operandos, operadores, y jumps
pila_operandos = [] #cómo sabe python si es un stack o un queue
pila_operadores = []
pila_tipos = []
pila_jumps = []
fila_quadruplos = []

# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

#Variables Globales
current_type = ''
cont = 0 #Contador de quadruplos


#Fución de Fill
def fill(quad_number, fill_number):
    #Reemplazar tupla con una nueva
    lista_quadruplo = list(fila_quadruplos[quad_number])
    lista_quadruplo[3] = fill_number
    fila_quadruplos[quad_number] = tuple(lista_quadruplo)

# Tabla de Consideraciones
def tabla_de_consideraciones(left_operand, right_operand, operator):
    if(operator == 10 or operator == 11 or operator == 12):
        return "bool"
    elif((1000 <= left_operand <= 1999 or 4000 <= left_operand <= 4999) and (1000 <= left_operand <= 1999 or 4000 <= left_operand <= 4999) and (operator == 4 or operator == 5 or operator == 7)):
        return "int"
    elif((1000 <= left_operand <= 1999 or 4000 <= left_operand <= 4999) and (1000 <= left_operand <= 1999 or 4000 <= left_operand <= 4999) and operator == 6):
        return "float"
    elif((1000 <= left_operand <= 1999 or 4000 <= left_operand <= 4999) and (2000 <= left_operand <= 2999 or 5000 <= left_operand <= 5999) and (operator == 4 or operator == 5 or operator == 6 or operator == 7)):
        return "float"
    elif((2000 <= left_operand <= 2999 or 5000 <= left_operand <= 5999) and (2000 <= left_operand <= 2999 or 5000 <= left_operand <= 5999) and (operator == 4 or operator == 5 or operator == 6 or operator == 7)):
        return "float"
    else:
        print("Error en parámetros, el tipo de operando es incorrecto.")
    
#––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Programas de Prueba:
# Asignacion
    # prog id; var int: id2, id3, id4; [id2 = (5 + 3) * 5;] end
    # prog id; var int: id2, id3; [id2 = (5 + 3) / 2;] end
    # prog id; var int: id2, id3; [id2 = (5 - 3);] end
    # prog id; var int: id2; [id2 = 5;] end
    # prog id; var int: id1, id2; [id1 = 5; id2 = id1 * 4;] end
# Condicion
    # prog id; var int: id2; [si (5 > 3) [id2 = 200;] sino [id2 = 100;];] end
    # prog id; var int: id2; [si (5 < 3) [id2 = 200;] sino [id2 = 3;];] end
# Ciclo
    # prog id; var int: id2; [id2 = 0; mientras (id2 < 5) [print(id2); id2 = id2 + 1;];] end
    # prog id; var int: id2; [id2 = 8; mientras (id2 > 5) [print(id2); id2 = id2 - 1;];] end
# Escritura
    # prog id; var int: id2; [print("Hello World");] end 
    # prog id; var int: id2; [print(3 + 5);] end
    # prog id; var int: id2; [print("Hello World", 3 + 5);] end 
# Otro
    # prog id; var int: id1, id2, idFib; [id1 = 1; id2 = 1; idFib = 0; mientras (idFib < 5) [idFib = id1 + id2; id1 = id2; id2 = idFib; print(idFib);];] end

#––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
    
# Build the lexer object
lexer = lex.lex()

# Test it out
data = '''
prog id; var int: id2, id3; [id2 = (5 + 3) * 5;] end
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

# --- Parser

# Write functions for each grammar rule which is
# specified in the docstring.

start = "programa"


def p_programa(p):
    '''programa : prog id punto_comma vars cuerpo end 
                | prog id punto_comma end
    '''
    print("parsing completed")
    global cont
    for i in range(len(fila_quadruplos)):
        print(fila_quadruplos[i])
    
    
def p_tipo(p):
    '''tipo : int seen_tipo
            | float seen_tipo
    '''
    
def p_seen_tipo(p):
    "seen_tipo :"
    global current_type
    current_type = p[-1]


def p_vars(p):
    '''vars : var vars_uno
    '''
    

def p_vars_uno(p):
    ''' vars_uno : tipo dos_puntos id seen_id vars_dos punto_comma vars_tres
    '''

def p_vars_dos(p):
    ''' vars_dos : vars_tres
                 | comma id seen_id vars_dos
                 | empty
    '''
    
def p_vars_tres(p):
    ''' vars_tres : vars_uno
                 | empty
    '''
    
def p_seen_id(p):
    "seen_id :"
    if(p[-1] in tabla_de_variables):
        print("Error: La variable ya está declarada")
    else:
        cont = tabla_de_direcciones[current_type]
        tabla_de_variables[p[-1]] = cont
        tabla_de_direcciones[current_type] = cont + 1
        
def p_cuerpo(p):
    '''cuerpo : bracket_isq cuerpo_dos bracket_der
    '''
    
def p_cuerpo_dos(p):
    '''cuerpo_dos : estatuto cuerpo_dos
                  | empty
    '''
    

def p_termino(p):
    '''termino : factor seen_factor termino_dos'''
    
def p_seen_factor(p):
    "seen_factor :"
    if(pila_operadores):
        if(pila_operadores[-1] == 7 or pila_operadores[-1] == 6):
            right_operand = pila_operandos.pop()
            right_type = pila_tipos.pop()
            left_operand = pila_operandos.pop()
            left_type = pila_tipos.pop()
            operator = pila_operadores.pop()
            result_type = tabla_de_consideraciones(left_type, right_type, operator)
            if(result_type in ["int", "float"]):
                #Generar result
                cont_result = tabla_de_direcciones[result_type] #AVAIL.NEXT()
                result = cont_result
                #Sumar contador
                tabla_de_direcciones[result_type] = cont_result + 1
                #Generar quadrupla y agregarla a fila de quadruplas
                fila_quadruplos.append((operator, left_operand, right_operand, result))
                global cont
                cont = cont + 1
                pila_operandos.append(result) 
                pila_tipos.append(result)
               
            else:
                print("Error, type mismatch")
            
            
def p_termino_dos(p):
    '''termino_dos : por seen_por_div termino
                   | div seen_por_div termino
                   | empty'''
    
def p_seen_por_div(p):
    "seen_por_div :"
    cont = tabla_de_operadores[p[-1]]
    pila_operadores.append(cont)
    

def p_exp(p):
    '''exp : termino seen_termino exp_dos
    '''

def p_exp_dos(p):
    '''exp_dos : mas seen_exp_op exp
               | menos seen_exp_op exp
               | empty
    '''
    
    
def p_seen_exp_op(p):
    "seen_exp_op :"
    cont = tabla_de_operadores[p[-1]]
    pila_operadores.append(cont)
    

def p_seen_termino(p):
    "seen_termino :"
    if(pila_operadores):
        if(pila_operadores[-1] == 4 or pila_operadores[-1] == 5): #la comparación de debe hacer con 'mas' o '+'
            right_operand = pila_operandos.pop()
            right_type = pila_tipos.pop()
            left_operand = pila_operandos.pop()
            left_type = pila_tipos.pop()
            operator = pila_operadores.pop()
            result_type = tabla_de_consideraciones(left_type, right_type, operator) #Obtiene la consideración
            if(result_type in ["int", "float"]):
                #Generar result
                result = tabla_de_direcciones[result_type]
                #Sumar contador
                tabla_de_direcciones[result_type] = result + 1
                #Generar quadrupla y agregarla a fila de quadruplas
                fila_quadruplos.append((operator, left_operand, right_operand, result))
                global cont
                cont = cont + 1
                pila_operandos.append(result)
                pila_tipos.append(result)
                
            else:
                print("Error, type mismatch")
    
    
def p_expresion(p):
    '''expresion : exp
                 | exp mayor seen_expresion_op exp seen_expresion_bool
                 | exp menor seen_expresion_op exp seen_expresion_bool
                 | exp menor_mayor seen_expresion_op exp seen_expresion_bool'''
    
def p_seen_expresion_op(p):
    "seen_expresion_op :"
    cont = tabla_de_operadores[p[-1]]
    pila_operadores.append(cont)

def p_seen_expresion_bool(p):
    "seen_expresion_bool :"
    if(pila_operadores):
        if(pila_operadores[-1] in [10,11,12]):
            right_operand = pila_operandos.pop()
            right_type = pila_tipos.pop()
            left_operand = pila_operandos.pop()
            left_type = pila_tipos.pop()
            operator = pila_operadores.pop()
            result_type = tabla_de_consideraciones(left_type, right_type, operator) #Obtiene la consideración
            if(result_type in ["bool"]):
                #Generar result
                result = tabla_de_direcciones[result_type]
                #Sumar contador
                tabla_de_direcciones[result_type] = result + 1
                #Generar quadrupla y agregarla a fila de quadruplas
                fila_quadruplos.append((operator, left_operand, right_operand, result))
                global cont
                cont = cont + 1
                pila_operandos.append(result)
                pila_tipos.append(result)
                
            else:
                print("Error, type mismatch")
    
    


def p_const_var(p):
    '''const_var : id seen_const_var_id
                 | cte_i seen_const_var_cte_i
                 | cte_f seen_const_var_cte_f
'''
    

def p_seen_const_var_id(p):
    "seen_const_var_id :"
    #Buscar en la tabla de variables
    cont_operando = tabla_de_variables[p[-1]]
    #Ingresar direccion a pila de operando
    pila_operandos.append(cont_operando)
    #Encontrar dirección a pila de tipos
    pila_tipos.append(cont_operando)
    
    
def p_seen_const_var_cte_i(p):
    "seen_const_var_cte_i :"
    
    #Si la constante ya se ha visto antes, entonces tomar direccion de esa constante
    # Sino, entonces sí lo metemos a la tabla de constantes
    if(p[-1] in tabla_de_constantes):
        cont_operando = tabla_de_constantes[p[-1]]
        pila_operandos.append(cont_operando)
    else:
        cont_cte_i = tabla_de_direcciones["cte_i"]
        tabla_de_constantes[p[-1]] = cont_cte_i
        #Actualizar contador
        tabla_de_direcciones["cte_i"] = cont_cte_i + 1
        #Ingresar direccion a pila de operando
        pila_operandos.append(cont_cte_i)
    
    #Ingresar direccion a pila de tipos
    pila_tipos.append(tabla_de_constantes[p[-1]])
    
    
    
    
def p_seen_const_var_cte_f(p):
    "seen_const_var_cte_f :"
    #Si la constante ya se ha visto antes, entonces tomar direccion de esa constante
    # Sino, entonces sí lo metemos a la tabla de constantes
    if(p[-1] in tabla_de_constantes):
        cont_operando = tabla_de_constantes[p[-1]]
        pila_operandos.append(cont_operando)
    else:
        cont_cte_f = tabla_de_direcciones["cte_f"]
        tabla_de_constantes[p[-1]] = cont_cte_f
        #Actualizar contador
        tabla_de_direcciones["cte_f"] = cont_cte_f + 1
        #Ingresar direccion a pila de operando
        pila_operandos.append(cont_cte_f)
    
    #Ingresar direccion a pila de tipos
    pila_tipos.append(tabla_de_constantes[p[-1]])
    
def p_factor(p):
    '''factor : par_isq seen_par_isq expresion par_der seen_par_der
              | mas seen_factor_op const_var
              | menos seen_factor_op const_var
              | const_var'''
    

def p_seen_par_isq(p):
    "seen_par_isq :"
    #Mete un fondo falso a la pila de operadores
    pila_operadores.append(99)
    
def p_seen_par_der(p):
    "seen_par_der :"
    pila_operadores.remove(99)
    
def p_seen_factor_op(p):
    "seen_factor_op :"
    cont = tabla_de_operadores[p[-1]]
    pila_operadores.append(cont)
    
    
def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | escritura
'''
    
def p_asigna(p):
    '''asigna : id igual seen_asigna expresion punto_comma seen_punto_comma_asigna'''
    
def p_seen_asigna(p):
    "seen_asigna :"
    #Obtener direccion del operador igual
    cont_igual = tabla_de_operadores[p[-1]]
    #Meter a la pila de operadores
    pila_operadores.append(cont_igual)
    #Sacar la direccion del operando
    cont_id = tabla_de_variables[p[-2]]
    #Meter a la pila de operandos
    pila_operandos.append(cont_id)

def p_seen_punto_comma_asigna(p):
    "seen_punto_comma_asigna :"
    #Función para generar nuevo quadruplo
    cont_igual = pila_operadores.pop()
    result = pila_operandos.pop()
    const_id = pila_operandos.pop()
    #Generamos nuevo quadruplo
    quadruplo = (cont_igual, result, None, const_id)
    fila_quadruplos.append(quadruplo)
    #Aumentamos contador de quadruplos
    global cont
    cont = cont + 1
    


def p_condicion(p):
    '''condicion : si par_isq seen_par_isq expresion seen_expresion par_der seen_par_der cuerpo punto_comma seen_punto_comma
                 | si par_isq seen_par_isq expresion seen_expresion par_der seen_par_der cuerpo sino seen_sino cuerpo punto_comma seen_punto_comma
     '''
    
def p_seen_expresion(p):
    "seen_expresion :"
    #La expresion es booleana?
    exp_type = pila_tipos.pop()
    if(exp_type > 3999 or exp_type < 3000):
        print("Error: Type Mismatch")
    else:
        #Generar quadruplo y agregarla a fila de quadruplos
        result = pila_operandos.pop()
        dir_gotof = tabla_de_operadores["GotoF"]
        quadruplo = (dir_gotof, result, None, None)
        fila_quadruplos.append(quadruplo)
        #Actualizamos contador de quadruplos
        global cont
        cont = cont + 1
        #Agregamos el número donde se encuentra el GotoF a fila de jumps
        pila_jumps.append(cont - 1)
    
def p_seen_punto_comma(p):
    "seen_punto_comma :"
    end = pila_jumps.pop()
    global cont
    #Llamamos función de Fill
    fill(end, cont)
    
def p_seen_sino(p):
    "seen_sino :"
    dir_goto = tabla_de_operadores["Goto"]
    quadruplo = (dir_goto, None, None, None)
    fila_quadruplos.append(quadruplo)
    global cont
    cont = cont + 1
    false = pila_jumps.pop()
    pila_jumps.append(cont - 1)
    fill(false, cont)
    
    
def p_ciclo(p):
    '''ciclo : mientras seen_mientras par_isq seen_par_isq expresion seen_expresion par_der seen_par_der cuerpo punto_comma seen_ciclo_punto_comma'''
    
def p_seen_mientras(p):
    "seen_mientras :"
    global cont
    pila_jumps.append(cont)

def p_seen_ciclo_punto_comma(p):
    "seen_ciclo_punto_comma :"
    end = pila_jumps.pop()
    result = pila_jumps.pop()
    dir_goto = tabla_de_operadores["Goto"]
    quadruplo = (dir_goto, None, None, result)
    fila_quadruplos.append(quadruplo)
    global cont
    cont = cont + 1
    fill(end, cont)

    
    
def p_escritura(p):
    '''escritura : print par_isq escritura_uno par_der punto_comma 
    '''


def p_escritura_uno(p):
    '''escritura_uno : expresion seen_escritura_exp escritura_uno 
                     | comma expresion seen_escritura_exp escritura_uno
                     | string seen_escritura_string escritura_uno 
                     | empty
    '''

def p_seen_escritura_string(p):
    "seen_escritura_string :"
    #Generar cuadrupla con left_op y right_op vacíos
    cont_print = tabla_de_operadores["print"]
    fila_quadruplos.append((cont_print, None, None, p[-1]))
    #Actualizamos contador
    global cont
    cont = cont + 1

def p_seen_escritura_exp(p):
    "seen_escritura_exp :"
    #Generar cuadrupla con left_op y right_op vacíos
    cont_print = tabla_de_operadores["print"]
    cont_operando = pila_operandos.pop()
    fila_quadruplos.append((cont_print, None, None, cont_operando))
    #Actualizamos contador
    global cont
    cont = cont + 1
    

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    

    
    
import ply.yacc as yacc
parser = yacc.yacc()

cont_parser = 0
while cont_parser < 1:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)
    cont_parser += 1
    
    
    