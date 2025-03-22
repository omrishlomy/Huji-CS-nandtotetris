"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code





def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    parser = Parser(input_file)
    symboltable = SymbolTable()
    variable_address = 16  # Initialize at the start of your assemble_file function

    def convert_to_binary(num: str) -> str:
        """Converts a decimal number to a 15-bit binary number.

        Args:
            num (str): a decimal number.

        Returns:
            str: the 15-bit binary representation of the number.
        """
        if num in symboltable.symbol_table:
            num = symboltable.symbol_table[num]
        return bin(int(num))[2:].zfill(15)

    def add_symbols():
        instruction_counter = 0
        clean_lines = []

        while parser.has_more_commands():
            # First, clean the command thoroughly
            command = parser.current_command.strip()
            if command == "" or command.startswith("//"):
                parser.advance()
                continue

            # Remove inline comments BEFORE checking command type
            command = command.split("//")[0].strip()

            # Update parser's current command with cleaned version
            parser.current_command = command

            # Now check command type with clean command
            if parser.command_type() == "L_COMMAND":
                symbol = parser.symbol()  # This will now get clean symbol
                symboltable.add_entry(symbol, instruction_counter)
            else:
                clean_lines.append(command)
                instruction_counter += 1
            parser.advance()
        parser.current_line = -1
        parser.input_lines = clean_lines
        parser.current_command = ""

    add_symbols()
    print(symboltable.symbol_table)
    while parser.has_more_commands():
        """translate the commands to binary. aka second pass"""
        command = parser.current_command.strip()
        if command == "" or command.startswith("//"):
            parser.advance()
            continue
        parser.current_command = command.split("//")[0].strip()
        if parser.command_type() == "L_COMMAND":
            parser.advance()
            continue
        elif parser.command_type() == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                output_file.write("0" + convert_to_binary(symbol) + "\n")
            elif symbol in symboltable.symbol_table:
                output_file.write("0" + convert_to_binary(symbol) + "\n")
            else:
                # Using variable_address from outer scope
                symboltable.add_entry(symbol, variable_address)
                output_file.write("0" + convert_to_binary(symbol) + "\n")
                variable_address += 1

        elif parser.command_type() == "C_COMMAND":
            current_binary_line = "111"
            current_binary_line += Code.comp(parser.comp())
            current_binary_line += Code.dest(parser.dest())
            current_binary_line += Code.jump(parser.jump()) if parser.jump() else "000"
            output_file.write(current_binary_line + "\n")

        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
