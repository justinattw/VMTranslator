//  push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  pop pointer 1
@THAT
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop that 0
@THAT
D=M
@0
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop that 1
@THAT
D=M
@1
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  push constant 2
@2
D=A
@SP
AM=M+1
A=A-1
M=D
//  sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
//  pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  label MAIN_LOOP_START
(MAIN_LOOP_START)
//  push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  if-goto COMPUTE_ELEMENT
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE
//  goto END_PROGRAM
@END_PROGRAM
0;JMP
//  label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
//  push that 0
@THAT
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  push that 1
@THAT
D=M
@1
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
//  pop that 2
@THAT
D=M
@2
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push pointer 1
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
//  push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
//  add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
//  pop pointer 1
@THAT
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  push constant 1
@1
D=A
@SP
AM=M+1
A=A-1
M=D
//  sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
//  pop argument 0
@ARG
D=M
@0
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
//  label END_PROGRAM
(END_PROGRAM)
