"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        raw_lines = input_file.read().splitlines()
        self.input_lines = []
        for line in raw_lines:
            line = line.strip()
            if line and not line.startswith("//"):
                if "//" in line:
                    line = line.split("//")[0].strip()
                self.input_lines.append(line)
        self.current_line = -1
        self.current_command = ""
        self.advance()

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_line < len(self.input_lines)



    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.current_line += 1
        if self.current_line < len(self.input_lines):
            self.current_command = self.input_lines[self.current_line]
        else:
            self.current_command = ""


    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if '@' in self.current_command:
            return "A_COMMAND"
        elif '(' in self.current_command:
            return "L_COMMAND"
        elif '=' in self.current_command or ';' in self.current_command:
            return "C_COMMAND"
        else:
            return ""

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.current_command[1:]
        elif self.command_type() == "L_COMMAND":
            return self.current_command[1:-1]

    def dest(self) -> str:
        command = self.current_command.replace(" ", "")  # Remove ALL whitespace
        if '=' in command:
            return command.split('=')[0]
        return ""

    def comp(self) -> str:
        command = self.current_command.replace(" ", "")  # Remove ALL whitespace
        if '=' in command:
            return command.split('=')[1].split(';')[0]
        else:
            return command.split(';')[0]

    def jump(self) -> str:
        command = self.current_command.replace(" ", "")  # Remove ALL whitespace
        if ';' in command:
            return command.split(';')[1]
        return ""
