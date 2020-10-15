"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUS = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET =  0b00010001
ADD = 0b10100000

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # holds 256 bytes 
        self.reg = [0] * 8   # sets the registers  
        self.pc = 0
        self.reg[SP] = 0xf4    # empty stack pointer
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('Usage: ls8.py progname')
            sys.exit(1)

        file_name = sys.argv[1]

        with open('examples/' + file_name) as f:
            for line in f:
                line = line.strip()
                if line == '' or line[0] == '#':
                    continue

                str_value = line.split('#')[0]
                value = int(str_value, 2)
            
                self.ram[address] = value
                address += 1
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL': 
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def push_value(self, value):
        # Decrement the SP
        self.reg[SP] -= 1

        # to the address pointed to by SP.
        top_of_stack = self.reg[SP]
        self.ram[top_of_stack] = value

    def pop(self):
        # Copy the value from the address pointed to by SP
        top_of_stack = self.reg[SP]
        value = self.ram[top_of_stack]

        # Increment SP
        self.reg[SP] += 1

        return value 
        # # save value in register
        # self.reg[operand_a] = value

        

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            IR = self.ram[self.pc]  # instruction register 

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # print(f'{IR} in binary {IR:b}')

            # HALT
            if IR ==  HLT:
                running = False

            # LDI
            elif IR == LDI:
                self.reg[operand_a] = operand_b   # set register to value 

            # PRINT
            elif IR == PRN: 
                print(self.reg[operand_a])

            #MULTIPLY
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)

            #PUSH
            elif IR == PUS:
                value = self.reg[operand_a]
                self.push_value(value)
                
            #POP
            elif IR == POP:
                value = self.pop()
                # save value in register
                self.reg[operand_a] = value

            # CALL
            elif IR == CALL:
                # push next address onto the stack 
                self.push_value(self.pc + 2)

                # set the address to pc
                addr = self.reg[operand_a]
                self.pc = addr
            # ADD
            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)

            # RETURN
            elif IR == RET:
                # Pop the value from the top of the stack
                value = self.pop()
               
                # store value in the PC.
                self.pc = value


            else:
                print(f"unknown instruction {IR:b} at address {self.pc}")
                sys.exit(1)

            
            if ((IR & 0b00010000) >> 4) == 1:
                pass
            else:
                inst_len = ((IR & 0b11000000) >> 6) + 1
                self.pc += inst_len



    def ram_read(self, address):
        return self.ram[address]
    

    def ram_write(self, address, value):
        self.ram[address] = value 
