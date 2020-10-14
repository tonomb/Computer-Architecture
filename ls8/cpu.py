"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUS = 0b01000101
POP = 0b01000110

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

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            IR = self.ram[self.pc]  # instruction register 

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # print(f'{IR} in binary {IR:b}')

            # HLT 
            if IR ==  HLT:
                running = False

            # LDI
            elif IR == LDI:
                self.reg[operand_a] = operand_b   # set register to value 

            # PRN
            elif IR == PRN: 
                print(self.reg[operand_a])

            #MUL
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)

            #PUSH
            elif IR ==PUS:
                # Decrement the SP
                self.reg[SP] -= 1
                #Copy the value in the given register 
                value = self.reg[operand_a]
        
                # to the address pointed to by SP.
                top_of_stack = self.reg[SP]
                self.ram[top_of_stack] = value
                
            #POP
            elif IR ==POP:
                # Copy the value from the address pointed to by SP
                top_of_stack = self.reg[SP]
                value = self.ram[top_of_stack]

                # save value in register
                self.reg[operand_a] = value

                # Increment SP
                self.reg[SP] += 1


            else:
                print(f"unknown instruction {IR:b} at address {self.pc}")
                sys.exit(1)

            
            inst_len = ((IR & 0b11000000) >> 6) + 1
            self.pc += inst_len


    def ram_read(self, address):
        return self.ram[address]
    

    def ram_write(self, address, value):
        self.ram[address] = value 
