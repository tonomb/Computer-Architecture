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


# "opcode" == the intructions byte
# "operands" == arguments to the instruction

PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4

memory = [0] * 256

# Variables are called "registers".
# * There are a fixed number
# * They have preset names R0, R1, R2, R3 ... R7
# Registers can hold a single byte 

register = [0] * 8

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

    else:
        print(f"unknown instruction {instruction} at address {instruction}")
        sys.exit(1)
