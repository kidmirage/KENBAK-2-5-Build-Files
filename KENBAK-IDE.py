import time
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import Font
import tkinter.scrolledtext as tkscrolled
from time import sleep
import re

try:
    import wiringpi as wiringpi
    wiringPiLoaded = True
except:
    wiringPiLoaded = False
    

# Set the base number of ic1.
ic1_pin_base = 65
# Pin number to code number:
# 1 = 65, 2 = 66, 3 = 67, 4 = 68, 5 = 69, 6 = 70, 7 = 71, 8 = 72, 9 = 73, 10 = 74, 11 = 75, 12 = 76, 13 = 77, 14 = 78, 15 = 79, 16 = 80

# Define the i2c address of ic1.
ic1_i2c_addr = 0x24

# Set the base number of ic2.
ic2_pin_base = 81
# Pin number to code number:
# 1 = 81, 2 = 82, 3 = 83, 4 = 84, 5 = 85, 6 = 86, 7 = 87, 8 = 88, 9 = 89, 10 = 90, 11 = 91, 12 = 92, 13 = 93, 14 = 94, 15 = 95, 16 = 96

# Define the i2c address of ic2.
ic2_i2c_addr = 0x20

if wiringPiLoaded:
    # Initialize the wiringpi library.
    wiringpi.wiringPiSetup()
    
    # Enable ic1 on the mcp23017 hat.
    wiringpi.mcp23017Setup(ic1_pin_base,ic1_i2c_addr)
    
    # Enable ic2 on the mcp23017 hat.
    wiringpi.mcp23017Setup(ic2_pin_base,ic2_i2c_addr)

# Define LED pins.
light_stop = 65
light_store = 66
light_set = 67
light_clear = 68

light_0 = 73
light_1 = 74
light_2 = 75
light_3 = 76
light_4 = 77
light_5 = 78
light_6 = 79
light_7 = 80

# Define toggle pins.
toggle_off = 69
toggle_on = 70
toggle_unl = 71
toggle_lock = 72

# Define button pins
button_stop = 81
button_start = 82
button_store = 83
button_read = 84
button_set = 85
button_display = 86
button_clear = 87 

button_0 = 89
button_1 = 90
button_2 = 91
button_3 = 92
button_4 = 93
button_5 = 94
button_6 = 95
button_7 = 96

if wiringPiLoaded:
    # Set the pin mode to output for all the LEDs.
    wiringpi.pinMode(light_stop,1)
    wiringpi.pinMode(light_store,1)
    wiringpi.pinMode(light_set,1)
    wiringpi.pinMode(light_clear,1)
    wiringpi.pinMode(light_0,1)
    wiringpi.pinMode(light_1,1)
    wiringpi.pinMode(light_2,1)
    wiringpi.pinMode(light_3,1)
    wiringpi.pinMode(light_4,1)
    wiringpi.pinMode(light_5,1)
    wiringpi.pinMode(light_6,1)
    wiringpi.pinMode(light_7,1)
    
    # Set all the LEDs off to start with.
    wiringpi.digitalWrite(light_stop,0)
    wiringpi.digitalWrite(light_store,0)
    wiringpi.digitalWrite(light_set,0)
    wiringpi.digitalWrite(light_clear,0)
    wiringpi.digitalWrite(light_0,0)
    wiringpi.digitalWrite(light_1,0)
    wiringpi.digitalWrite(light_2,0)
    wiringpi.digitalWrite(light_3,0)
    wiringpi.digitalWrite(light_4,0)
    wiringpi.digitalWrite(light_5,0)
    wiringpi.digitalWrite(light_6,0)
    wiringpi.digitalWrite(light_7,0)
    
    
    # Set the pin mode to input for all the switches and buttons.
    wiringpi.pinMode(toggle_off,0)
    wiringpi.pinMode(toggle_on,0)
    wiringpi.pinMode(toggle_lock,0)
    wiringpi.pinMode(toggle_unl,0)
    
    wiringpi.pinMode(button_stop,0)
    wiringpi.pinMode(button_start,0)
    wiringpi.pinMode(button_store,0)
    wiringpi.pinMode(button_read,0)
    wiringpi.pinMode(button_set,0)
    wiringpi.pinMode(button_display,0)
    wiringpi.pinMode(button_clear,0)
    wiringpi.pinMode(button_0,0)
    wiringpi.pinMode(button_1,0)
    wiringpi.pinMode(button_2,0)
    wiringpi.pinMode(button_3,0)
    wiringpi.pinMode(button_4,0)
    wiringpi.pinMode(button_5,0)
    wiringpi.pinMode(button_6,0)
    wiringpi.pinMode(button_7,0)
    
    # Enable the internal pull-ups on all the inputs.
    wiringpi.pullUpDnControl(toggle_off,2)
    wiringpi.pullUpDnControl(toggle_on,2)
    wiringpi.pullUpDnControl(toggle_lock,2)
    wiringpi.pullUpDnControl(toggle_unl,2)
    
    wiringpi.pullUpDnControl(button_stop,2)
    wiringpi.pullUpDnControl(button_start,2)
    wiringpi.pullUpDnControl(button_store,2)
    wiringpi.pullUpDnControl(button_read,2)
    wiringpi.pullUpDnControl(button_set,2)
    wiringpi.pullUpDnControl(button_display,2)
    wiringpi.pullUpDnControl(button_clear,2)
    wiringpi.pullUpDnControl(button_0,2)
    wiringpi.pullUpDnControl(button_1,2)
    wiringpi.pullUpDnControl(button_2,2)
    wiringpi.pullUpDnControl(button_3,2)
    wiringpi.pullUpDnControl(button_4,2)
    wiringpi.pullUpDnControl(button_5,2)
    wiringpi.pullUpDnControl(button_6,2)
    wiringpi.pullUpDnControl(button_7,2)

# Update the console data lamps based on the bits passed
def show_data_lamps(bits):
    if wiringPiLoaded:
        if bits & 0b00000001:
            wiringpi.digitalWrite(light_0,1)
        else:
            wiringpi.digitalWrite(light_0,0)
        if bits & 0b00000010:
            wiringpi.digitalWrite(light_1,1)
        else:
            wiringpi.digitalWrite(light_1,0)
        if bits & 0b00000100:
            wiringpi.digitalWrite(light_2,1)
        else:
            wiringpi.digitalWrite(light_2,0)
        if bits & 0b00001000:
            wiringpi.digitalWrite(light_3,1)
        else:
            wiringpi.digitalWrite(light_3,0)
        if bits & 0b00010000:
            wiringpi.digitalWrite(light_4,1)
        else:
            wiringpi.digitalWrite(light_4,0)
        if bits & 0b00100000:
            wiringpi.digitalWrite(light_5,1)
        else:
            wiringpi.digitalWrite(light_5,0)
        if bits & 0b01000000:
            wiringpi.digitalWrite(light_6,1)
        else:
            wiringpi.digitalWrite(light_6,0)
        if bits & 0b10000000:
            wiringpi.digitalWrite(light_7,1)
        else:
            wiringpi.digitalWrite(light_7,0)
        
# Debounce the button passed.
def debounceButton(button):
    if wiringPiLoaded:
        while not wiringpi.digitalRead(button):
            # Wait a bit.
            sleep(.01)
        
        
def open_file():
    global memory
    global restart
    
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
        
    # Load the memory as binary. First change the extension.
    binFilePath = filepath.replace(".asm",".bin")
    with open(binFilePath, "rb") as binary_file:
        memoryBytes = binary_file.read()
        memory = bytearray(memoryBytes)
        restart = bytearray(memoryBytes)
        
    # Initialize the instruction pointer to the default.
    memory[PC] = 4

def save_file():
    global memory
    global restart
    
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".asm",
        filetypes=[("Assembler Files", "*.asm"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_code.get(1.0, tk.END)
        output_file.write(text)
    # Save the memory as binary. First change the extension.
    binFilePath = filepath.replace(".asm",".bin")
    with open(binFilePath, "wb") as binary_file:
        binary_file.write(memory)

    
# Return a string with the hex, digital, octal, and binary representations of 
# the 8-bit memory number who's location is passed.
def show_number(index):
    value = memory[index]
    return format_number(value)

# Return a string with the hex, digital, octal, and binary representations of 
# the 8-bit memory number who's value is passed.
def format_number(value):
    return f"{value:02x}|{value:03}|{value:03o}|{value:08b}".upper()
    
# Return true is the emulator is running.
def isEmulatorRunning():
    global stepping
    global autoRun
    
    return stepping or autoRun or run

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
    special_canvas.create_text(SPECIAL_X, SPECIAL_Y+BYTE_Y*9, font=('Courier',14,'bold'), anchor=tk.W, text=f"ADDR: " + format_number(addressRegister))
    
    # Dump the memory locations.
    dump_canvas.delete("all")
    for row in range(8):
        dump_canvas.create_text(HEX_DUMP_X, HEX_DUMP_Y+row*BYTE_Y, font=('Courier',14,'bold'), text=f"{row*32:03}:".upper())
        for col in range(32):
            fillColor = "black"
            if row*32+col == memory[PC]:
                fillColor = "green"
            dump_canvas.create_text(HEX_DUMP_X+(col+1)*BYTE_X+20, HEX_DUMP_Y+row*BYTE_Y, fill=fillColor, font=('Courier',14,'bold'), text=f"{memory[row*16+col]:02x}".upper())
    
    # Dump the memory details.
    first, _ = memory_details.yview()
    memory_details.delete('1.0',tk.END)
    for i in range(256):
        if i == memory[PC]:
            memory_details.insert(tk.END, f"{i:03}: " + show_number(i)+ "\n", 'PC')
        else:
            memory_details.insert(tk.END, f"{i:03}: " + show_number(i)+ "\n")
    memory_details.yview_moveto(first)
    
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
    global breakPoints
    global atBreakpoint
    
    # Check for breakpoint.
    if memory[PC] in breakPoints:
        if not atBreakpoint:
            # Honor the breakpoint.
            atBreakpoint = True
            return False
        else:
            # Let the execution continue past the breakpoint.
            atBreakpoint = False
   
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
    global stepping
    
    global inputState
    global addressState
    global memoryState
    global runState
    
    # Set the running mode.
    run = True
    autoRun = False
    singleStep = False
    stepping = False
    
    inputState = False
    addressState = False
    memoryState = False
    runState = True
    
# Run the program at full speed.
def restart_program():
    global memory
    global restart
    global addressRegister
    
    # Stop all program activity.
    stop_program()
    
    # Replace memory with a fresh copy from the load.
    memory[:] = restart
    
    # Initialize the instruction pointer to the default.
    memory[PC] = 4
    
    # Clear the address register.
    addressRegister = 0
    
# Clear memory and workspace.
def clear_program():
    global memory
    global restart
    global addressRegister
    
    # Stop all program activity.
    stop_program()
    
    # Clear the memory.
    memory[:] = bytearray(256)
    
    # Initialize the instruction pointer to the default.
    memory[PC] = 4
    
    # Clear the address register.
    addressRegister = 0
    
    # Remove any text from the assembly area.
    txt_code.delete(1.0, tk.END)

# Run the program at about one instruction per second.       
def auto_run_program():
    global autoRun
    global nextStepTime
    global run
    global singleStep
    global stepping
    
    global inputState
    global addressState
    global memoryState
    global runState
    
    # Set the running mode.
    autoRun = True
    run = False
    singleStep = False
    stepping = False
    
    inputState = False
    addressState = False
    memoryState = False
    runState = True
    
    # Set the time for the next instruction to run at.
    nextStepTime = int(time.time() * 1000) + 1000
        
    
# Perform the next step in the loaded program.
def step_program():
    global singleStep
    global stepping
    global autoRun
    global run
    
    global inputState
    global addressState
    global memoryState
    global runState
    
    # Set the running mode.
    singleStep = True
    stepping = True
    autoRun = False
    run = False
    
    inputState = False
    addressState = False
    memoryState = False
    runState = True

# Stop the currently running program.  
def stop_program():
    global run
    global autoRun
    global singleStep
    global stepping
    
    global inputState
    global addressState
    global memoryState
    global runState
    
    run = False
    autoRun = False
    singleStep = False
    stepping = False
    
    inputState = False
    addressState = False
    memoryState = False
    runState = False

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
            return "???????????? ???", programCounter
        if opCode in {"and","or","lneg"} and not register == "A":
            return "???????????? ???", programCounter
        
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
            
            return f"[{opValue:02x}|{opValue:03}|{opValue:03o}]".upper() + " " + address, programCounter+2
        else:
            return "???????????? ???", programCounter 
    return "???????????? ???", programCounter

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
            return "???????????? ???", programCounter
        if not comparison in {"NE","EQ","LT","GE","GT","GLE"}:
            return "???????????? ???", programCounter
        
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
                return "????????????? ???", programCounter
            
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
            
            return f"[{opValue:02x}|{opValue:03}|{opValue:03o}]".upper() + " " + address, programCounter+2
        else:
            return "???????????? ???", programCounter 
    return "???????????? ???", programCounter

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
            return "???????????? ???", programCounter
        if not compareBit in {"0","1"}:
            return "???????????? ???", programCounter
        
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
            
            return f"[{opValue:02x}|{opValue:03}|{opValue:03o}]".upper() + " " + address, programCounter+2
        else:
            return "???????????? ???", programCounter 
    return "???????????? ???", programCounter

def process_shift_and_rotate_opcodes(opCode, operands, programCounter):
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
            return "???????????? ???", programCounter
        if not direction in {"L","R"}:
            return "????????????", programCounter
        if not amount in {"1","2","3","4"}:
            return "????????????", programCounter
        
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
            
        return f"[{opValue:02x}|{opValue:03}|{opValue:03o}]".upper(), programCounter+1
    return "????????????", programCounter

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
        return process_shift_and_rotate_opcodes(opCode, operands, programCounter)
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
                    return "[80|128|200]", programCounter+1
                elif opCode == "halt":
                    # Save the op code into memory.
                    memory[programCounter] = 0b00000000
                    return "[00|000|000]", programCounter+1
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
        assembled = f"{showCounter:03}" + ":   " + processed
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
    
# Create the left hand assembled code panel.
class TextAssembly(tk.Canvas):
    
    def __init__(self, textwidget, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.codeLines = {}
        self.textwidget = textwidget
        self.configure(width=16, state="disabled", background="light grey")
        self.bind('<Button-1>', self.toggleBreakPoint)
        self.redraw()
        
    # Set or clear the break point at the line passed.
    def toggleBreakPoint(self, event):
        global breakPoints
         
        for y in self.codeLines.keys():
            if event.y > y and event.y < y + 15:
                address = self.codeLines[y]
                if (address > 0):
                    if address in breakPoints:
                        breakPoints.remove(address)
                    else:
                        breakPoints.append(address)
                break;


    # Redraw all of the assembled instructions in the visible part of the text window.
    def redraw(self):
        global breakPoints
        global atBreakpoint
        
        # Reset the modified flag.
        self.textwidget.edit_modified(False)
        
        # Clear the assembled code.
        self.delete("all")
        
        # Clear the code lines dictionary.
        self.codeLines.clear()
        
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
            line = assembledLines[lineindex]
            color = "black"
            programCounter = 0
            if line != "":
                programCounter = int(line.split(":")[0])
                if programCounter == memory[PC]:
                    if atBreakpoint:
                        color = "red"
                    else:
                        color = "green"
            self.codeLines[y] = programCounter
            self.create_text(5,y,anchor="nw", font=('Courier',14,'bold'), fill=color, text=line)
            if programCounter in breakPoints:
                self.create_text(290,y+1,anchor="nw", font=('Courier',20,'bold'), fill="red", text="*")
            i = self.textwidget.index("%s+1line" % i)

# Maintain a list of breakpoint positions in memory.
breakPoints = []
        
# Setup the working window.
window = tk.Tk()
window.title("KENBAK-2/5 IDE")
window.geometry("1590x905")
window.rowconfigure(0, minsize=10, weight=0)
window.rowconfigure(1, minsize=600, weight=0)
window.rowconfigure(2, minsize=250, weight=1)
window.columnconfigure(0, minsize=100, weight=0)
window.columnconfigure(1, minsize=800, weight=1)
window.columnconfigure(2, weight=0)

codeFont = Font(family="Courier", size=14)
buttonFont = Font(family="Arial", size=12)

# Row 2 Assembler
txt_code = tkscrolled.ScrolledText(window, font=codeFont, undo=True, autoseparators=True, maxundo=-1, borderwidth=2)
txt_code.configure(width=80, state="normal", wrap="none", padx="10")
txt_assembled = TextAssembly(txt_code, breakPoints)

# Row 3 Memory dump.
special_canvas = tk.Canvas(window, width=315, height=250, bg="dark gray")
dump_canvas = tk.Canvas(window, bg="white", height=250)
memory_details = tkscrolled.ScrolledText(window, font=('Courier',14,'bold'))
memory_details.configure(width=25, height=250, state="normal", wrap="none", padx="10")
memory_details.tag_config('PC', background="white", foreground="green")

fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=3)
btn_load = tk.Button(fr_buttons, font=buttonFont, text="Load", command=open_file)
btn_save = tk.Button(fr_buttons, font=buttonFont, text="Save As...", command=save_file)
btn_restart = tk.Button(fr_buttons, font=buttonFont, text="Restart", command=restart_program)
btn_clear = tk.Button(fr_buttons, font=buttonFont, text="Clear", command=clear_program)
btn_run = tk.Button(fr_buttons, font=buttonFont, text="Run", command=run_program)
btn_auto = tk.Button(fr_buttons, font=buttonFont, text="Auto", command=auto_run_program)
btn_step = tk.Button(fr_buttons, font=buttonFont, text="Step", command=step_program)
btn_stop = tk.Button(fr_buttons,  font=buttonFont,text="Stop", command=stop_program)

btn_load.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
btn_restart.grid(row=0, column=2, sticky="ew", padx=5)
btn_clear.grid(row=0, column=3, sticky="ew", padx=5)
btn_run.grid(row=0, column=4, sticky="ew", padx=5)
btn_auto.grid(row=0, column=5, sticky="ew", padx=5)
btn_step.grid(row=0, column=6, sticky="ew", padx=5)
btn_stop.grid(row=0, column=7, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, columnspan="3", sticky="ew")
txt_assembled.grid(row=1, column=0, sticky="nsew")
txt_code.grid(row=1, column=1, columnspan="2", sticky="nsew")
special_canvas.grid(row=2, column=0, sticky="nsew")
dump_canvas.grid(row=2, column=1, sticky="nsew")
memory_details.grid(row=2, column=2, sticky="nsew")

# Reserve space for the 256 byte memory of the KENBAK-1.
memory = bytearray(256)  # All bytes are initialized to null (zeros).
restart = bytearray(256)  # All bytes are initialized to null (zeros).

# Define the valid op codes.
opCodes = {"add","sub","load","store","and","or","lneg","jmp","jmk","skp","set","sft","rot","nop","halt","org"}

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
    
# Control the behavior of the program.
singleStep = False
stepping = False
autoRun = False
run = False
nextStepTime = 0
atBreakpoint = False

# Define the various states that the console can be in.
powerOn  = False
inputState = True
addressState = False
memoryState = False
runState = False

# Define the address register used when reading and storing data.
addressRegister = 0

while True:
    
    if wiringPiLoaded:
        # Handle the toggles, buttons, and lamps on the console.
        # Check for the power on button.
        if not wiringpi.digitalRead(toggle_on) and not powerOn:
            # Clear the memory. This is not strictly required as
            # the original will have random data when powered on.
            # Also no need to press Start and Stop to initialize
            # the internal control circuits. Just feel that this 
            # is cleaner.
            memory = bytearray(256)
            
            # Default program start location.
            memory[PC] = 4
            
            inputState = True
            addressState = False
            memoryState = False
            runState = False
            powerOn = True
        elif not wiringpi.digitalRead(toggle_off) and powerOn:
            inputState = False
            addressState = False
            memoryState = False
            runState = False
            powerOn = False
            
        # Show what state we are in.
        if inputState:
            wiringpi.digitalWrite(light_clear,1)
        else:
            wiringpi.digitalWrite(light_clear,0)
        if addressState:
            wiringpi.digitalWrite(light_set,1)
        else:
            wiringpi.digitalWrite(light_set,0)
        if memoryState:
            wiringpi.digitalWrite(light_store,1)
        else:
            wiringpi.digitalWrite(light_store,0)
        if runState:
            wiringpi.digitalWrite(light_stop,1)
        else:
            wiringpi.digitalWrite(light_stop,0)
            
        # Handle the data buttons.
        if not wiringpi.digitalRead(button_0):
            memory[INPUT] |= 0b00000001
        elif not wiringpi.digitalRead(button_1):
            memory[INPUT] |= 0b00000010
        elif not wiringpi.digitalRead(button_2):
            memory[INPUT] |= 0b00000100
        elif not wiringpi.digitalRead(button_3):
            memory[INPUT] |= 0b00001000
        elif not wiringpi.digitalRead(button_4):
            memory[INPUT] |= 0b00010000
        elif not wiringpi.digitalRead(button_5):
            memory[INPUT] |= 0b00100000
        elif not wiringpi.digitalRead(button_6):
            memory[INPUT] |= 0b01000000
        elif not wiringpi.digitalRead(button_7):
            memory[INPUT] |= 0b10000000
            
        # Handle the clear button.
        if not wiringpi.digitalRead(button_clear):
            memory[INPUT] = 0b00000000
            inputState = True
            addressState = False
            memoryState = False
        
        # Handle the display button.
        if not wiringpi.digitalRead(button_display) and not runState:
            inputState = False
            addressState = True
            memoryState = False
            runState = False
            
        # Handle the set button.
        if not wiringpi.digitalRead(button_set) and not runState and inputState:
            addressRegister = memory[INPUT]
            
        # Handle the read button.
        if not wiringpi.digitalRead(button_read) and not runState:
            addressRegister += 1
            inputState = False
            addressState = False
            memoryState = True
            runState = False
            debounceButton(button_read)
            
        # Handle the store button.
        if not wiringpi.digitalRead(button_store) and not runState and inputState and not wiringpi.digitalRead(toggle_unl):
            memory[addressRegister] = memory[INPUT]
            addressRegister += 1
            debounceButton(button_store)
            
        # Handle the start button.
        if not wiringpi.digitalRead(button_start) and not runState:
            inputState = False
            addressState = False
            memoryState = False
            runState = True
            
            autoRun = False
            run = True
            singleStep = False
            stepping = False
            
        # Handle the stop button.
        if not wiringpi.digitalRead(button_stop) and runState:
            inputState = False
            addressState = False
            memoryState = False
            runState = False
            
            run = False
            autoRun = False
            singleStep = False
            stepping = False
            
            # As long as the stop button is pressed ee if the user wants to single step.
            while not wiringpi.digitalRead(button_stop):
                if not wiringpi.digitalRead(button_start):
                    # User pressed start and stop ate the same time, so single step.
                    runState = True
                    singleStep = True
                    stepping = True
                    debounceButton(button_start)
                    break
            
    # Update the console data lamps depending on the state we 
    # are in.
    if powerOn:
        if inputState:
            show_data_lamps(memory[INPUT])
        elif addressState:
            show_data_lamps(addressRegister)
        elif memoryState:
            show_data_lamps(memory[addressRegister-1])
        else:
            show_data_lamps(memory[OUTPUT])
    
    # Check to see if we want to run the next step of the program.
    if singleStep or run or (autoRun and int(time.time() * 1000) > nextStepTime):
        if perform_next_instruction() == False:
            # Halt encountered.
            stop_program()
        singleStep = False
        nextStepTime = int(time.time() * 1000) + 1000
    
    # Update the memory part of the screen,
    try:
        txt_assembled.redraw()
        draw_state()
        window.update_idletasks()
        window.update()
        
        # Wait a bit.
        sleep(.001)
    except:
        # Ignore to prevent error when application is destroyed.
        pass
    
    

