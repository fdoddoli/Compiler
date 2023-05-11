# Introduction

This is my final proyect for the course Introduction to Compilers. I built a compiler in python for the following language using PLY as my parsing tool. 

<img width="811" alt="Screen Shot 2023-05-11 at 9 04 49 AM" src="https://github.com/fdoddoli/Compiler/assets/58672371/5c32e3c7-6a35-42c3-833a-2cd14abcbe01">


The proyect includes 2 main programs, a lexer and parser that generates quadruples for each line of operations, and a virtual machine that compiles the program. I simulate computer memory by assigning address values to variables, constants, and operators. 

# Technical Documentation

### Data Structures: Lexer and Parser

Variable Table: A dictionary with the variable name as the key and the address as the value.

Constant Table: A dictionary with the constant as the key and the address as the value.

Operator Table: A dictionary with the operator as the key and the address as the value.

Address Table: A dictionary used to maintain a counter for different variables seen in the program. The key represents the type (int, float, bool, cte_i, cte_f), and the value represents the address. The addresses for different types are divided into the following ranges: (int: 1000 to 1999, float: 2000 to 2999, bool: 3000 to 3999, cte_i: 4000 to 4999, cte_f: 5000 to 5999).

Operand Stack: A stack that holds the addresses of operands.

Operator Stack: A stack that holds the addresses of operators.

Type Stack: A stack that holds the addresses of types.

Jump Stack: A stack that holds the quadruple numbers to which it will jump when creating the GotoF, Goto, and GotoT quadruples.

Quadruple Table: A list of quadruples, where each quadruple is a tuple with four values: the address of the operator, the address of the left operand, the address of the right operand, and the address of the result.

### Data Structures: Virtual Machine

Variable Table: A dictionary with the address as the key and the value as the variable name.

Constant Table: A dictionary with the address as the key and the value as the constant.

### Main Developed Algorithms

Below are the most complex algorithms in the program. It should be noted that they do not represent the entirety of its functions.

**Function "fill":**

The "fill" function is used to populate the Goto, GotoF, and GotoT quadruples. It takes the current quadruple number and the quadruple counter as parameters. Since we cannot directly edit tuple values, we transform the quadruple tuple into a list, modify the desired value using its index, transform the list back into a tuple, and replace the original tuple with the new one.

**Functions "p_seen_factor," "p_seen_termino," and "p_seen_expresion_bool":**

These algorithms are very similar. The only difference is that "p_seen_factor" is called in the term grammar at the crucial point when exiting a factor, indicating that a multiplication or division was performed. On the other hand, "p_seen_termino" is called in the expression grammar at the crucial point when exiting a term, indicating that an addition or subtraction was performed. And "p_seen_expresion_bool" is called in the expression grammar at the crucial point when finishing a comparison.

Consequently, all three algorithms have a conditional statement that only allows entry when a multiplication or division was performed ("p_seen_factor"), or an addition or subtraction was performed ("p_seen_termino"), or a comparison with conditional operators such as greater than, less than, and not equal to was performed ("p_seen_expresion_bool"). Once this condition is met, the operands (right and left) and their respective types are popped from the stacks. Then, the consideration table is called to determine the data type of the operation, and the result is stored in "result_type." If the "result_type" is valid, a new address is obtained based on that type, and this value is stored in "result." Finally, a quadruple is generated with the operator, the left operand, the right operand, and the result.

**Function "p_seen_const_var_id":**

This function is used when the program encounters a constant or variable. It looks up the address in the variable table and pushes it onto the operand and type stacks.

**Functions "p_seen_const_var_cte_i" and "p_seen_const_var_cte_f":**

These functions are used when the program encounters an integer or float constant, respectively. The function first checks if the constant is already in the constant table. If it is, it retrieves its address and pushes it onto the operand stack.

Otherwise, for integer constants, we obtain the address using the address table and add it to the constant table, where the key is the constant and the value is the address. Additionally, we push the same address onto the operand stack. Finally, outside the if-else statement, we push the address onto the type stack.

Similarly, for float constants, we follow the same procedure as above, but instead of searching for the address in the address table using "cte_i," we use "cte_f" to indicate that we are looking for the address of a float constant.

**Function "p_seen_punto_comma_asigna":**

This function is called at the crucial point when finishing an assignment in order to generate a new quadruple. It retrieves the operator's address from the operator stack, the address that will store the assigned value from the operand stack, and the value being assigned from the operand stack. It then generates the quadruple and updates the global quadruple counter.

**Function "p_seen_expresion":**

This function is called at the crucial point in a condition, after encountering an expression. It first checks if the result of the expression is boolean; if not, it throws an error. Otherwise, it proceeds to generate a quadruple by retrieving


# Inputs to Test Program

**Equal to**
<img width="695" alt="Screen Shot 2023-05-11 at 9 00 42 AM" src="https://github.com/fdoddoli/Compiler/assets/58672371/f126bc79-cfbd-41ae-a3db-0e25ac3be5de">

**Conditional**
<img width="692" alt="Screen Shot 2023-05-11 at 9 01 08 AM" src="https://github.com/fdoddoli/Compiler/assets/58672371/5dd18a53-8fe6-4de5-8a29-a096a36f2003">

**While Loop**
<img width="693" alt="Screen Shot 2023-05-11 at 9 01 28 AM" src="https://github.com/fdoddoli/Compiler/assets/58672371/210495b5-00f9-49dd-84f4-a20ab9764cd9">

**Print**
<img width="694" alt="Screen Shot 2023-05-11 at 9 01 45 AM" src="https://github.com/fdoddoli/Compiler/assets/58672371/79e647a0-0e0a-477a-b0ac-4e188f614646">

# Steps to Run Proyect

1. Open the directory where the project is located in the terminal.
2. Run the following command: python3 virtual_machine.py
3. Enter the desired test.
