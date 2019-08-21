"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self,PC,IR,reg,ram):
        """Construct a new CPU."""
        self.reg = [0] * 8
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
        self.IR = self.PC
        
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        PUSH = 'find what needs to go here'
        POP = 'find what needs to go here'
        SP = 0

        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while running:
            command = self.ram[self.IR]
            if command == LDI:
                self.ram_read(command)
                self.reg[operand_a] = operand_b
                self.PC += 3
            elif command == PRN:
                print(self.reg[operand_a])
                self.PC += 2
            elif command == HLT:
                running = False
            elif command == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.PC += 3
            elif command == PUSH:
                ram = self.ram[self.PC + 1]
                val = self.reg[ram]
                self.reg[SP] -= 1
                ram[self.reg[SP]] = val
                self.PC += 2
            elif command == POP:
                ram = self.ram[self.PC + 1]
                val = self.reg[ram]
                self.reg[SP] += 1
                ram[self.reg[SP]] = val
                self.PC += 2

            else:
                print(f"unknown command {command}")