"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self,PC,IR,reg,ram):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.ram = [0] * 255
        self.PC = 0 
        self.IR = 0 

    def halt(self):
        print('Stopping program')
        sys.exit(1)
    
    # should accept the address to read and return the value stored there.
    def ram_read(self,MAR):
        return self.ram[MAR]
        
    #  should accept a value to write, and the address to write it to.
    def ram_write(self,MDR,MAR):
        self.ram[MAR] = MDR
    
    def pop(self,reg):
        self.reg[reg] = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def push(self, reg):
        self.reg[7] -= 1
        self.ram_write(self.reg[reg], self.reg[7])        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    num = line[0].split("#",1)
                    if num.strip() is "":
                        continue
                    self.ram[address] = int(num,2)
                    address += 1
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} where not found")

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        command = self.ram_read(self.PC)

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while running:
            command = self.ram[self.IR]
            if command == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif command == PRN:
                print(f"Register: {operand_a}, Value: {self.reg[operand_a]}")
                self.PC += 2
            elif command == HLT:
                running = False
                self.PC +=1
            elif command == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3
            elif command == PUSH:
                self.push(operand_a)
                self.PC += 2
            elif command == POP:
                self.pop(operand_a)
                self.PC += 2
            elif command == CALL:
                # this will push the next command to the stack
                # and preform the subroutine
                self.push(operand_a)
                self.PC += 2
            elif command == RET:
                # this will pop the first command from the stack and
                # put it into PC
                self.pop(operand_a)
                self.PC += 1
            else:
                print(f"unknown command {command}")