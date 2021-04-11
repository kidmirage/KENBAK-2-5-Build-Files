import tkinter.scrolledtext as tkscrolled
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import Font
import re

# Reserve space for the 256 byte memory of the KENBAK-1.
memory = bytearray(256)  # All bytes are initialized to null (zeros).

# Define the valid op codes.
opCodes = {"add","sub","load","store","and","or","lneg","jmp","jmk","skp","set","sft","rot","nop","halt","org"}

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Assembler Files", "*.asm"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_code.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_code.insert(tk.END, text)

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension="asm",
        filetypes=[("Assembler Files", "*.asm"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_code.get(1.0, tk.END)
        output_file.write(text)
    # Save the memory as binary. First change the extension.
    binFilePath = filepath.replace(".asm",".bin")
    with open(binFilePath, "wb") as output_file:
        output_file.write(memory)

def process_constant(constant):
    # Figure out the base
    if len(constant) > 0:
        if len(constant) == 2 and constant[0] == "'":
            return ord(constant[1])
        elif constant[0] in {'-','1','2','3','4','5','6','7','8','9'}:
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

def process_address(address):
    # Remove all white space from the address.
    pattern = re.compile(r'\s+')
    address = re.sub(pattern, '', address)
    
    # See if address contains +X indicating Indexed.
    indexed = address.find("+X")
    if indexed > 0:
        address = address[0:indexed]
       
    # See if the address is an immediate constant.
    immediate = process_constant(address)
    if immediate >= 0:
        addressMode = 0b011
        return addressMode, ""
    else:
        # See if the address contains () indicating Indirect.
        if address[0] == "(" and address[len(address)-1] == ")":
            label = address[1:len(address)-1]
            if indexed > 0:
                addressMode = 0b111
            else:
                addressMode = 0b101
        else:
            label = address
            if indexed > 0:
                addressMode = 0b110
            else:
                addressMode = 0b100
    return addressMode, label

def process_full_address_opcodes(opCode, operands, programCounter, labels):
    # There should be two operands.
    tokens = operands.split(",")
    if len(tokens) == 2 and len(tokens[1]) > 0:
        if opCode == "add":
            opValue = 0b00000000
        elif opCode == "sub":
            opValue = 0b00001000
        elif opCode == "load":
            opValue = 0b00010000
        elif opCode == "store":
            opValue = 0b00011000
        elif opCode == "and":
            opValue = 0b11010000
        elif opCode == "or":
            opValue = 0b11000000
        elif opCode == "lneg":
            opValue = 0b11011000
            
        register = tokens[0].upper()
        address = tokens[1].upper()
        
        # Make sure the register is valid for the operation.
        if not register in {"A","B","X"}:
            return "??????? ???", programCounter
        if opCode in {"and","or","lneg"} and not register == "A":
            return "??????? ???", programCounter
        
        # Add the appropriate register bits to the op value.
        if register in {"A","B","X"} and opCode in {"add","sub","load","store"}:
            if register == "A":
                opValue = opValue | 0b00000000
            elif register == "B":
                opValue = opValue | 0b01000000
            elif register == "X":
                opValue = opValue | 0b10000000
        
        # Add the appropriate address bits to the op value.
        addressMode, label = process_address(address)
        offset = 0;
        if "+" in label:
            parts = label.split("+")
            label = parts[0]
            offset = process_constant(parts[1])
            if (offset < 0):
                offset = 0;
        if addressMode >= 0:
            opValue = opValue | addressMode
            if addressMode == 3:
                # Immediate.
                addressValue = process_constant(address)
                address = f"{addressValue:03}"
            elif label in labels:
                # Lookup address.
                addressValue = labels[label]+offset
                address = f"{addressValue:03}"
            else:
                # Don't know yet.
                addressValue = 0
                address = "???"
            # Save the op code and address into memory.
            memory[programCounter] = opValue
            memory[programCounter+1] = addressValue
            
            return f"[{opValue:03o}|{opValue:02x}]".upper() + " " + address, programCounter+2
        else:
            return "??????? ???", programCounter 
    return "??????? ???", programCounter

def process_jump_opcodes(opCode, operands, programCounter, labels):
    # There should be three operands.
    tokens = operands.split(",")
    if len(tokens) == 1 or (len(tokens) == 3 and len(tokens[2]) > 0):
        
        # Get ready to parse the instruction
        opValue = 0b00100000
        
        if len(tokens) == 1:
            register = "A"
            comparison = "GLE"
            address = tokens[0].upper()
        else:
            register = tokens[0].upper()
            comparison = tokens[1].upper()
            address = tokens[2].upper()
        
        # Make sure the register and comparison are valid for the operation.
        if not register in {"A","B","X"}:
            return "??????? ???", programCounter
        if not comparison in {"NE","EQ","LT","GE","GT","GLE"}:
            return "??????? ???", programCounter
        
        # Is this a jump or a jump and mark.
        if opCode == "jmk":
            opValue = opValue | 0b00010000
            
        # Add the appropriate register bits to the op value.
        if comparison == "GLE":
            opValue = opValue | 0b11000000
        elif register == "A":
            opValue = opValue | 0b00000000
        elif register == "B":
            opValue = opValue | 0b01000000
        elif register == "X":
            opValue = opValue | 0b10000000
            
        # Add the appropriate conditional bits to the op value.
        if comparison == "NE":
            opValue = opValue | 0b00000011
        elif comparison == "EQ":
            opValue = opValue | 0b00000100
        elif comparison == "LT":
            opValue = opValue | 0b00000101
        elif comparison == "GE":
            opValue = opValue | 0b00000110
        elif comparison == "GT":
            opValue = opValue | 0b00000111
        elif comparison == "GLE":
            opValue = opValue | 0b00000111
            
        
        # Add the appropriate address bits to the op value.
        addressMode, label = process_address(address)
        offset = 0;
        if "+" in label:
            parts = label.split("+")
            label = parts[0]
            offset = process_constant(parts[1])
            if (offset < 0):
                offset = 0;
        if addressMode >= 0:
            # Only memory and indirect addressing modes are valid.
            if addressMode == 4 or addressMode == 5:
                if addressMode == 5:
                    # Indirect addressing. (Direct = 0).
                    opValue = opValue | 0b00001000
            else:
                return "??????? ???", programCounter
            
            # Find the label address.
            if label in labels:
                # Lookup address.
                addressValue = labels[label]+offset
                address = f"{addressValue:03}"
            else:
                # Don't know yet.
                addressValue = 0
                address = "???"
            
            # Save the op code and address into memory.
            memory[programCounter] = opValue
            memory[programCounter+1] = addressValue
            
            return f"[{opValue:03o}|{opValue:02x}]".upper() + " " + address, programCounter+2
        else:
            return "??????? ???", programCounter 
    return "??????? ???", programCounter

def process_skip_and_set_opcodes(opCode, operands, programCounter, labels):
    # There should be three operands.
    tokens = operands.split(",")
    if len(tokens) == 3 and len(tokens[2]) > 0:
        
        # Get ready to parse the instruction
        opValue = 0b00000010
        bitPosition = tokens[0]
        compareBit = tokens[1]
        address = tokens[2].upper()
        
        # Make sure the bit position and compare bit are valid for the operation.
        if not bitPosition in {"0","1","2","3","4","5","6","7"}:
            return "??????? ???", programCounter
        if not compareBit in {"0","1"}:
            return "??????? ???", programCounter
        
        # Is this a skip or a set.
        if opCode == "skp":
            opValue = opValue | 0b10000000
            
        # Add the appropriate position bits to the op value.
        opValue = opValue | (int(bitPosition)<<3)
        
        # Add the appropriate compare bit to the op value.
        opValue = opValue | (int(compareBit)<<6)
          
        # Add the appropriate address bits to the op value.
        addressMode, label = process_address(address)
        offset = 0;
        if "+" in label:
            parts = label.split("+")
            label = parts[0]
            offset = process_constant(parts[1])
            if (offset < 0):
                offset = 0;
        
        # Only memory addressing mode is valid.
        if addressMode == 4:
            # Find the label address.
            if label in labels:
                # Lookup address.
                addressValue = labels[label]+offset
                address = f"{addressValue:03}"
            else:
                # Don't know yet.
                addressValue = 0
                address = "???"
            
            # Save the op code and address into memory.
            memory[programCounter] = opValue
            memory[programCounter+1] = addressValue
            
            return f"[{opValue:03o}|{opValue:02x}]".upper() + " " + address, programCounter+2
        else:
            return "??????? ???", programCounter 
    return "??????? ???", programCounter

def process_shift_and_rotate_opcodes(opCode, operands, programCounter, labels):
    # There should be three operands.
    tokens = operands.split(",")
    if len(tokens) == 3 and len(tokens[2]) > 0:
        
        # Get ready to parse the instruction
        opValue = 0b00000001
        register = tokens[0].upper()
        direction = tokens[1].upper()
        amount = tokens[2]
        
        # Make sure the register, direction, and amount are valid for the operation.
        if not register in {"A","B"}:
            return "??????? ???", programCounter
        if not direction in {"L","R"}:
            return "???????", programCounter
        if not amount in {"1","2","3","4"}:
            return "???????", programCounter
        
        # Is this a shift or a rotate.
        if opCode == "rot":
            opValue = opValue | 0b01000000
            
        # Set register.
        if register == "B":
            opValue = opValue | 0b00100000
            
        # Set direction. 
        if direction == "L":
            opValue = opValue | 0b10000000
            
        # Set amount.
        opValue = opValue | (int(amount)%4)<<3
        
        # Save the op code into memory.
        memory[programCounter] = opValue
            
        return f"[{opValue:03o}|{opValue:02x}]".upper(), programCounter+1
    return "???????", programCounter

def process_opcode(opCode, operands, programCounter, labels):
    # Treat all op codes as lower case.
    opCode = opCode.lower()
    operands = operands.replace(" ", "")
    if opCode == "org":
        constant = process_constant(operands)
        if constant >= 0:
            return "", constant
    elif opCode in {"add","sub","load","store","and", "or","lneg"}:
        return process_full_address_opcodes(opCode, operands, programCounter, labels)
    elif opCode in {"jmp","jmk"}:
        return process_jump_opcodes(opCode, operands, programCounter, labels)
    elif opCode in {"skp","set"}:
        return process_skip_and_set_opcodes(opCode, operands, programCounter, labels)
    elif opCode in {"sft","rot"}:
        return process_shift_and_rotate_opcodes(opCode, operands, programCounter, labels)
    return "", programCounter

def process_line(line, programCounter, labels):
    # Remove any comments.
    line = line.upper().split(";",1)[0]
    
    # Split the line into space separated tokens.
    tokens = line.split()
    
    # See if there is a label.
    if len(tokens) > 0 and line[0].isalpha():
        label = tokens[0]
        labels[label] = programCounter
        tokens.remove(label)
    
    # See if there is an op code.
    if len(tokens) > 0:
        if tokens[0].lower() in opCodes:
            opCode = tokens[0].lower()
            if len(tokens) > 1:
                # 2 byte instruction.
                operands = tokens[1]
                # Concatenate removing spaces.
                for i in range(2, len(tokens)):
                    operands = operands + tokens[i]
                return process_opcode(opCode, operands, programCounter, labels)
            else:
                # Must be nop or halt.
                if opCode == "nop":
                    # Save the op code into memory.
                    memory[programCounter] = 0b10000000
                    return "[200|80]", programCounter+1
                elif opCode == "halt":
                    # Save the op code into memory.
                    memory[programCounter] = 0b00000000
                    return "[000|00]", programCounter+1
                else:
                    # org with no integer constant
                    return "", programCounter
        else:
            # Must be an integer constant.
            decimalValue = process_constant(tokens[0])
            if decimalValue >= 0:
                memory[programCounter] = decimalValue
                return f"{decimalValue:03}", programCounter+1
            else:
                return "???", programCounter
    return "", programCounter
    
def assemble_line(line, programCounter, labels):
    showCounter = programCounter
    processed,programCounter = process_line(line, programCounter, labels)
    if processed != "":
        assembled = f"{showCounter:03}" + ": " + processed
    else:
        assembled = ""
    return assembled, programCounter

def process_lines(lineList, labels, programCounter):
    assembly = []
    unresolvedLabels = False
    for line in lineList:
        # Process line
        if line:
            assembled_line, programCounter = assemble_line(line, programCounter, labels)
            if " ???" in assembled_line:
                unresolvedLabels = True
            assembly.append(assembled_line)
        else:
            assembly.append("")
    return assembly, unresolvedLabels

def assemble_code(code, programCounter):
    lineList = code.split('\n')
    
    # Pre fill with default labels for special memory locations.
    labels = dict()
    labels["A"] = 0             # A register.
    labels["B"] = 1             # B register.
    labels["X"] = 2             # C register.
    labels["PC"] = 3            # Program counter.
    labels["OUTPUT"] = 128      # Maps to front panel data display lamps.
    labels["OCA"] = 129         # Overeflow/Carry bits for A register.
    labels["OCB"] = 130         # Overeflow/Carry bits for B register.
    labels["OCX"] = 131         # Overeflow/Carry bits for X register.
    labels["INPUT"] = 255       # Maps to the front panel data input buttons.
    
    assembly, unresolvedLabels = process_lines(lineList, labels, programCounter)
    if unresolvedLabels:
        # Try one more time to process later binding labels.
        assembly, unresolvedLabels = process_lines(lineList, labels, programCounter)
    return assembly

class TextAssembly(tk.Canvas):
        
    def __init__(self, textwidget, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = textwidget
        self.configure(width=16, state="disabled", background="light grey")
        self.redraw()

    def redraw(self):
        # Redraw all of the assembled instructions in the visible part of the text window.
        self.delete("all")
        
        # Get all of the text in the code window as a list of lines.
        programCounter = 4
        assembledLines = assemble_code(self.textwidget.get(1.0, tk.END), programCounter)

        # Find the first visible line.
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            lineindex = int(linenum)-1
            self.create_text(5,y,anchor="nw", font=('Courier',14,'bold'), text=assembledLines[lineindex])
            i = self.textwidget.index("%s+1line" % i)

        # Refreshes the canvas widget 30fps
        self.after(30, self.redraw)

window = tk.Tk()
window.title("Kenbak-1 Assembler")
window.rowconfigure(0, minsize=10, weight=1)
window.rowconfigure(1, minsize=700, weight=1)
window.columnconfigure(0, minsize=200, weight=0)
window.columnconfigure(1, minsize=500, weight=1)

codeFont = Font(family="Courier", size=14)
buttonFont = Font(family="Arial", size=12)

txt_code = tkscrolled.ScrolledText(window, font=codeFont, undo=True, autoseparators=True, maxundo=-1, borderwidth=2)
txt_code.configure(width=80, state="normal", wrap="none")
txt_assembled = TextAssembly(txt_code)

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_load = tk.Button(fr_buttons, font=buttonFont, text="Load", command=open_file)
btn_save = tk.Button(fr_buttons, font=buttonFont, text="Save As...", command=save_file)

btn_load.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=0, column=1, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, columnspan="2", sticky="ew")
txt_assembled.grid(row=1, column=0, sticky="nsew")
txt_code.grid(row=1, column=1, sticky="nsew")
window.mainloop()