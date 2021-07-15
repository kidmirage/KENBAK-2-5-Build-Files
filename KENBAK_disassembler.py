import sys
import re
from argparse import ArgumentParser

# Setup the command line arguments.

parser = ArgumentParser("Disassemble a binary or delimited text file to KENBAK-1 source")
parser.add_argument("-s", "--save",
                    action="store_true", dest="saveResults", default=False,
                    help="save the disassembly to a .asm file")
parser.add_argument("-d", "--dump",
                    action="store_true", dest="dumpResults", default=False,
                    help="dump the disassembly to standard out")
parser.add_argument("-a", "--address",
                    action="store_true", dest="showAddress", default=False,
                    help="add the instruction address to each line")
parser.add_argument("-f", "--file", dest="filename", required=True,
                    help="file to disassemble", metavar="FILE")

# Initialize the memory buffer.
memory = bytearray(256)

# Create a map to distinguish between code bytes and data bytes.
codemap = bytearray(256)

# Define all of the available opcodes.
opCodes = {"add","sub","load","store","and","or","lneg","jmp","jmk","skp","set","sft","rot","nop","halt","org","db"}

# Register addresses.
register_addresses = [0, 1, 2, 3, 128, 129, 130, 131, 255]
register_names = ["A", "B", "X", "PC", "OUTPUT", "OCA", "OCB", "OCX", "INPUT"]

# Define the single byte instructions.
single_byte_opcodes = ["nop", "halt", "sft", "rot"]

memory_mode_opcodes = ["add", "sub", "load", "store", "and", "or", "lneg"]

# Maintain a list of instructions that have been disassembled. Each instruction will also
# be a list with the following values ["address", "label", "opcode", "operand"].
instructions = []

# Given the byte passed determine what opcode that byte represents.
def determine_opcode(opcode): 
    if opcode & 0b10000111 == 0b00000000:
        return "halt"
    elif opcode & 0b10000111 == 0b10000000:
        return "nop"
    elif opcode & 0b01000111 == 0b01000001:
        return "rot"
    elif opcode & 0b01000111 == 0b00000001:
        return "sft"
    elif opcode & 0b10000111 == 0b00000010:
        return "set"
    elif opcode & 0b10000111 == 0b10000010:
        return "skp"
    elif opcode & 0b00110000 == 0b00110000:
        return "jmk"
    elif opcode & 0b00110000 == 0b00100000:
        return "jmp"
    elif opcode & 0b11111000 == 0b11011000:
        return "lneg"
    elif opcode & 0b11111000 == 0b11000000:
        return "or"
    elif opcode & 0b11111000 == 0b11010000:
        return "and"
    elif opcode & 0b00111000 == 0b00011000:
        return "store"
    elif opcode & 0b00111000 == 0b00010000:
        return "load"
    elif opcode & 0b00111000 == 0b00001000:
        return "sub"
    elif opcode & 0b00111000 == 0b00000000:
        return "add"
    else:
        return "db"

# Format the operand into one of five different addressing modes. 
def create_addressing_mode_operand(opcode, operand):
    # Determine what register to use.
    register = ""
    
    if opcode & 0b11000000 == 0b11000000:
        # And and or operations.
        register = "A,"
    elif opcode & 0b11000000 == 0b00000000:
        register = "A,"
    elif opcode & 0b11000000 == 0b01000000:
        register = "B,"
    elif opcode & 0b11000000 == 0b10000000:
        register = "X,"
        
    # Find addressing mode.
    zfill = 3
    immediate = False
    if opcode & 0b00000111 == 0b00000011:
        # Immediate.
        pattern = "{0}{1}"
        zfill = 1
        immediate = True
    elif opcode & 0b00000111 == 0b00000100:
        # Memory.
        pattern = "{0}{1}"
    elif opcode & 0b00000111 == 0b00000101:
        # Indirect.
        pattern = "{0}({1}}"
    elif opcode & 0b00000111 == 0b00000110:
        # Indexed.
        pattern = "{0}{1}+X"
    elif opcode & 0b00000111 == 0b00000111:
        # Indirect, Indexed.
        pattern = "{0}({1})+X"
    
    # See if the address is a special register.
    if not immediate and operand in register_addresses:
        address = register_names[register_addresses.index(operand)]
    else:
        address = str(operand).zfill(zfill)
    
    # Return the operand string.
    return pattern.format(register, address)
    
    
# Given the byte passed determine what opcode that byte represents.
def determine_operand(symbol, opcode, operand):
    # Handle opcodes that have an addressing mode.
    if symbol in memory_mode_opcodes:
        return create_addressing_mode_operand(opcode, operand)
    elif symbol == "skp":
        bit = str((opcode & 0b00111000) >> 3)
        if opcode & 0b01000000 == 0b01000000:
            on = "1"
        else:
            on = "0"
        if operand in register_addresses:
            address = register_names[register_addresses.index(operand)]
        else:
            address = str(operand).zfill(3)
        return bit + "," + on + "," + address
    elif symbol == "set":
        bit = str((opcode & 0b00111000) >> 3)
        if opcode & 0b01000000 == 0b01000000:
            way = "1"
        else:
            way = "0"
        if operand in register_addresses:
            address = register_names[register_addresses.index(operand)]
        else:
            address = str(operand).zfill(3)
        return bit + "," + way + "," + address
    elif symbol in ["sft", "rot"]:
        if opcode & 0b10000000 == 0b10000000:
            way = "L"
        else:
            way = "R"
        places = (opcode & 0b00011000) >> 3
        if places == 0:
            places = 4
        if opcode & 0b00100000 == 0b00100000:
            reg = "B"
        else:
            reg = "A"
        return reg + "," + way + "," + str(places)
    elif symbol in ["jmp", "jmk"]:
        if operand in register_addresses:
            address = register_names[register_addresses.index(operand)]
        else:
            address = str(operand).zfill(3)
        if opcode & 0b00001000 == 0b00001000:
            address = "(" + address + ")"
        
        if opcode & 0b11000000 == 0b00000000:
            reg = "A"
        elif opcode & 0b11000000 == 0b01000000:
            reg = "B"
        elif opcode & 0b11000000 == 0b10000000:
            reg = "X"
        else:
            return address # Unconditional
        
        condition_number = opcode & 0b00000111
        if condition_number == 3:
            condition = "NE"
        elif condition_number == 4:
            condition = "EQ"  
        elif condition_number == 5:
            condition = "LT"  
        elif condition_number == 6:
            condition = "GE"  
        elif condition_number == 7:
            condition = "GT"  
           
        return reg + "," + condition + "," + address
    else:
        return str(operand).zfill(3)

# Return true the operator takes an immediate value.
def is_immediate(opcode, opvalue):
    if opcode in memory_mode_opcodes:
        if opvalue & 0b00000111 == 0b000000011:
            return True
    return False

def get_decimal(constant):
    # Figure out the base
    if len(constant) > 0:
        if constant[0] in {'-','1','2','3','4','5','6','7','8','9'}:
            base = 10  # Decimal
        elif constant.lower().startswith("0x"):
            base = 16  # Hex
            constant = constant[2:]
        elif constant.lower().startswith("0b"):
            base = 2   # Binary
            constant = constant[2:]
        elif constant[0] == "0":
            base = 8   # Octal
        else:
            return -1
        
        # Convert to decimal number.
        try:
            decimalValue = int(constant, base)
            if (decimalValue < 0):
                decimalValue = 127 - decimalValue
            if decimalValue < 256:
                return decimalValue
            else:
                # Too big.
                return -1
        except ValueError:
            return -1
    return -1

# Load the name file into the memory buffer.
def load_file(filename):
    global memory
    
    # Figure out the extension.
    ext = filename[filename.rindex(".")+1:len(filename)]
    if ext == "bin":
        # Assume binary file with 256 bytes.
        try:
            with open(filename, "rb") as binary_file:
                memory = binary_file.read(256)       
                binary_file.close()
        except:
            print(filename+" not found.")
            exit(1)
    else:
        # Assume text file with delimited entries for each byte.
        try:
            with open(filename, "r") as text_file:
                contents = text_file.read()
                text_file.close()
                values = re.split('\s|,|\.|:|;', contents)
                if len(values) > 256:
                    print(filename + " too many values.")
                    exit(1)
                memory_pos = 0
                for value in values:
                    decimal = get_decimal(value)
                    if decimal == -1:
                        print(filename + " invalid value " + value)
                        exit(1)
                    memory[memory_pos] = decimal
                    memory_pos += 1
        except:
            print(filename +" not found.")
            exit(1)      
        
# Get the file to disassemble from the command line.
args = parser.parse_args()
filename = args.filename

if filename == "":
    parser.error("-f FILE required")

# Set to True to print the opcode addresses at the beginning of each line.
showAddress = args.showAddress

# If true emit the disassembled code to standard out.
dumpResults = args.dumpResults

# If true emit the disassembled code to standard out.
saveResults = args.saveResults

if not dumpResults and not saveResults:
    parser.error("at least one of -s and -d required")

# Load the binary file into the memory buffer.
load_file(filename)

# Build a map that indicates what byte are code vs data. The strategy is to
# use the JMP instructions to determine the code blocks since the only way
# to get to code (aside from the first instruction) is to jump there.
inCode = True
checkByte = 4 # Default starting location for KENBAK programs.
while checkByte < 256:
    # If not in code skip to the next block of code.
    if inCode == False:
        if codemap[checkByte] == 1:
            inCode = True
        else:
            checkByte += 1
            continue
        
    opcode = determine_opcode(memory[checkByte])
    if opcode == "jmp":
        address = memory[checkByte+1]
        if address > checkByte:
            # Jumping forward to code so mark the destination address.
            codemap[address] = 1
        else:
            if (memory[checkByte] & 0b11000000) == 0b11000000:
                # Jumping back assume that this is the end of a code block.
                inCode = False
            else:
                # Conditional jump so keep going.
                codemap[address] = 1
    elif opcode == "jmk":
        address = memory[checkByte+1]
        if address > checkByte:
            # Jumping forward to code so mark the destination address skipping return byte.
            codemap[address+1] = 1
        else:
            if (memory[checkByte] & 0b11000000) == 0b11000000:
                # Jumping back assume that this is the end of a code block.
                inCode = False
            else:
                # Conditional jump so keep going.
                codemap[address+1] = 1
    elif opcode == "halt":
        if memory[checkByte+1] == 0:
            # Assume that two consecutive halt instruction means end of code.\
            inCode = False
    codemap[checkByte] = 1
    if opcode in single_byte_opcodes:
        checkByte += 1
    else:
        codemap[checkByte+1] = 1
        checkByte += 2
        
# Find all of the memory locations that have to be written to so that
# they can be marked with a db directive. First all of the registers.
for address in register_addresses:
    address = address
    codemap[address] = 2
    
checkByte = 4 # Default starting location for KENBAK programs.
while checkByte < 256:
    # Only interested in code sections.
    if codemap[checkByte] == 1:
        opcode = determine_opcode(memory[checkByte])
        
        if opcode == "store":
            address = memory[checkByte+1]
            if (memory[checkByte] & 0b000000111) == 0b00000100:
                # Memory.
                codemap[address] = 2
            elif (memory[checkByte] & 0b000000111) == 0b00000101 or (memory[checkByte] & 0b000000111) == 0b00000111:
                # Indirect.
                address = memory[address]
                codemap[address] = 2
        elif opcode == "jmk":
            address = memory[checkByte+1]
            if (memory[checkByte] & 0b00001000) == 0b00001000:
                # Indirect.
                address = memory[address]
            codemap[address] = 2
        elif opcode == "set":
            address = memory[checkByte+1]
            codemap[address] = 2
    if opcode in single_byte_opcodes:
        checkByte += 1
    else: 
        checkByte += 2
             
# Index into the memory buffer.
nextByte = 0
    
# Only want to process halt (0) if the last instruction net a halt.
lastWasInstruction = False

# Build a list of assembler instructions.
while nextByte < 256:
    
    # Format the address of the next opcode.
    address = str(nextByte).zfill(3)
    
    # Check for data.
    if codemap[nextByte] == 0:
        instruction = [address, "", str(memory[nextByte]), "", ""]
        instructions.append(instruction)
        nextByte += 1
    elif codemap[nextByte] == 2:
        # This is a writeable byte.
        instruction = [address, "", "db", "", ""]
        instructions.append(instruction)
        nextByte += 1
    else:
        # Convert the byte codes into instructions.
        opcode = determine_opcode(memory[nextByte])
        if opcode == "halt":
            if lastWasInstruction:
                instruction = [address, "", opcode, "", ""]
                instructions.append(instruction)
                lastWasInstruction = False
            nextByte += 1
        elif opcode == "nop":
            instruction = [address, "", opcode, "", ""]
            instructions.append(instruction)
            lastWasInstruction = True
            nextByte += 1  
        else:
            operand = determine_operand(opcode, memory[nextByte], memory[nextByte+1])
            if opcode in ["sft", "rot"]:
                op_address = ""
            else:
                op_address = str(memory[nextByte+1]).zfill(3)
            instruction = [address, "", opcode, operand, op_address]
            instructions.append(instruction)
            lastWasInstruction = True
            if opcode in ["sft", "rot"]:
                nextByte += 1
            else:
                nextByte += 2
                
# Add labels for address references.
for instruction in instructions:
    address = int(instruction[0])
    if address in register_addresses:
        instruction[1] = register_names[register_addresses.index(address)]
    else:
        op_address = instruction[4]
        if op_address != "" and not is_immediate(instruction[2], memory[address]):
            # Instruction has an address byte.
            label = "LAB" + op_address
            instruction[3] = instruction[3].replace(op_address, label)
            for add_label in instructions:
                if add_label[0] == op_address and add_label[1] == "":
                    add_label[1] = label
                    break
                
# Open a text file for writing the disassembly. Use the input file name with 
# a .asm extension.
outfilename = filename[0:filename.rindex(".")]+".asm"
outfile = open(outfilename,"w")

# Now save the instructions. Start with a header.
org_spaces = 10
addr_spaces = ""
if showAddress:
    addr_spaces = "     "
header = [addr_spaces+";", addr_spaces+"; Disassembly for ["+filename+"]", addr_spaces+";", addr_spaces+"          org     0"]
for line in header:
    if dumpResults:
        print(line)
    if saveResults:
        outfile.write(line+"\n")
# Now the generated instructions.
for instruction in instructions:
    if showAddress:
        address = instruction[0]+": "
    else:
        address = ""
    label = instruction[1] + ' ' * (10 - len(instruction[1]))
    opcode = instruction[2] + ' ' * (8 - len(instruction[2]))
    operand = instruction[3]
    line = address + label + opcode + operand
    
    if dumpResults:
        print(line)
    if saveResults:
        outfile.write(line+"\n")    
outfile.close()
sys.exit(0)
    