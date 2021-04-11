import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import tkinter.scrolledtext as tkscrolled

# Reserve space for the 256 byte memory of the KENBAK-1.
memory = bytearray(256)  # All bytes are initialized to null (zeros).
restart = bytearray(256)  # All bytes are initialized to null (zeros).

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

# Auto run flag.
autoRun = False

# Load a memory image from file.
def open_file():
    global memory
    global restart
    
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Binary Files", "*.bin")]
    )
    if not filepath:
        return
    with open(filepath, "rb") as input_file:
        memoryBytes = input_file.read()
        memory = bytearray(memoryBytes)
        restart = bytearray(memoryBytes)
        
    # Initialize the instruction pointer to the default.
    memory[PC] = 4
    
    # Show the result on screen.
    draw_state()
    
# Return a string with the hex, digital, octal, and binary representations of 
# the 8-bit memory number who's location is passed.
def show_number(index):
    value = memory[index]
    return f"{value:02x}|{value:03}|{value:03o}|{value:08b}".upper()
    
# Draw the the current state of the program memory.
def draw_state():
    global special_canvas
    global dump_canvas
    global memory_details
    
    HEX_DUMP_X = 30
    HEX_DUMP_Y = 15
    BYTE_X = 27
    BYTE_Y = 25
    SPECIAL_X = 10
    SPECIAL_Y = 15

    # Show the registers and special memory addresses.
    special_canvas.delete("all")
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y, font=('Courier',14,'bold'), anchor=tk.W, text=f"A:    " + show_number(0))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y, font=('Courier',14,'bold'), anchor=tk.W, text=f"B:    " + show_number(1))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*2, font=('Courier',14,'bold'), anchor=tk.W, text=f"X:    " + show_number(2))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*3, font=('Courier',14,'bold'), anchor=tk.W, text=f"PC:   " + show_number(3))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*4, font=('Courier',14,'bold'), anchor=tk.W, text=f"OUT:  " + show_number(128))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*5, font=('Courier',14,'bold'), anchor=tk.W, text=f"OCA:  " + show_number(129))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*6, font=('Courier',14,'bold'), anchor=tk.W, text=f"OCB:  " + show_number(130))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*7, font=('Courier',14,'bold'), anchor=tk.W, text=f"OCX:  " + show_number(131))
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*8, font=('Courier',14,'bold'), anchor=tk.W, text=f"IN:   " + show_number(255))
    
    # Dump the memory locations.
    dump_canvas.delete("all")
    for row in range(16):
        dump_canvas.create_text(HEX_DUMP_X, HEX_DUMP_Y+row*BYTE_Y, font=('Courier',14,'bold'), text=f"{row*16:02x}: ".upper())
        for col in range(16):
            fillColor = "black"
            if row*16+col == memory[PC]:
                fillColor = "red"
            dump_canvas.create_text(HEX_DUMP_X+(col+1)*BYTE_X+5, HEX_DUMP_Y+row*BYTE_Y, fill=fillColor, font=('Courier',14,'bold'), text=f"{memory[row*16+col]:02x}".upper())
    
    # Dump the memory details.
    memory_details.delete('1.0',tk.END)
    for i in range(256):
        if i == memory[PC]:
            memory_details.insert(tk.END, f" {i:02x}: " + show_number(i)+ "\n", 'PC')
        else:
            memory_details.insert(tk.END, f" {i:02x}: " + show_number(i)+ "\n")
             
# Based on the current op code and program counter fetch and return
# the operand address. This call applies to all instructions that
# support the five basic addressing modes: add, sub, load, store,
# and, or, lneg.
def get_address():
    opCode = memory[memory[PC]]
    operand = memory[memory[PC]+1]
    
    addressingMode = opCode & 0b00000111
    if addressingMode == 0b011:
        # Immediate.
        address = memory[PC]+1
    elif addressingMode == 0b100:
        # Memory.
        address = operand
    elif addressingMode == 0b101:
        # Indirect.
        address = memory[operand]
    elif addressingMode == 0b110:
        # Indexed.
        address = operand+memory[X]
    elif addressingMode == 0b111:
        # Indirect Indexed
        address = memory[operand]+memory[X]
    else:
        # Error. Should not happen.
        address = 0
        
    return address

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
    checkByte = memory[memory[memory[PC+1]]]
    
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
    
    # Get the address based on the ] addressing mode of the instruction.
    address = get_address()
    
    # Determine what register to store.
    register = (opCode & 0b11000000) >> 6
    
    # Save the register contents to the appropriate address.
    memory[address] = memory[register]
    
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
    memory[register] = (memory[register] + operand) & 0b11111111
    
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
    address = memory[memory[PC]+1]    # Direct address.
    if opCode & 0b00001000:
        # Indirect address.
        address = memory[address]
    
    # Perform the jump if the condition is met.
    if check_for_jump():
        memory[PC] = address
    else:
        # Just advance to next instruction.
        memory[PC] += 2

# Execute the instruction the the PC register points to.        
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

# Run the program at full speed.
def run_program():
    global memory
    global run
    global autoRun
    global singleStep
    
    # Initialize the instruction pointer to the default.
    memory[PC] = 4

    # Set the running mode.
    run = True
    autoRun = False
    singleStep = False
    
# Run the program at full speed.
def restart_program():
    global memory
    global restart
    
    # Stop all program activity.
    stop_program()
    
    # Replace memory with a fresh copy from the load.
    memory[:] = restart
    
    # Initialize the instruction pointer to the default.
    memory[PC] = 4
    
    # Refresh the screen.
    draw_state()


# Run the program at about one instruction per second.       
def auto_run_program():
    global autoRun
    global nextStepTime
    global run
    global singleStep
    
    # Set the running mode.
    autoRun = True
    run = False
    singleStep = False
    
    # Set the time for the next instruction to run at.
    nextStepTime = int(time.time() * 1000) + 1000
        
    
# Perform the next step in the loaded program.
def step_program():
    global singleStep
    global autoRun
    global run

    # Set the running mode.
    singleStep = True
    autoRun = False
    run = False

# Stop the currently running program.  
def stop_program():
    global run
    global autoRun
    global singleStep
    
    run = False
    autoRun = False
    singleStep = False
    
# Control the behavior of the program.
singleStep = False
autoRun = False
run = False
nextStepTime = 0

# Setup the working window.
window = tk.Tk()
window.title("Kenbak-1 Emulator")
window.rowconfigure(0, minsize=10)
window.rowconfigure(1, minsize=500, weight=1)
window.columnconfigure(0, minsize=100, weight=0)
window.columnconfigure(1, minsize=485, weight=1)
window.columnconfigure(2, minsize=100, weight=0)

buttonFont = Font(family="Arial", size=12)

special_canvas = tk.Canvas(window, width=290, bg="light gray")
dump_canvas = tk.Canvas(window, bg="white")
memory_details = tkscrolled.ScrolledText(window, font=('Courier',14,'bold'))
memory_details.configure(width=25, state="normal", wrap="none")
memory_details.tag_config('PC', background="white", foreground="red")

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
btn_load = tk.Button(fr_buttons, font=buttonFont, text="Load", command=open_file)
btn_restart = tk.Button(fr_buttons, font=buttonFont, text="Restart", command=restart_program)
btn_run = tk.Button(fr_buttons, font=buttonFont, text="Run", command=run_program)
btn_auto = tk.Button(fr_buttons, font=buttonFont, text="Auto", command=auto_run_program)
btn_step = tk.Button(fr_buttons, font=buttonFont, text="Step", command=step_program)
btn_stop = tk.Button(fr_buttons,  font=buttonFont,text="Stop", command=stop_program)

btn_load.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_restart.grid(row=0, column=1, sticky="ew", padx=5)
btn_run.grid(row=0, column=2, sticky="ew", padx=5)
btn_auto.grid(row=0, column=3, sticky="ew", padx=5)
btn_step.grid(row=0, column=4, sticky="ew", padx=5)
btn_stop.grid(row=0, column=5, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, columnspan="3", sticky="ew")
special_canvas.grid(row=1, column=0, sticky="nsew")
dump_canvas.grid(row=1, column=1, sticky="nsew")
memory_details.grid(row=1, column=2, sticky="nsew")

# The main loop of the program.
while True:
    
    # Check to see if we want to run the next step of the program.
    if singleStep or run or (autoRun and int(time.time() * 1000) > nextStepTime):
        if perform_next_instruction() == False:
            # Halt encountered.
            stop_program()
        draw_state()
        singleStep = False
        nextStepTime = int(time.time() * 1000) + 1000
    
    window.update_idletasks()
    window.update()
    
    

