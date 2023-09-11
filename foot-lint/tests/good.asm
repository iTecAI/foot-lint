#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
#
# FILE: $File$
# AUTHOR: P. White
# Contributors:
# W. Carithers
# K. Reek
# 
# DESCRIPTION:
# This program reads up to 10 of numbers (or until the user
# enters the value 9999) from the standard input, and then
# computes and prints their sum.
#-------------------------------
#
# CONSTANTS
#
MAX_SIZE = 10 # number of array elements
PRINT_STRING = 4 # arg for syscall to tell it to write
PRINT_INT = 1
#-------------------------------
#
# DATA AREAS
#
        .data
        .align 2 # word data must be on word boundaries
array:
        .space 4*MAX_SIZE # Reserve space for array to hold data
        # the array is up to MAX_SIZE words (4byte
        # each). Note the array isn’t initialized
size:
        .word 0 # Actual number of values in the array
        .align 0 # string data doesn’t have to be aligned
before:
        .asciiz "Values entered: "
        .text
        .align 2
#
# Name: main
#
# Description: EXECUTION BEGINS HERE
# Arguments: none
# Returns: none
# Destroys: t0,t1,t2,t3
#
FRAMESIZE_8 = 8
main:
        # allocate space for the stack frame
        # note: example of a long line
        addi $sp,$sp,-FRAMESIZE_8
        sw $ra,4($sp) # store the ra on the stack
        sw $s0,0($sp) # store the s0 on the stack
        la $a0,array # Pass the address of the array in a0
        li $a1,MAX_SIZE # and its max size in a1
        lw $ra,4($sp) # restore the registers
        lw $s0,0($sp)
        addi $sp,$sp,FRAMESIZE_8
        jr $ra # return from main and exit program
#
# Name: parray
#
# Description: prints the "size" number of integers from the
# array "array"
# Arguments: none
# Returns: none
# Destroys: t0,t1
#
#---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
parray:
        la $a0,array # a0 is the location of the array
        la $t0,size
        lw $a1, 0($t0) # a1 is the number of elements entered
done:
        li $v0,PRINT_STRING
        la $a0,lf
        syscall # print a newline
        jr $ra