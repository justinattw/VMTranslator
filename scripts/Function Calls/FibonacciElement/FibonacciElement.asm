//  Boostrap code
@256
D=A
@SP
M=D
//  call Sys.init 0
@RETURN_0
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_0)
//  function Main.fibonacci 0
(Main.fibonacci)
//  push argument 0
@ARG
A=M
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
//  lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@TRUE_0
D;JLT
D=0
@END_0
0;JMP
(TRUE_0)
D=-1
(END_0)
@SP
A=M
M=D
@SP
M=M+1
//  if-goto IF_TRUE
@SP
AM=M-1
D=M
@Main.fibonacci.IF_TRUE
D;JNE
//  goto IF_FALSE
@Main.fibonacci.IF_FALSE
0;JMP
//  label IF_TRUE
(Main.fibonacci.IF_TRUE)
//  push argument 0
@ARG
A=M
D=M
@SP
AM=M+1
A=A-1
M=D
//  return
@LCL
D=M
@frame
M=D
@5
A=D-A
D=M
@return
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@frame
D=M
@1
A=D-A
D=M
@THAT
M=D
@frame
D=M
@2
A=D-A
D=M
@THIS
M=D
@frame
D=M
@3
A=D-A
D=M
@ARG
M=D
@frame
D=M
@4
A=D-A
D=M
@LCL
M=D
@return
A=M
0;JMP
//  label IF_FALSE
(Main.fibonacci.IF_FALSE)
//  push argument 0
@ARG
A=M
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
//  call Main.fibonacci 1
@RETURN_1
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_1)
//  push argument 0
@ARG
A=M
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
//  call Main.fibonacci 1
@RETURN_2
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_2)
//  add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
//  return
@LCL
D=M
@frame
M=D
@5
A=D-A
D=M
@return
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@frame
D=M
@1
A=D-A
D=M
@THAT
M=D
@frame
D=M
@2
A=D-A
D=M
@THIS
M=D
@frame
D=M
@3
A=D-A
D=M
@ARG
M=D
@frame
D=M
@4
A=D-A
D=M
@LCL
M=D
@return
A=M
0;JMP
//  function Sys.init 0
(Sys.init)
//  push constant 4
@4
D=A
@SP
AM=M+1
A=A-1
M=D
//  call Main.fibonacci 1
@RETURN_3
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
D=M
@6
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_3)
//  label WHILE
(Sys.init.WHILE)
//  goto WHILE
@Sys.init.WHILE
0;JMP