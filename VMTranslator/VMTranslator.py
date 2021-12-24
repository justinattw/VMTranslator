#!/usr/bin/env python3
import os
import sys
from collections import OrderedDict

from CodeWriter import CodeWriter
from Parser import Parser

PRIORITY_FILES = ["Sys.vm", "Main.vm"]


class Main:
    """
    The Main class contains the main logic of the VM VMTranslator
    """

    @staticmethod
    def translate(input_path: str):
        """
        Translates .vm code file(s) written in VM language, into .asm code file(s) in Assembly language.
        If provided input_path argument is a directory, this program will translate each .vm code file individually
        into a corresponding .asm code file (e.g., abc.vm will generate an abc.asm file).

        The .asm code file(s) is written and saved in the same directory as the input .vm code file(s) directory.

        :param input_path: a path to a .vm file, or a directory containing .vm file(s), to be translated into .asm
        files.
        """
        files: OrderedDict = Main.read_filepath_input(input_path)
        Main.translate_files(files, input_path)

        print(f"Translation completed. Translated {len(files)} file(s):\n\t", end="")
        print("\n\t".join(files.keys()))

    @staticmethod
    def translate_files(files: OrderedDict, input_path: str):
        code_writer = CodeWriter(input_path)
        for filepath in files:
            Main.translate_file(files[filepath], filepath, code_writer)

        code_writer.close()

    @staticmethod
    def translate_file(file: [str], filepath: str, code_writer: CodeWriter):
        parser = Parser(file)
        code_writer.set_filename(filepath)
        while parser.has_more_commands():

            parser.advance()
            command_type = parser.command_type()

            if command_type == "C_RETURN":
                code_writer.write_return()
                continue

            arg1 = parser.arg1()
            if command_type == "C_ARITHMETIC":
                code_writer.write_arithmetic(arg1)
                continue
            elif command_type in ["C_PUSH", "C_POP"]:
                arg2 = parser.arg2()
                code_writer.write_push_pop(command_type, arg1, arg2)
                continue
            elif command_type == "C_LABEL":
                code_writer.write_label(arg1)
                continue
            elif command_type == "C_IF":
                code_writer.write_if(arg1)
                continue
            elif command_type == "C_GOTO":
                code_writer.write_goto(arg1)
                continue

            arg2 = parser.arg2()
            if command_type == "C_FUNCTION":
                code_writer.write_function(arg1, arg2)
            elif command_type == "C_CALL":
                code_writer.write_call(arg1, arg2)
            else:
                raise Exception(f"This project should not contain a '{command_type}' command type (yet).")

    @staticmethod
    def is_vm_file(filepath: str):
        return os.path.isfile(filepath) and filepath.endswith(".vm")

    @staticmethod
    def strip_extension(filename: str):
        return os.path.basename(filename).replace(".asm", "")

    @staticmethod
    def read_filepath_input(input_path) -> OrderedDict:
        """
        Reads the filepath_input and extracts all .vm files into a dictionary.

        :param input_path: a path to a .vm file, or a directory containing .vm file(s), to be translated into .asm
        files.
        :return: a dictionary consisting of filepath as keys, and the file as values {filename: file}.
        """
        if not os.path.exists(input_path):
            raise Exception(f"The provided path '{input_path}' does not exist.")

        files = OrderedDict()

        # Read single file into files dict
        if Main.is_vm_file(input_path):
            file = Main.read_vm_file(input_path)
            files[input_path] = file
            return files

        if not os.path.isdir(input_path):
            raise Exception(f"Input path '{input_path}' must be a valid .vm file, or an existing directory.")

        files_in_dir = os.listdir(input_path)

        # # Read priority .vm files into dict first
        # for priority_file in PRIORITY_FILES:
        #     if priority_file not in files_in_dir:
        #         continue
        #     files = Main.read_file_into_dict(input_path, priority_file, files)
        #     files_in_dir.remove(priority_file)  # remove read file from files_in_dir

        for filename in files_in_dir:
            Main.read_file_into_dict(input_path, filename, files)  # Read .vm file from filepath into 'files' dict

        if not files:
            raise Exception(f"No vm files found in input path '{input_path}'.")

        return files

    @staticmethod
    def read_file_into_dict(dir_path: str, filename: str, files: OrderedDict):
        full_filepath = os.path.join(dir_path, filename)
        if not Main.is_vm_file(full_filepath):
            return files
        files[full_filepath] = Main.read_vm_file(full_filepath)  # Read .vm file from filepath into 'files' dict
        return files

    @staticmethod
    def read_vm_file(filename: str) -> [str]:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("PROGRAM NOT RUN. Usage: python VMTranslator.py directory/file")
        exit()

    path = sys.argv[1]
    Main.translate(path)
