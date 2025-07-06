; Program to calculate the day of the week for any date. To start this program you will
; have to input the date in four parts: Century, Year, Month, and Day. Each of the parts
; is entered as a two digit Binary Coded Decimal number (ie. the first digit will occupy 
; bits 7-4 as a binary number, and the second digit bits 3-0) using the front panel data
; buttons. The steps to run this program are:
;
; 1) Set the PC register (at address 3) to 4.
; 2) Clear the input data then enter the date Century.
; 3) Press Start.
; 4) Clear the input data then enter the date Year.
; 5) Press Start.
; 6) Clear the input data then enter the date Month.
; 7) Press Start.
; 8) Clear the input data then enter the date Day.
; 9) Press Start.
;
; The day of the week will be returned via the data lamps using the following encoding:
; 
;      7-Sunday 6-Monday 5-Tuesday 4-Wednesday 3-Thursday 2-Friday 1-Saturday
;
; All lamps turned on means the last item entered was invalid and you have to restart.
;
;
; Get the date we want the day for.
;
    load    A,INPUT         ; Get the century.
    jmk 	   bcd2bin
    store   A,century
    halt
    load    A,INPUT         ; Get the year.
    jmk     bcd2bin
    store   A,year
    halt
    load    A,INPUT         ; Get the month.
    jmk     bcd2bin
    sub     A,1			    ; Convert from 1 based to 0 based.
    store   A,month
    halt
    load    A,INPUT         ; Get the day.
    jmk     bcd2bin
    store   A,day
    load    A,0b10000000    ; Setup the rotation pattern.
    store   A,rotate
; 
; All the inputs should be in place. Start the conversion.
;
    load    A,year          ; Get the year.
    sft 	   A,R,2           ; Divide by 4.
    store   A,B             ; Save to B the working result.
    add     B,day           ; Add the day of the month.
    load    X,month         ; Use X as index into the month keys.
    add     B,monkeys+X     ; Add the month key.
    jmk     leapyr          ; Returns a leap year offset in A if applicable.
    jmk     working         ; Working...
    sub     B,A             ; Subtract the leap year offset.
    jmk     cencode         ; Returns a century code in A if applicable.
    jmk     working         ; Working...
    add     B,A             ; Add the century code.
    add     B,Year          ; Add the year input to the working result.
chkrem      
    load    A,B             ; Find the remainder when B is divided by 7.
    and     A,0b11111000    ; Is B > 7?
    jmp     A,EQ,isseven    ; No then B is 7 or less.
    sub     B,7             ; Yes then reduce B by 7.
    jmk     working         ; Working...
    jmp     chkrem          ; Check again for remainder.
isseven     
    load    A,B             ; Is B = 7?
    sub     A,7             ; Subtract 7 from B value.
    jmp     A,LT,gotday     ; No B is less than 7.
    load    B,0             ; Set B to zero because evenly divisible.
gotday      
    load    X,B             ; B holds the resulting day number. Use as index.
    load    A,sat+X         ; Convert to a day lamp.
    store   A,OUTPUT
    halt
error   
    load    A,0xff          ; Exit with error
    store   A,OUTPUT        ; All lamps lit.
    halt

;
; Store inputs.
;   
century db
year    db
month   db  
day     db

;
; Static table to hold month keys.
;
monkeys 1               
        4
        4
        0
        2
        5
        0
        3
        6
        1
        4
        6

;
; Need to preserve A while performing some steps.
;
saveA   db  

;
; Subroutine to blink the lamps to indicate working.
; 
rotate  db                  ; Pattern to rotate.
working db                  ; Save space for return adderess.
    store   A,saveA         ; Remember the value in A.  
    load    A,rotate        ; Get the rotate pattern.
    store   A,OUTPUT        ; Show the rotated pattern.
    rot     A,R,1           ; Rotate the pattern.
    store   A,rotate        ; Save the new rotation.
    load    A,saveA         ; Restore the value of A.
    jmp     (working)       ; Return to caller.

    org 133                 ; Skip over registers.

;
; Subroutine takes a BCD nuber in A as input and returns the equivalent binary number 
; also in A.
;   
bcd2bin db                  ; Save space for return address.    
    store   A,X             ; Save A.
    sft     A,R,4           ; Get the 10's digit.
    and     A,0b00001111	   ; Clear the high nibble.
    jmk     chkdig          ; Make sure digit is 0 - 9.
    store   A,B             ; B will hold the 10's digit x 10 result
    add     B,B             ; B now X 2
    sft     A,L,3           ; A is now 10's digit X 8
    add     B,A             ; B now 10's digit X 10
    store   X,A             ; Retrieve original value of A
    and     A,0b00001111    ; Get the 1's digit value in binary.
    jmk     chkdig          ; Make sure digit is 0 - 9.
    add     A,B             ; Add the 10's digit value in binary.
    jmp     (bcd2bin)       ; A now has the converted BCD value.

;
; Subroutine determines if the date is a leap year in January or February and returns
; an offset of 1 if it is, and 0 otherwise.
;
leapyr  db                  ; Save space for return address.    
    load    A,month         ; Check to see if month is January or February.
    and     A,0b11111110    ; Are any bits other than bit 0 set?
    jmp     A,NE,notlpyr    ; Yes then not January or February. Return 0.
    load    A,year          ; Is this an even century?
    jmp     A,NE,chkyear    ; No then have to check the year.
    load    A,century       ; Yes so see if century evenly divisible by 4.
    and     A,0b00000011    ; Are bits 1 or 0 set?
    jmp     A,EQ,islpyr     ; Yes evenly divisible by 4 and is a leap year.
    jmp     notlpyr         ; No this is not a leap year.
chkyear     
    load    A,year          ; See if rear evenly divisible by 4.    
    and     A,0b00000011    ; Are bits 1 or 0 set?
    jmp     A,NE,notlpyr    ; Yes so not evenly divisible by 4 and not a leap year.
islpyr  
    load    A,1             ; Offset 1.
    jmp (leapyr)            ; Return offset.    
notlpyr 
    load    A,0             ; Offset 0.
    jmp (leapyr)            ; Return offset.        

;
; Subroutine determines if a century code needs to be applied to the calculation.
;
cencode db                  ; Save space for return address.
    load    A,century       ; Century must be between 17 - 20.
chkmin  
    sub     A,17            ; Is century less than 17?
    jmp     A,GE,chkmax     ; Yes so century >= 17. Check max boundry.
    load    A,century       ; Increase century by 4.
    add     A,4
    store   A,century
    jmp     chkmin
chkmax  
    load    A,century       ; Century must be between 17 - 20.
    sub     A,20            ; Is century greater than 20?
    jmp     A,LT,retcode    ; No so calculate century code.
    jmp     A,EQ,retcode
    load    A,century       ; Decrease century by 4.
    sub     A,4
    store   A,century
    jmp     chkmax+2
retcode 
    load    X,century       ; Calculate the century code
    sub     X,17            ; Create an index into the century codes.           
    load    A,ctcodes+X     ; Get the appropriate century code.
    jmp     (cencode)       ; Return century code.          
;
; Subroutine that checks if the digit passed in A is in range 0 - 9.
;
chkdig  db                  ; Save space for return adderess.
    store   A,saveA         ; Remember value in A.
    load    A,9         
    sub     A,saveA         ; Subtract value passed from 9.
    and     A,0b10000000    ; Is negative bit set?
    jmp     A,NE,error      ; Yes so value in A not in range 0 - 9.
    load    A,saveA         ; No so A value in range. 
    jmp    (chkdig)         ; Return to caller.

;
; Static table to hold the output pattern for the day of the week.
;
sat     0b00000010
sun     0b10000000
mon     0b01000000
tues    0b00100000
wed     0b00010000
thur    0b00001000
fri     ; Pattern is 0b00000100, same as first item in ctcodes. Saves a byte.

;
; Static table to hold century codes.
;
ctcodes 4
        2
        0
        6
