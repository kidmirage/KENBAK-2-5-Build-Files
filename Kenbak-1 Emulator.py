import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

# Reserve space for the 256 byte memory of the KENBAK-1.
memory = bytearray(256)  # All bytes are initialized to null (zeros).

# Define the special memory locations.
A = 0           # Registers.
B = 1
X = 2
PC = 3          # Program counter points to the next instruction to execute.
OUTPUT = 128    # Maps to front panel data display lamps.
OCA = 129       # Overeflow/Carry bits for A register.
OCB = 130       # Overeflow/Carry bits for B register.
OCX = 131       # Overeflow/Carry bits for X register.
INPUT = 255     # Maps to the front panel data input buttons.

# Define flags register bits.
CARRY = 0b00000010
OVERFLOW = 0b00000001
SIGN = 0b10000000

# Load a memory image from file.
def open_file():
    global memory
    
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Binary Files", "*.bin")]
    )
    if not filepath:
        return
    with open(filepath, "rb") as input_file:
        memoryBytes = input_file.read()
        memory = bytearray(memoryBytes)
        
    # Initialize the instruction pointer to the default.
    memory[PC] = 4
    
    # Show the result on screen.
    draw_state()
    
# Draw the the current state of the program memory.
def draw_state():
    global special_canvas
    global dump_canvas
    
    HEX_DUMP_X = 20
    HEX_DUMP_Y = 10
    BYTE_X = BYTE_Y = 25
    SPECIAL_X = 10
    SPECIAL_Y = 10

    # Show the registers and special memory addresses.
    special_canvas.delete("all")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y, font="Courier", anchor=tk.W, text=f"A:    {memory[0]:02x}|{memory[0]:03o}|{memory[0]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y, font="Courier", anchor=tk.W, text=f"B:    {memory[1]:02x}|{memory[1]:03o}|{memory[1]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*2, font="Courier", anchor=tk.W, text=f"X:    {memory[2]:02x}|{memory[2]:03o}|{memory[2]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*3, font="Courier", anchor=tk.W, text=f"PC:   {memory[3]:02x}|{memory[3]:03o}|{memory[3]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*4, font="Courier", anchor=tk.W, text=f"OUT:  {memory[128]:02x}|{memory[128]:03o}|{memory[128]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*5, font="Courier", anchor=tk.W, text=f"OCA:  {memory[129]:02x}|{memory[129]:03o}|{memory[129]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*6, font="Courier", anchor=tk.W, text=f"OCB:  {memory[130]:02x}|{memory[130]:03o}|{memory[130]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*7, font="Courier", anchor=tk.W, text=f"OCX:  {memory[131]:02x}|{memory[131]:03o}|{memory[131]:08b}")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*8, font="Courier", anchor=tk.W, text=f"IN:   {memory[255]:02x}|{memory[255]:03o}|{memory[255]:08b}")
    
    # Dump the memory locations.
    dump_canvas.delete("all")
    for row in range(16):
        dump_canvas.create_text(HEX_DUMP_X, HEX_DUMP_Y+row*BYTE_Y, font="Courier", text=f"{row*16:02x}:".upper())
        for col in range(16):
            dump_canvas.create_text(HEX_DUMP_X+(col+1)*BYTE_X+5, HEX_DUMP_Y+row*BYTE_Y, font="Courier", text=f"{memory[row*16+col]:02x}".upper())
    
# Based on the current op code and program counter fetch and return
# the operand address. This call applies to all instructions that
# support the five basic addressing modes: add, sub, load, store,
# and, or, lneg.
def get_address():
    opCode = memory[memory[PC]]
    addressingMode = opCode & 0b00000111
    if addressingMode == 0b011:
        # Immediate.
        return PC+1
    elif addressingMode == 0b100:
        # Memory.
        return memory[PC+1]
    elif addressingMode == 0b101:
        # Indirect.
        return memory[memory[PC+1]]
    elif addressingMode == 0b110:
        # Indexed.
        return memory[PC+1]+memory[X]
    elif addressingMode == 0b111:
        # Indirect Indexed
        return memory[memory[PC+1]]+memory[X]
    else:
        # Error. Should not happen.
        return 0
    
# Based on the current op code and program counter fetch and return
# the operand value. This call applies to all instructions that
# support the five basic addressing modes: add, sub, load, store,
# and, or, lneg.
def get_operand():
    return memory[get_address()]

# Based on the current op code and program counter store the
# operand value passed. This call applies to all instructions that
# support the five basic addressing modes: add, sub, load, store,
# and, or, lneg.
def set_operand(operand):
    memory[get_address()] = operand

# Return true if the current jump op code condition is met.
def check_for_jump():
    opCode = memory[memory[PC]]
    
    # Determine what register to check or for unconditional.
    register = (opCode & 0b11000000) >> 6
     
    # Check for jump true.
    if register == 3:
        # Unconditional.
        return True
    else:
        # Get the condition to check.
        condition = opCode & 0b00000111
        if condition == 3 and memory[register] & 0b11111111  > 0:
            # Non-zero.
            return True
        elif condition == 4 and memory[register] & 0b11111111 == 0:
            # Zero.
            return True
        elif condition == 5 and memory[register] & 0b10000000:
            # Negative.
            return True
        elif condition == 6 and memory[register] & 0b10000000 == 0:
            # Positive.
            return True
        elif condition == 7 and memory[register] & 0b10000000 == 0 & memory[register] & 0b01111111:
            # Positive Non-zero.
            return True
    # Condition not met.
    return False
        
# Process the single byte rotate instruction.
def process_rot():
    opCode = memory[memory[PC]]
    
    # A or B register.
    if opCode & 0b00100000:
        value = memory[B]
    else:
        value = memory[A]
        
    # Number of rotations (1-4)
    rotations = (opCode & 0b00011000) >> 3
    if rotations == 0:
        rotations = 4
        
    # Left or right shift.
    if opCode & 0b10000000:
        # Left. 
        keep = (value & 0b11110000) >> (8 - rotations)
        value = (value << rotations & 0b11111111) | keep
    else:
        # Righ
        keep = ((value & 0b00001111) << (8 - rotations)) & 0b11111111
        value = (value >> rotations) | keep
        
    # A or B register.
    if opCode & 0b00100000:
        memory[B] = value
    else:
        memory[A] = value
    
    # Advance to next instruction.
    memory[PC] += 1
    
# Process the single byte shift instruction.
def process_sft():
    opCode = memory[memory[PC]]
    
    # A or B register.
    if opCode & 0b00100000:
        value = memory[B]
    else:
        value = memory[A]

    # Number of shifts (1-4)
    shifts = (opCode & 0b00011000) >> 3
    if shifts == 0:
        shifts = 4
        
    # Left or right shift.
    if opCode & 0b10000000:
        # Left.
        value = (value << shifts) & 0b11111111
    else:
        # Right
        value = value >> shifts
       
    # A or B register.
    if opCode & 0b00100000:
        memory[B] = value
    else:
        memory[A] = value
    
    # Advance to next instruction.
    memory[PC] += 1
    
# Process the two byte skip instruction.
def process_skp():
    opCode = memory[memory[PC]]
    
    # Get the value that will be used to check for a skip.
    checkByte = memory[memory[PC+1]]
    
    # Set a bit in the position that we are interested in.
    position = (opCode & 0b00111000) >> 3
    checkBit = 0b00000001 << position
    
    # Check based on skip on zero or skip on one.
    if opCode & 0b01000000:
        # Skip on 1.
        if checkByte & checkBit:
            # Bit set so skip over two extra bytes.
            memory[PC] += 2
    else:
        # Skip on 0.
        if checkByte & checkBit == 0:
            # Bit not set so skip over two extra bytes.
            memory[PC] += 2
    
    # Advance to next instruction.   
    memory[PC] += 2
    
# Process the two byte set instruction.
def process_set():
    opCode = memory[memory[PC]]
    
    # Get the value that will be updated.
    updateByte = memory[memory[PC+1]]
    
    # Set a bit in the position that we are interested in.
    position = (opCode & 0b00111000) >> 3
    updateBit = 0b00000001 << position
    
    # Update based on set zero or set one.
    if opCode & 0b01000000:
        # Set to 1.
        updateByte |= updateBit
    else:
        # Set to 0.
        updateByte &= (updateBit ^ 0b11111111)
        
    # Replace with the updated value.
    memory[memory[PC+1]] = updateByte
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte load negative instruction.
def process_lneg():
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Load A register with the arithmetic compliment of the operand.
    if operand == 0b1000000:
        # Special case for -128.
        memory[A] = operand
    else:
        memory[A] = operand ^ 0b11111111
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte or instruction.
def process_or(): 
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Logically OR the A register with the operand value.
    memory[A] |= operand 
    
    # Advance to next instruction.
    memory[PC] += 2

# Process the two byte and instruction.
def process_and():
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Logically AND the A register with the operand value.
    memory[A] &= operand 
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte store instruction.
def process_store():
    opCode = memory[memory[PC]]
    
    # Determine what register to store.
    register = (opCode & 0b11000000) >> 6
    
    # Save the appropriate register with to the appropriate address.
    set_operand(memory[register])
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte load instruction.
def process_load():
    opCode = memory[memory[PC]]
    
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Determine what register to load.
    register = (opCode & 0b11000000) >> 6
    
    # Load the appropriate register with the operand value.
    memory[register] = operand
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte subtract instruction.
def process_sub():
    opCode = memory[memory[PC]]
    
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Determine what register to update.
    register = (opCode & 0b11000000) >> 6
    
    # Clear the flags register.
    memory[OCA+register] = 0
    
    # Check for carry condition.
    if memory[register] < operand:
        memory[OCA+register] |= CARRY
    
    # Check for overflow condition.
    op1Sign = memory[register] & SIGN
    op2Sign = operand & SIGN
    ansSign = (memory[register] - operand) & SIGN
    if (op1Sign != op2Sign) and ansSign != op1Sign:
        memory[OCA+register] |= OVERFLOW
    
    # Perform the subtraction.
    memory[register] -= operand
    
    # Advance to next instruction.
    memory[PC] += 2
    
# Process the two byte add instruction.
def process_add():
    opCode = memory[memory[PC]]
    
    # Get the value of the operand based on the addressing mode of the instruction.
    operand = get_operand()
    
    # Determine what register to update.
    register = (opCode & 0b11000000) >> 6
    
    # Clear the flags register.
    memory[OCA+register] = 0
    
    # Check for carry condition.
    if (memory[register] + operand) > 255:
        memory[OCA+register] |= CARRY
    
    # Check for overflow condition.
    op1Sign = memory[register] & SIGN
    op2Sign = operand & SIGN
    ansSign = (memory[register] + operand) & SIGN
    if (op1Sign == op2Sign) and ansSign != op1Sign:
        memory[OCA+register] |= OVERFLOW
    
    # Perform the addition.
    memory[register] += operand
    
    # Advance to next instruction.
    memory[PC] += 2
    
        
# Process the two byte jump and mark instruction.
def process_jmk():
    opCode = memory[memory[PC]]
    
    # Get the target address.
    address = memory[PC+1]    # Direct address.
    if opCode & 0b00001000:
        # Indirect address.
        address = memory[address]
    
    # Perform the jump if the condition is met.
    if check_for_jump():
        # Save the address of the next instruction at the destination address.
        memory[address] = memory[PC] + 2
        memory[PC] = address + 1
    else:
        # Just advance to next instruction.
        memory[PC] += 2
    
# Process the two byte jump instruction.
def process_jmp():
    opCode = memory[memory[PC]]
    
    # Get the target address.
    address = memory[PC+1]    # Direct address.
    if opCode & 0b00001000:
        # Indirect address.
        address = memory[address]
    
    # Perform the jump if the condition is met.
    if check_for_jump():
        memory[PC] = address
    else:
        # Just advance to next instruction.
        memory[PC] += 2
        
def perform_next_instruction():
   
    # Next instruction.
    opCode = memory[memory[PC]]
    
    # Figure out what instruction the op code represents.
    if opCode & 0b00000111 == 0b00000000:
        if opCode & 0b10000000:
            # NOP. Just skip to the next instruction.
            memory[PC] += 1
        else:
            # HALT. Stop the program.
            return False
    elif opCode & 0b00000111 == 0b00000001:
        if opCode & 0b01000000:
            # ROT.
            process_rot()
        else:
            # SFT.
            process_sft()
    elif opCode & 0b00000111 == 0b00000010:
        if opCode & 0b10000000:
            # SKP.
            process_skp()
        else:
            # SET.
            process_set()
    elif opCode & 0b11111000 == 0b11011000:
        # LNEG.
        process_lneg()
    elif opCode & 0b11111000 == 0b11000000:
        # OR.
        process_or()
    elif opCode & 0b11111000 == 0b11010000:
        # AND.
        process_and()
    elif opCode & 0b00111000 == 0b00011000:
        # STORE.
        process_store()
    elif opCode & 0b00111000 == 0b00010000:
        # LOAD.
        process_load()
    elif opCode & 0b00111000 == 0b00001000:
        # SUB.
        process_sub()
    elif opCode & 0b00111000 == 0b00000000:
        # ADD.
        process_add()
    elif opCode & 0b00100000 == 0b00100000:
        if opCode & 0b00010000:
            # JMK.
            process_jmk()
        else:
            # JMP.
            process_jmp()
    else:
        # Error.
        return False
    return True

def run_program():
    global memory
    
    # Initialize the instruction pointer to the default.
    memory[PC] = 4

    # Run the program.
    while perform_next_instruction():
        draw_state()
    
# Perform the next step in the loaded program.
def step_program():
    perform_next_instruction()
    draw_state()

# Setup the working window.
window = tk.Tk()
window.title("Kenbak-1 Emulator")
window.rowconfigure(0, minsize=10)
window.rowconfigure(1, minsize=500, weight=1)
window.columnconfigure(0, minsize=100, weight=0)
window.columnconfigure(1, minsize=450, weight=10)

codeFont = Font(family="Courier", size=14)

special_canvas = tk.Canvas(window, width=220, bg="light gray", bd=2)
dump_canvas = tk.Canvas(window, bg="white", bd=2)

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_run = tk.Button(fr_buttons, text="Run", command=run_program)
btn_step = tk.Button(fr_buttons, text="Step", command=step_program)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_run.grid(row=0, column=1, sticky="ew", padx=5)
btn_step.grid(row=0, column=2, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, columnspan="2", sticky="ew")
special_canvas.grid(row=1, column=0, sticky="nsew")
dump_canvas.grid(row=1, column=1, sticky="nsew")
window.mainloop()
    
