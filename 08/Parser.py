"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """
    arithmetic_commands = {"add", "sub", "and", "or", "eq", "gt", "lt","neg","not","shiftleft","shiftright"}
    memory_commands = {"push", "pop"}
    branching_commands = {"label", "if-goto", "goto"}
    function_commands = {"call", "function", "return"}

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        raw_lines = input_file.read().splitlines()
        self.current_line = 0
        self.input_lines = []
        # remove comments and empty lines
        for line in raw_lines:
            # Remove whitespace
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("//"):
                # Remove inline comments
                if "//" in line:
                    line = line.split("//")[0].strip()
                self.input_lines.append(line)
        self.current_command = self.input_lines[self.current_line]
    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.current_line < len(self.input_lines)-1:
            return True
        else:
            return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.current_line += 1
        if self.current_line < len(self.input_lines):
            self.current_command = self.input_lines[self.current_line]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        if self.current_command in self.arithmetic_commands:
            return "C_ARITHMETIC"
        elif self.current_command.split()[0] in self.memory_commands:
            return "C_" + self.current_command.split()[0].upper()
        elif self.current_command.split()[0] in self.branching_commands:
            return "C_" + self.current_command.split()[0].upper()
        elif self.current_command.split()[0] in self.function_commands:
            return "C_" + self.current_command.split()[0].upper()

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type == "C_RETURN":
            return None
        elif self.command_type() == "C_ARITHMETIC":
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        if self.command_type() in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
            return int(self.current_command.split()[2])

