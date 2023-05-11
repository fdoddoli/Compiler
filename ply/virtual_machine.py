from lexer_parser import tabla_de_constantes, tabla_de_variables, tabla_de_direcciones, tabla_de_operadores, fila_quadruplos


# Implementación

# Fase 1
# En un nuevo arreglo, voltiar tabla_de_contantes para que la llave sea la direccion
# En un nuevo arreglo, voltiar tabla_de_variables para que la llave sea la direccion
# Hacer una nueva tabla de memoria global, donde la llave es la direccion y el valor es lo que se le asigna a esa variable
# Hacer una nueva tabla de memoria temporal donde la llave es la dirección, con los valores de resultados de operaciones, equivalentes a t1, t2, t3, etc

# Fase 2
# Implementar el switch hacer condicionales utilizando la tabla_de_operadores 
# para ver si el primer valor del quadruplo es una asignación o suma/resta/mult/div o comparacion o GOTOs


# Fase 3
# Hacer operaciones respectivas para 
# asignacion
# suma/resta/mult/div
# print
# comparacion
# Gotos


# Crear clase de Virtual Machine
class VirtualMachine:
    def __init__(self, tabla_de_constantes, tabla_de_direcciones, tabla_de_operadores, tabla_de_variables):
        self.tabla_de_constantes = tabla_de_constantes
        self.tabla_de_direcciones = tabla_de_direcciones
        self.tabla_de_operadores = tabla_de_operadores
        self.tabla_de_variables = tabla_de_variables
        self.fila_quadruplos = fila_quadruplos
        self.tabla_de_memoria_global = {}
        self.tabla_de_memoria_temporal = {}
    
    def __str__(self):
        return str(self)

    # Voltear diccionarios necesarios
    # En un nuevo arreglo, voltiar tabla_de_contantes para que la llave sea la direccion
    # En un nuevo arreglo, voltiar tabla_de_variables para que la llave sea la direccion
    def swap_tabla_de_constantes(self, tabla_de_constantes, tabla_de_variables):
        self.tabla_de_constantes = dict(
            [(int(x), int(y)) for (y, x) in tabla_de_constantes.items()]
        )

        self.tabla_de_variables = dict(
            [(x, y) for (y, x) in tabla_de_variables.items()]
        )

# Inicializar clase
virtual_machine = VirtualMachine(tabla_de_constantes, tabla_de_direcciones, tabla_de_operadores, tabla_de_variables)
virtual_machine.swap_tabla_de_constantes(tabla_de_constantes, tabla_de_variables)

#Current instruction pointer igual al contador de los quadruplos
current_ip = 0

def operacion(quadruplo, idx):
    if(quadruplo[idx] in range(1000,3000)):
        if(quadruplo[1] in virtual_machine.tabla_de_memoria_temporal):
            return virtual_machine.tabla_de_memoria_temporal[quadruplo[idx]]
        else: 
            return virtual_machine.tabla_de_memoria_global[quadruplo[idx]]
    elif(quadruplo[idx] in range(4000,6000)):
        return virtual_machine.tabla_de_constantes[quadruplo[idx]]

def switch(quadruplo):
    # Asigna
    global current_ip
    if(quadruplo[0] == 20):
        # Metemos en la tabla_de_memoria_global en la llave equivalente a quadruplo[3] 
        # el valor de quadruplo[1]
        if(quadruplo[1] in range(1000,3000)):
            #Asignación en Operación
            if(quadruplo[1] in virtual_machine.tabla_de_memoria_temporal):
                valor_de_resultado = virtual_machine.tabla_de_memoria_temporal[quadruplo[1]]
                virtual_machine.tabla_de_memoria_global[quadruplo[3]] = valor_de_resultado
            #Asignación de Id Solo
            else:
                valor_de_resultado = virtual_machine.tabla_de_memoria_global[quadruplo[1]]
                virtual_machine.tabla_de_memoria_global[quadruplo[3]] = valor_de_resultado
        #Asignación de Constante
        elif(quadruplo[1] in range(4000,6000)):
            valor_de_constante = virtual_machine.tabla_de_constantes[quadruplo[1]]
            virtual_machine.tabla_de_memoria_global[quadruplo[3]] = valor_de_constante
    # Mas
    elif(quadruplo[0] == 4):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq + elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Menos
    elif(quadruplo[0] == 5):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq - elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Div
    elif(quadruplo[0] == 6):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq / elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Por
    elif(quadruplo[0] == 7):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq * elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Print
    elif(quadruplo[0] == 100):
        # Si sólo es un string
        if(isinstance(quadruplo[3], str)):
            print(quadruplo[3])
        else:
            if(quadruplo[3] in range(1000,3000)):
                #Asignación en Operación
                if(quadruplo[3] in virtual_machine.tabla_de_memoria_temporal):
                    valor_de_resultado = virtual_machine.tabla_de_memoria_temporal[quadruplo[3]]
                    print(valor_de_resultado)
                #Asignación de Id Solo
                else:
                    valor_de_resultado = virtual_machine.tabla_de_memoria_global[quadruplo[3]]
                    print(valor_de_resultado)
            #Asignación de Constante
            elif(quadruplo[3] in range(4000,6000)):
                valor_de_constante = virtual_machine.tabla_de_constantes[quadruplo[3]]
                print(valor_de_constante)
    # Comparación: Mayor que
    elif(quadruplo[0] == 10):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq > elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Comparación: Menor que
    elif(quadruplo[0] == 11):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq < elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    # Comparación: Menor Mayor que
    elif(quadruplo[0] == 12):
        elemento_izq = operacion(quadruplo, 1)
        elemento_der = operacion(quadruplo, 2)
        resultado = elemento_izq != elemento_der
        virtual_machine.tabla_de_memoria_temporal[quadruplo[3]] = resultado
    #GotoF
    elif(quadruplo[0] == 101):
        resultado = virtual_machine.tabla_de_memoria_temporal[quadruplo[1]]
        if(resultado == False):
            current_ip = quadruplo[3] - 1
    #GotoF
    elif(quadruplo[0] == 103):
        resultado = virtual_machine.tabla_de_memoria_temporal[quadruplo[1]]
        if(resultado == True):
            current_ip = quadruplo[3] - 1
    #Goto
    elif(quadruplo[0] == 102):
        current_ip = quadruplo[3] - 1
            

# Iterar fila de quadruplos
while(current_ip < len(fila_quadruplos)):
    switch(fila_quadruplos[current_ip])
    current_ip += 1

print(virtual_machine.tabla_de_memoria_global)
    
    




    


        


