//  push constant 0
@0
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop local 0
@LCL
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
//  label LOOP_START
(LOOP_START)
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
//  push local 0
@LCL
D=M
@0
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
//  pop local 0
@LCL
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
//  if-goto LOOP_START
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
//  push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
