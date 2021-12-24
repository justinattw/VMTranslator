//  push constant 3030
@3030
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop pointer 0
@THIS
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push constant 3040
@3040
D=A
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
//  push constant 32
@32
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop this 2
@THIS
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
//  push constant 46
@46
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop that 6
@THAT
D=M
@6
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
//  push pointer 0
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
//  push pointer 1
@THAT
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
//  push this 2
@THIS
D=M
@2
A=D+A
D=M
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
//  push that 6
@THAT
D=M
@6
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
