; Generate all of the numbers in the Fibonacci Sequence that are less that 256.
; In the Fibonacci sequence, each number is the sum of the two preceding ones, 
; starting from 0 and 1. The generated sequence is stored in memory.

	load	A,0		; Seed the results with the first two numbers 
	store	A,results		; in the sequence 0 and 1.
	load	A,1
	store	A,results+1
	store	X,0		; Use the X register as an index into results.
loop	load	A,results+X		; Add the two preceding numbers.
	add	A,results+1+X
	skp	1,0,OCA		; Make sure the carry bit is not set.
	nop			; Padding. Skp skips two bytes.
	halt			; Carry bit set, register too small, stop.
	store	A,results+2+X		; Store the next number of the sequence.
	store	A,OUTPUT		; Show the next number on the display
	add	X,1		; Advance the X index for the next calculation.
	jmp	loop		; Find the next number.
results	0			; The Fibonacci sequence will be stored here.


