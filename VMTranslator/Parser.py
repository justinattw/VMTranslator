#!/usr/bin/env python3

from Command import Command
import re
from typing import List


class Parser:
    """
    Parser, is a class that handles the parsing of a single .vm (input) file.
    It reads a VM command, parses the command into its lexical components, and provides convenient access to these
    components.
    """

    def __init__(self, file: [str]):
        self._file = self.clean_file(file)
        self._current_command = None
        self._line = -1

    @property
    def file(self):
        """
        :return: The file that the Parser is currently parsing
        """
        return self._file

    @property
    def current_command(self) -> Command:
        """
        :return: The current command that the Parser is currently parsing
        """
        return self._current_command

    @current_command.setter
    def current_command(self, string: str):
        self._current_command = Command(string)

    @property
    def line(self):
        """
        :return: The line number that the Parser is parsing, and is related to the current_command currently 'active'
        """
        return self._line

    @line.setter
    def line(self, i: int):
        self._line = i

    def has_more_commands(self):
        """
        :return: False if line number is at the end of the file, else True
        """
        return self.line + 1 < len(self.file)

    def advance(self):
        """
        Progresses the current line and command of a file being parsed
        """
        self.line += 1
        self.current_command = self.file[self.line]

    def command_type(self) -> str:
        """
        :return: The command type corresponding to the current command.
        """
        return self.current_command.command_type

    def arg1(self) -> str:
        """
        :return: The first argument corresponding to the current command.
        """
        return self.current_command.arg1

    def arg2(self) -> int:
        """
        :return: The second argument corresponding to the current command.
        """
        return self.current_command.arg2

    @staticmethod
    def clean_file(file: List[str]):
        """
        Removes the file of all comments and empty lines
        :param file:
        :return:
        """
        line = 0
        while line < len(file):
            file[line] = Parser.clean_line(file[line])
            if Parser.is_blank(file[line]):
                file.pop(line)
                continue
            line += 1
        return file

    @staticmethod
    def clean_line(line: str):
        """
        :return: line with comments and leading/ trailng whitespaces removed
        """
        line = re.sub('//.*', "", line)  # remove comments
        line = line.strip()  # strip leading/ trailing whitespaces
        return line

    @staticmethod
    def is_blank(line: str) -> bool:
        """
        :param line: any string
        :return: true if line is empty or consists of only whitespace, else false
        """
        return not line or line.isspace()

