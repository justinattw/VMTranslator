#!/usr/bin/env python3

COMMAND_TYPES = {"C_ARITHMETIC", "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION", "C_RETURN", "C_CALL"}
# A set of commands in VM language, and their associated Command Type
COMMAND_TYPE_MAP = {
    # Stack
    "pop": "C_POP",
    "push": "C_PUSH",
    # Arithmetic
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    # Branching
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if-goto": "C_IF",
    # Function
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL"
}
# If command type in this blacklist, then arg1 should not be filled
ARG1_BLACKLIST_COMMAND_TYPES = {"C_RETURN"}
# Arg2 should be filled if and only if command type is in this whitelist
ARG2_WHITELIST_COMMAND_TYPES = {"C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"}


class Command:

    def __init__(self, string: str):
        self._command_type = None
        self._arg1 = None
        self._arg2 = None
        commands: [str] = string.split(" ")
        if len(commands) == 0:
            raise Exception(f"Line with 0 commands found.")

        self.command_type = commands[0]
        if self.command_type == "C_ARITHMETIC":
            self.arg1 = commands[0]
            return

        elif self.command_type == "C_RETURN":
            return

        elif len(commands) == 1:
            raise Exception(f"Non-arithmetic command '{string}' with only one argument given.")

        self.arg1: str = commands[1]
        if len(commands) == 2:
            return

        self.arg2: str = commands[2]
        if len(commands) > 3:
            raise Exception(f"Line with more than 3 commands found: {string}.")

    @property
    def command_type(self) -> str:
        return self._command_type

    @command_type.setter
    def command_type(self, string: str):
        if string not in COMMAND_TYPE_MAP:
            raise Exception(f"Unidentified command '{string}' found.")
        self._command_type = COMMAND_TYPE_MAP.get(string)

    @property
    def arg1(self) -> str:
        if not self.is_valid_arg1_call():
            raise Exception("arg1 should not be called when command is of type C_RETURN.")
        return self._arg1

    @arg1.setter
    def arg1(self, string: str):
        if not self.is_valid_arg1_call():
            raise Exception("arg1 should not be given when command of type C_RETURN is called.")
        self._arg1 = self.command_type if self.is_arithmetic_command() else string

    def is_valid_arg1_call(self):
        return self.command_type not in ARG1_BLACKLIST_COMMAND_TYPES

    def is_arithmetic_command(self):
        return COMMAND_TYPE_MAP.get(self.command_type) == "C_ARITHMETIC"

    @property
    def arg2(self) -> int:
        if self.command_type not in ARG2_WHITELIST_COMMAND_TYPES:
            raise Exception(f"arg2 should not be called when command of type {self.command_type} is called.")
        return self._arg2

    @arg2.setter
    def arg2(self, string: str):
        if self.command_type not in ARG2_WHITELIST_COMMAND_TYPES:
            raise Exception(f"arg2 should not be given when command of type {self.command_type} is called.")
        try:
            num = int(string)
            if num < 0:
                raise Exception(f"Command with index '{num}' given, but indexes cannot be negative.")
            self._arg2 = num
        except ValueError:
            raise Exception(f"arg2 must be an integer, instead '{string}' is given.")
