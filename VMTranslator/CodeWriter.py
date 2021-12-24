#!/usr/bin/env python3
import os

# Maps the commands to their @segment RAM address names
SEGMENTS_MAPPER = {
    "argument": "ARG",
    "local": "LCL",
    "this": "THIS",
    "that": "THAT"
    # "static": "",
    # "constant": "",
    # "pointer": "",
    # "temp": ""
}


class CodeWriter:

    def __init__(self, filepath, log_vm_commands=True):

        # Set filepath of output .asm file
        if filepath.endswith(".vm"):
            out_filename = filepath.replace(".vm", ".asm")
        elif os.path.isdir(filepath):
            base_dir_name = os.path.basename(filepath)
            if len(base_dir_name) == 0:
                raise Exception("Base directory name cannot be empty.")
            out_filename = os.path.join(filepath, base_dir_name + ".asm")
        else:
            out_filename = filepath

        print(f"Writing to output file '{out_filename}'.")

        if not out_filename.endswith(".asm"):
            raise Exception(f"Output filepath '{filepath}' must be a '.asm' file")

        self._in_filepath = filepath
        self._out_filename = out_filename
        self._write_file = open(out_filename, "w+")
        self._current_filename = None
        self._current_function = None
        self.arith_jump_counter = 0
        self.return_counter = 0
        self._log_vm_commands = log_vm_commands

        self.write_init()

    # region Properties
    @property
    def in_filepath(self):
        """
        :return: The base filepath of which the CodeWriter is writing to
        """
        return self._in_filepath

    @property
    def out_filename(self):
        return self._out_filename

    @property
    def current_filename(self):
        return self._current_filename

    @property
    def current_function(self):
        return self._current_function

    @current_function.setter
    def current_function(self, function_name):
        self._current_function = function_name

    @property
    def in_function(self):
        return self.current_function is not None

    @property
    def write_file(self):
        return self._write_file

    @property
    def arith_jump_counter(self):
        return self._arith_jump_counter

    @arith_jump_counter.setter
    def arith_jump_counter(self, num: int):
        self._arith_jump_counter = num

    @property
    def return_counter(self):
        return self._return_counter

    @return_counter.setter
    def return_counter(self, num: int):
        self._return_counter = num

    @property
    def log_vm_commands(self):
        return self._log_vm_commands

    # endregion

    def set_filename(self, filepath: str):
        self._current_filename = os.path.basename(filepath).replace(".vm", "")
        self.current_function = None

    def write(self, commands: [str]):
        """
        :param commands: A list of asm commands to be written to the open output file.
        """
        lines = "\n".join(commands) + "\n"
        self.write_file.write("%s" % lines)

    def close(self):
        self.write_file.close()
        # if self.in_function and self.current_function != "Sys.init":
        #     raise Exception(f"Unexpected unreturned function: {self.current_function}")

    def write_init(self):
        """
        If translating a full directory, add bootstrap code.

        Bootstrap code:
            SP=256
            call Sys.init
        """
        if not os.path.isdir(self.in_filepath):
            return

        if self.log_vm_commands:
            self.write(["//  Boostrap code"])  # Log vm command

        bootstrap_code = [
            "@256",
            "D=A",
            "@SP",
            "M=D"
        ]
        self.write(bootstrap_code)
        self.write_call("Sys.init", 0)
        return

    # region StackArithmetic writes
    def write_arithmetic(self, vm_command: str):
        """
        :param vm_command: Arithmetic vm commands translated into asm commands, and write them to the open output file.
        """
        if self.log_vm_commands:
            self.write([f"//  {vm_command}"])  # log vm command associated with generated asm commands
        asm_commands = self.translate_arithmetic_vm_code_to_assembly(vm_command)
        self.write(asm_commands)

    def write_push_pop(self, command_type: str, segment: str, index: int):
        """
        Writes asm commands to output file, based on given parameters.
        :param command_type:
        :param segment:
        :param index:
        :return:
        """
        if self.log_vm_commands:
            command = "push" if command_type == "C_PUSH" else "pop"
            self.write([f"//  {command} {segment} {index}"])  # log vm command associated with generated asm commands

        if command_type == "C_PUSH":
            asm_commands = self.translate_push_vm_code_to_asm(segment, index)
        elif command_type == "C_POP":
            asm_commands = self.translate_pop_vm_code_to_asm(segment, index)
        else:
            raise Exception(f"Command type '{command_type}' erroneously triggered a write_push_pop() method.")

        self.write(asm_commands)

    # endregion

    # region Branching commands
    def write_label(self, label: str):
        if self.log_vm_commands:
            self.write([f"//  label {label}"])  # log vm command associated with generated asm commands

        label = f"{self.current_function}.{label}" if self.in_function else label
        asm_commands = [f"({label})"]
        self.write(asm_commands)

    def write_goto(self, label: str):
        if self.log_vm_commands:
            self.write([f"//  goto {label}"])  # log vm command associated with generated asm commands

        label = f"{self.current_function}.{label}" if self.in_function else label
        asm_commands = [
            f"@{label}",
            "0;JMP"  # Unconditional jump to label
        ]
        self.write(asm_commands)

    def write_if(self, label: str):
        if self.log_vm_commands:
            self.write([f"//  if-goto {label}"])  # log vm command associated with generated asm commands

        label = f"{self.current_function}.{label}" if self.in_function else label

        asm_commands = [
            "@SP",
            "AM=M-1",
            "D=M",  # Pop value from SP
            f"@{label}",
            "D;JNE"  # Jump if not equal to 0 (not false, i.e., true)
        ]
        self.write(asm_commands)

    # endregion

    # region Function writes
    def write_function(self, function_name: str, num_local_vars: int):

        self.current_function = function_name

        if self.log_vm_commands:
            # log vm command associated with generated asm commands
            self.write([f"//  function {function_name} {num_local_vars}"])

        # Declare label for function entry
        asm_commands = [
            f"({function_name})",
        ]

        # Declare 'num_local_vars' number of local variables and initialise them all to 0
        local_reg = CodeWriter.get_ram_code("local")
        for i in range(num_local_vars):
            asm_commands.extend([
                f"@{local_reg}",
                "D=M",
                f"@{i}",    # Address = *LCL + i
                "A=D+A",
                "M=0",      # Initialise to 0
                "@SP",
                "M=M+1"     # SP++, set SP past LCL
            ])

        self.write(asm_commands)

    def write_call(self, function_name: str, num_vars: int):
        if self.log_vm_commands:
            self.write([f"//  call {function_name} {num_vars}"])  # log vm command of generated asm commands

        # # Push num_vars arguments into ARG
        # for num_arg in range(num_vars):
        #     self.write_push_pop("C_PUSH", "argument", num_arg)

        # Initialise
        asm_commands = []
        return_address_label = f"RETURN_{self.return_counter}"
        self.return_counter += 1
        # push @return_address
        asm_commands.extend([
            f"@{return_address_label}",
            "D=A",
        ])
        asm_commands.extend(self.translate_push_vm_code_to_asm("skip", None))

        for mem in ["local", "argument", "this", "that"]:
            # push LCL, ARG, THIS, THAT
            asm_commands.extend([
                f"@{self.get_ram_code(mem)}",
                "D=M"
            ])
            asm_commands.extend(self.translate_push_vm_code_to_asm("skip", None))

        asm_commands.extend([
            # ARG = SP - n - 5
            "@SP",
            "D=M",
            f"@{num_vars + 5}",
            "D=D-A",
            f"@{self.get_ram_code('argument')}",
            "M=D",

            # LCL = SP
            "@SP",
            "D=M",
            f"@{self.get_ram_code('local')}",
            "M=D",

            # goto function
            f"@{function_name}",
            "0;JMP",

            # Declare label for the return address
            f"({return_address_label})"
        ])

        self.write(asm_commands)

    def write_return(self):
        if self.log_vm_commands:
            self.write([f"//  return"])  # log vm command associated with generated asm commands

        asm_commands = [
            # FRAME = LCL
            f"@{CodeWriter.get_ram_code('local')}",
            "D=M",
            "@frame",   # A temp variable indicating the start of the current frame
            "M=D",
            # RET = *(FRAME - 5)
            "@5",
            "A=D-A",
            "D=M",
            "@return",     # A temp variable indicating return address
            "M=D",
            # *ARG = pop()
            "@SP",
            "AM=M-1",   # SP--
            "D=M",      # Pop value from SP into D reg (pop value is the return value of the current function)
            f"@{CodeWriter.get_ram_code('argument')}",
            "A=M",
            "M=D",      # Return value placed into *ARG, because this is where the top of the stack trace is for caller
            # SP = ARG+1
            "D=A+1",    # D reg = ARG+1, because the SP for caller begins again one address above ARG
            "@SP",
            "M=D",
            # THAT = *(FRAME - 1)
            "@frame",   # Restore THAT of caller
            "D=M",
            "@1",
            "A=D-A",
            "D=M",
            f"@{CodeWriter.get_ram_code('that')}",
            "M=D",      # THAT=FRAME-1
            # THIS = *(FRAME - 2)
            "@frame",   # Restore THIS of the caller
            "D=M",
            "@2",
            "A=D-A",
            "D=M",
            f"@{CodeWriter.get_ram_code('this')}",
            "M=D",
            # ARG = *(FRAME - 3)
            "@frame",  # Restore ARG of the caller
            "D=M",
            "@3",
            "A=D-A",
            "D=M",
            f"@{CodeWriter.get_ram_code('argument')}",
            "M=D",
            # LCL = *(FRAME - 4)
            "@frame",  # Restore LCL of the caller
            "D=M",
            "@4",
            "A=D-A",
            "D=M",
            f"@{CodeWriter.get_ram_code('local')}",
            "M=D",  # ARG=FRAME-3
            # goto RET
            "@return",
            "A=M",
            "0;JMP"  # Goto returnAddress from caller
        ]

        self.write(asm_commands)
    # endregion

    # region Translation methods
    def translate_arithmetic_vm_code_to_assembly(self, command: str) -> [str]:
        if command is None:
            raise Exception(f"Command given cannot be none.")

        # @SP-- and 'pop' first item from SP into M register
        asm_commands = [
            "@SP",
            "AM=M-1",
        ]
        if not (command == "neg" or command == "not"):
            # If not 'neg' or 'not' command, pop second item from SP into M register. First item goes into D register.
            asm_commands.extend([
                "D=M",
                "@SP",
                "AM=M-1",
            ])

        if command == "add":
            arith_commands = ["M=M+D"]
        elif command == "sub":
            arith_commands = ["M=M-D"]
        elif command == "neg":
            arith_commands = ["M=-M"]
        elif command in ["eq", "gt", "lt"]:
            # Use branching with JEQ/ JGT/ JLT to update *SP with 1 or 0
            arith_commands = [
                "D=M-D",  # compute to evaluate whether M==D/ M>D/ M<D
                f"@TRUE_{self.arith_jump_counter}"  # branch jump if true
            ]

            if command == "eq":
                arith_commands.append("D;JEQ")
            elif command == "gt":
                arith_commands.append("D;JGT")
            elif command == "lt":
                arith_commands.append("D;JLT")

            arith_commands.extend([
                "D=0",  # False branch, set D to 0 (false)
                f"@END_{self.arith_jump_counter}",
                "0;JMP",
                f"(TRUE_{self.arith_jump_counter})",  # True branch, set D to -1 (true)
                "D=-1",
                f"(END_{self.arith_jump_counter})",
                "@SP",
                "A=M",
                "M=D"  # Update SP to 0 or -1
            ])
            self.arith_jump_counter += 1

        elif command == "and":
            arith_commands = ["M=D&M"]
        elif command == "or":
            arith_commands = ["M=D|M"]
        elif command == "not":
            arith_commands = ["M=!M"]
        else:
            raise Exception(f"'{command}' is not a valid arithmetic command.")

        asm_commands.extend(arith_commands)

        # @SP--
        asm_commands.extend([
            "@SP",
            "M=M+1"
        ])

        return asm_commands

    def translate_push_vm_code_to_asm(self, segment: str, index: int):
        """
        Example 1: vm code "push static 17" -> asm pseudocode "*SP=@static.17, @SP++"
        :param segment:
        :param index:
        :param filename:
        :return:
        """
        asm_commands = []

        # Skip already has value in D reg
        if segment != "skip":
            # Get segment value into M reg (except for 'constant' which goes into D reg)
            asm_commands.extend(self.translate_segment_vm_code(segment, index))
            # Store value of M reg into D reg (except for 'constant', which already has value in D reg)
            if segment != "constant":
                asm_commands.append("D=M")

        # @SP++ and place value of D register into SP
        asm_commands.extend([
            "@SP",
            "AM=M+1",  # @SP++
            "A=A-1",  #
            "M=D"
        ])

        return asm_commands

    def translate_pop_vm_code_to_asm(self, segment: str, index: int):
        """

        :param segment:
        :param index:
        :param filename:
        :return:
        """
        if segment == "constant":
            raise Exception(f"Can't call 'pop()' operation on a '{segment}' segment")

        # Get segment address into A reg and segment value into M reg (except for 'constant')
        asm_commands = self.translate_segment_vm_code(segment, index)

        # SP-- and Move SP value into segment address
        asm_commands.extend([
            "D=A",  # D = segAddress
            "@SP",
            "AM=M-1",  # SP--, M = spVal
            "D=D+M",  # D = segAddress + spVal
            "A=D-M",  # A = *segAddress, M = segAddress
            "D=D-A",  # D = spVal
            "M=D"  # segAddress = spVal
        ])

        return asm_commands

    def translate_segment_vm_code(self, segment: str, index: int):
        """
        Set M register to the location of segment VM code specification
        :param segment:
        :param index:
        :return:
        """
        if segment in {"local", "argument", "this", "that"}:
            ram_code = CodeWriter.get_ram_code(segment)

            seg_commands = [f"@{ram_code}"]
            if index == 0:
                extend_commands = ["A=M"]
            else:
                extend_commands = [
                    "D=M",
                    f"@{index}",
                    "A=D+A"  # address = ram_code + index
                ]
            seg_commands.extend(extend_commands)

        elif segment == "static":
            if self.current_filename is None:
                raise Exception("")
            seg_commands = [f"@{self.current_filename}.{index}"]

        elif segment == "pointer":
            if index == 0:
                seg_commands = ["@THIS"]
            elif index == 1:
                seg_commands = ["@THAT"]
            else:
                raise Exception(f"The 'pointer' segment cannot take index '{index}'. Only accepts 0 or 1.")

        elif segment == "temp":
            seg_commands = [
                "@5",
                "D=A",
                f"@{index}",
                "A=D+A"
            ]

        elif segment == "constant":
            seg_commands = [
                f"@{index}",
                "D=A"
            ]

        else:
            raise Exception(f"Unexpected segment command '{segment}' read.")

        return seg_commands

    @staticmethod
    def get_ram_code(segment: str):
        """
        :param segment:
        :return:
        """
        ram_code = SEGMENTS_MAPPER[segment]
        if ram_code is None:
            raise Exception(f"Could not find corresponding ram_code for segment command '{segment}'.")
        return ram_code

    # endregion
