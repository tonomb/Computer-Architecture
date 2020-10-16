import sys 

# Memroy
# -------
# Holds bytes
# Big array of bytes
# to get or set data in memory, you need the index in the array
# these erma re equivalent:
#* address 
#* locations
#* pointer

def push_val(value):
        # decrement the stack pointer 
        register[SP] -= 1

        #push to top of stack
        top_of_stack = register[SP]
        memory[top_of_stack] = value

def pop_val():
    #copy value from top of stack 
    top_of_stack = register[SP]
    value = memory[top_of_stack]

    # increment the stack pointer 
    register[SP] += 1

    return value


# "opcode" == the intructions byte
# "operands" == arguments to the instruction

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4
PUSH = 5
POP = 6
CALL= 7
RET = 8

memory = [0] * 256

# Variables are called "registers".
# * There are a fixed number
# * They have preset names R0, R1, R2, R3 ... R7
# Registers can hold a single byte 

register = [0] * 8

SP = 7
register[SP] = 0xf4 # <-- Stack pointer 

address = 0

if len(sys.argv) != 2:
    print('Usage: comp.py progname')
    sys.exit(1)

file_name = sys.argv[1]

file_name += '.txt'

# sys.exit()

try: 
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if line == '' or line[0] =='#':
                continue

            try:
                str_value = line.split('#')[0]
                value = int(str_value, 10)   # base 10 

            except ValueError:
                print(f'Invalid number: {str_value}')
                sys.exit(1)

            memory[address] = value
            address += 1

except FileNotFoundError:
    print(f'File not found: {sys.argv[1]}.txt')
    sys.exit(2)


# keep track of the address of the currently-executing instuction
pc = 0 # program counter, pointer to the instruction we're executing 

halted = False

while not halted:
    instruction = memory[pc]
    if instruction == PRINT_BEEJ:  #PRINT_BEEJ
        print('Beej!')
        pc += 1
    
    elif  instruction == HALT: #HALT
        halted = True
        pc += 1

    elif instruction == SAVE_REG: # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value 
        pc += 3

    elif instruction == PRINT_REG: # PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2

    elif instruction == PUSH:
        # decrement the stack pointer 
        register[SP] -= 1

        #grab the value out of the given register 
        reg_num = memory[pc + 1]
        value = register[reg_num]

        #push to top of stack
        top_of_stack = register[SP]
        memory[top_of_stack] = value

        pc += 2

    elif instruction == POP:
        #copy value from top of stack 
        top_of_stack = register[SP]
        value = memory[top_of_stack]

        # store in a register
        reg_num = memory[pc + 1]
        register[reg_num] = value

        # increment the stack pointer 
        register[SP] += 1

        pc += 2

    elif instruction == CALL:
        # get address of the next instruction after the call
        return_addr = pc + 2

        # push it on the stack
        push_val(return_addr)

        # get subroutine address from register
        reg_num = memory[ pc + 1]
        subroutine_addr = register[reg_num]

        pc = subroutine_addr

    elif instruction == RET:
        # get return addr from the top of the stack 
        return_addr = pop_val()

        # store it in the pc
        pc = return_addr


    else:
        print(f"unknown instruction {instruction} at address {instruction}")
        sys.exit(1)
