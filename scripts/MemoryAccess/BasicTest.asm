//  push constant 10
@10
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
//  push constant 21
@21
D=A
@SP
AM=M+1
A=A-1
M=D
//  push constant 22
@22
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop argument 2
@ARG
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
//  pop argument 1
@ARG
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
//  push constant 36
@36
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop this 6
@THIS
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
//  push constant 42
@42
D=A
@SP
AM=M+1
A=A-1
M=D
//  push constant 45
@45
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop that 5
@THAT
D=M
@5
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
M=D
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
//  push constant 510
@510
D=A
@SP
AM=M+1
A=A-1
M=D
//  pop temp 6
@5
D=A
@6
A=D+A
D=A
@SP
AM=M-1
D=D+M
A=D-M
D=D-A
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
//  push that 5
@THAT
D=M
@5
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
//  sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
//  push this 6
@THIS
D=M
@6
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
//  push this 6
@THIS
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
//  sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
//  push temp 6
@5
D=A
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
